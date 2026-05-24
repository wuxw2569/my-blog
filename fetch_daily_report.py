import argparse
import html
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree
from urllib.error import HTTPError, URLError


FEED_URL = "https://aihot.virxact.com/feed/daily.xml"
OUTPUT_FILE = Path("docs/daily.md")


def strip_html(text):
    text = re.sub(r"<[^>]+>", "", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_feed(xml_text, limit=12):
    root = ElementTree.fromstring(xml_text)
    items = []

    for item in root.findall("./channel/item")[:limit]:
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        description = strip_html(item.findtext("description", ""))
        pub_date = item.findtext("pubDate", "").strip()
        if title and link:
            items.append({
                "title": title,
                "link": link,
                "description": description,
                "pubDate": pub_date,
            })

    return items


def fetch_feed(url=FEED_URL, timeout=20):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "ai-blog-daily-report/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def render_markdown(items, source_url=FEED_URL, error=None):
    updated_at = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    lines = [
        "---",
        "title: AI 每日日报",
        "description: 自动订阅 AI Hot 每日日报 feed",
        "---",
        "",
        "# AI 每日日报",
        "",
        f"> 数据来源：[AI Hot 每日日报]({source_url})，最近更新：{updated_at}",
        "",
    ]

    if error:
        lines.extend([
            f"暂时无法获取外部日报源：`{error}`",
            "",
            "页面会在下一次自动任务中继续尝试更新。",
            "",
        ])
        return "\n".join(lines)

    if not items:
        lines.extend([
            "暂时没有抓取到日报内容，请稍后再看。",
            "",
        ])
        return "\n".join(lines)

    for item in items:
        description = item["description"][:260]
        lines.extend([
            f"## [{item['title']}]({item['link']})",
            "",
        ])
        if item["pubDate"]:
            lines.extend([f"`{item['pubDate']}`", ""])
        if description:
            lines.extend([description, ""])

    return "\n".join(lines)


def build_daily_report(url=FEED_URL, output_file=OUTPUT_FILE, limit=12):
    error = None
    try:
        xml_text = fetch_feed(url)
        items = parse_feed(xml_text, limit=limit)
    except (HTTPError, URLError, TimeoutError, ElementTree.ParseError) as exc:
        items = []
        error = exc

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(render_markdown(items, url, error), encoding="utf-8")
    print(f"Daily report generated: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Fetch AI daily report RSS feed into VitePress markdown.")
    parser.add_argument("--url", default=FEED_URL)
    parser.add_argument("--output", default=str(OUTPUT_FILE))
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()

    build_daily_report(args.url, Path(args.output), args.limit)


if __name__ == "__main__":
    main()
