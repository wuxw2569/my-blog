import base64
import os
import random
import re
from datetime import datetime
from pathlib import Path


TOPICS = [
    "AI如何帮助程序员自动生成日报",
    "用AI生成并部署个人网站",
    "AI自动生成SQL报表并可视化",
    "AI如何帮你写README文档",
    "用AI自动生成代码注释",
    "AI生成自动化测试用例",
    "AI自动总结会议纪要",
    "AI监控网站运行状态",
    "AI生成项目周报",
    "AI生成知识笔记并发布博客",
]

OUTPUT_BLOG_DIR = Path("docs/blog/posts")
OUTPUT_XHS_DIR = Path("docs/xhs")


def build_slug(topic):
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fa5]+", "-", topic).strip("-")
    return slug or "untitled"


def _latest_topic_dates(posts_dir):
    latest_dates = {}
    for md_path in posts_dir.glob("*.md"):
        match = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)\.md$", md_path.name)
        if not match:
            continue
        date_text, slug = match.groups()
        latest_dates[slug] = max(latest_dates.get(slug, ""), date_text)
    return latest_dates


def select_topic(topics, today, posts_dir=OUTPUT_BLOG_DIR, rng=None):
    """Pick a topic without overwriting today's generated post."""
    if not topics:
        raise ValueError("topics 不能为空")

    posts_dir = Path(posts_dir)
    latest_dates = _latest_topic_dates(posts_dir) if posts_dir.exists() else {}
    today_slugs = {
        re.match(rf"{re.escape(today)}-(.+)\.md$", md_path.name).group(1)
        for md_path in posts_dir.glob(f"{today}-*.md")
        if re.match(rf"{re.escape(today)}-(.+)\.md$", md_path.name)
    } if posts_dir.exists() else set()

    candidates = [topic for topic in topics if build_slug(topic) not in today_slugs]
    if not candidates:
        candidates = list(topics)

    scored = sorted(
        candidates,
        key=lambda topic: (latest_dates.get(build_slug(topic), ""), topic),
    )
    least_recent_date = latest_dates.get(build_slug(scored[0]), "")
    least_recent = [
        topic for topic in scored
        if latest_dates.get(build_slug(topic), "") == least_recent_date
    ]
    return (rng or random).choice(least_recent)


def unique_path(path):
    path = Path(path)
    if not path.exists():
        return path

    for index in range(2, 1000):
        candidate = path.with_name(f"{path.stem}-{index}{path.suffix}")
        if not candidate.exists():
            return candidate

    raise RuntimeError(f"无法生成不重复文件名: {path}")


def ensure_author(content):
    if "author:" in content[:500]:
        return content

    parts = content.split("---")
    if len(parts) >= 3:
        parts[1] = f"{parts[1].rstrip()}\nauthor: ai-helper\n"
        return "---".join(parts)

    return f"---\nauthor: ai-helper\n---\n{content}"


def normalize_content(content, cover_path):
    content = re.sub(r"```yaml[\s\S]*?```", "", content).strip()
    content = ensure_author(content)

    if content.startswith("---"):
        if "cover:" not in content[:500]:
            content = content.replace("---", f"---\ncover: {cover_path}", 1)
    else:
        content = f"---\ncover: {cover_path}\nauthor: ai-helper\n---\n{content}"

    return content


def get_client():
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        raise ValueError("请先配置环境变量 ZHIPUAI_API_KEY")

    from zhipuai import ZhipuAI

    return ZhipuAI(api_key=api_key)


def main():
    client = get_client()
    today = datetime.now().strftime("%Y-%m-%d")
    topic = select_topic(TOPICS, today)
    slug = build_slug(topic)

    image_dir = OUTPUT_BLOG_DIR / "images"
    OUTPUT_BLOG_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_XHS_DIR.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)

    blog_filename = unique_path(OUTPUT_BLOG_DIR / f"{today}-{slug}.md")
    xhs_filename = unique_path(OUTPUT_XHS_DIR / f"{today}-{slug}-xhs.md")
    image_filename = unique_path(image_dir / f"{today}-{slug}.png")
    cover_path = f"./images/{image_filename.name}"

    print(f"正在生成主题《{topic}》的博客...")

    blog_prompt = f"""
你是一位拥有10年经验的Java后端与架构开发者，请写一篇主题为《{topic}》的原创技术博客。

要求：
- Markdown 格式
- 包含：问题场景、AI解决思路、实现步骤（带代码示例）、效果展示、总结
- 结合架构层、网络层、数据层、工具层的工程视角
- 语气自然、有实操经验
- 输出时带 YAML 头部(title/date/tags/summary/author)，严格按照以下格式，只需要一个---开始和一个---结束，不要在YAML中使用额外的代码块或嵌套格式：
---
title: [文章标题]
date: [发布日期]
tags: [标签列表]
summary: [文章摘要]
author: ai-helper
---
"""

    resp = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": blog_prompt}],
    )
    content = resp.choices[0].message.content.strip()

    print("正在生成封面图...")
    try:
        image_prompt = f"一张横版16:9的封面图，主题是“{topic}”，风格未来感、极简科技感、亮色调"
        img_resp = client.images.generations(
            model="cogview-3",
            prompt=image_prompt,
            size="1024x576",
        )

        if img_resp and hasattr(img_resp, "data") and len(img_resp.data) > 0:
            image_base64 = getattr(img_resp.data[0], "b64_json", None)
            if image_base64:
                image_filename.write_bytes(base64.b64decode(image_base64))
                print(f"封面已保存：{image_filename}")
            else:
                print("未返回有效图像数据，跳过封面保存。")
        else:
            print("AI 未生成图像（data 为空），跳过封面生成。")
    except Exception as e:
        print(f"生成封面失败：{e}")

    content = normalize_content(content, cover_path)
    blog_filename.write_text(content, encoding="utf-8")
    print(f"博客已生成：{blog_filename}")

    print("正在生成小红书笔记版本...")
    xhs_prompt = f"""
请将以下博客内容改写成一篇适合小红书发布的笔记风格文章。

要求：
- 语气轻松、有吸引力、有实用感
- 用 emoji 表情适当点缀
- 开头要吸引人
- 添加3~5个小红书标签（如 #AI工具推荐 #效率神器 #编程日常）
- 内容长度控制在600字以内
- 最后附上一句总结性金句或call to action
博客内容如下：
{content}
"""

    xhs_resp = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": xhs_prompt}],
    )
    xhs_text = xhs_resp.choices[0].message.content.strip()

    xhs_header = f"""---
title: {topic}
date: {today}
cover: ../blog/posts/images/{image_filename.name}
platform: xiaohongshu
---

"""
    xhs_filename.write_text(xhs_header + xhs_text, encoding="utf-8")
    print(f"小红书笔记已生成：{xhs_filename}")


if __name__ == "__main__":
    main()
