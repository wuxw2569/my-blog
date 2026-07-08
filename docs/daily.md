---
title: AI 每日日报
description: 自动订阅 AI Hot 每日日报 feed
---

# AI 每日日报

> 数据来源：[AI Hot 每日日报](https://aihot.virxact.com/feed)，最近更新：2026-07-08 05:49:52 +0000

## [AI 审计代理在 Cloudflare CIRCL 中发现 7 个漏洞](https://aihot.virxact.com/items/cmrblfb8a050sihl1484pa3wo)

`Wed, 08 Jul 2026 04:29:33 GMT`

zkSecurity 的 AI 审计代理 zkao 持续扫描 Cloudflare 的 CIRCL 密码学库，使用 Opus 4.6 + skills 和 GPT-5.3 + skills 等模型发现并确认了 7 个真实漏洞。其中包括阈值 RSA 中 float64 精度丢失（AI 自评 Critical）和属性基加密（CP-ABE）访问控制完全失效（Critical，由 zkao 自行发现）。所有漏洞已在上游修复，多数在 HackerOne 上获得确认和奖励。AI 生成的候选发现仍需人工验证，但 zkao 已能自

## [美国商务部批准OpenAI大规模发布GPT-5.6，Sol明日亮相](https://aihot.virxact.com/items/cmrbkf2e804qlihl1e8qe5q4a)

`Wed, 08 Jul 2026 03:30:52 GMT`

美国商务部正式批准OpenAI大规模发布GPT-5.6。OpenAI宣布GPT-5.6 Sol将于本周四完成最后准备后，与Terra和Luna一同面向公众推出。此前因国家安全考量，美国政府要求分阶段发布，仅允许向经批准的有限实体开放。此次全面放行标志着临时管控结束。获批前，美国商务部下属AI标准与创新中心执行了测试，OpenAI技术团队驻扎华盛顿配合沟通。美国最新AI行政令即将出台，旨在为先进AI模型发布建立正式评估框架。 🔗 阅读原文：https://www.ithome.com/0/973/922.htm vi

## [蚂蚁集团旗下Robbyant开源LingBot-Vision：1B参数边界中心视觉基础模型，用于密集空间感知](https://aihot.virxact.com/items/cmrbikwbz04b5ihl16qfp5ntw)

`Wed, 08 Jul 2026 03:03:22 GMT`

蚂蚁集团旗下具身智能公司Robbyant开源LingBot-Vision，一套自监督视觉Transformer家族，专为密集空间感知设计。旗舰ViT-g/16参数约1.1B，采用掩膜边界建模训练，将边界作为原生预训练信号。在密集空间任务中，该1B模型匹配或超越参数规模高达7倍的大模型（如7B DINOv3）。模型以Apache-2.0许可证在Hugging Face开源，提供ViT-g、ViT-L（300M）、ViT-B（86M）、ViT-S四个规模。 🔗 阅读原文：https://www.marktechpost

## [Pulpie：用于清理网络的Pareto最优模型](https://aihot.virxact.com/items/cmrbez8y903b9ihl133b5wr18)

`Wed, 08 Jul 2026 01:33:24 GMT`

Pulpie是一族Pareto最优模型，用于从HTML页面提取主要内容。其最小模型pulpie-orange-small（210M参数）在WebMainBench上取得0.862的ROUGE-5 F1分数，接近600M参数的Dripper（0.864），但成本仅1/20。在NVIDIA L4 GPU上，Pulpie处理速度13.7页/秒，Dripper仅0.68页/秒。清理10亿页HTML，Pulpie成本约$7，900，Dripper需$159，000。模型采用编码器架构，单次前向传播即可标记每个HTML块为内容

## [Claude开发者分享两种多智能体模式：Advisor和Orchestrator](https://aihot.virxact.com/items/cmrbdqlcv02y4ihl11xbxx9xs)

`Wed, 08 Jul 2026 01:06:01 GMT`

Claude开发者官方分享团队高频使用的两种多智能体模式。Advisor模式：Sonnet 5作为执行者，通过tool call调用Fable 5获取指导。SWE-bench Pro（482题）上，Sonnet 5单独75.5%/$0.75，加顾问达84%/$1.40，Fable 5单独91.5%/$2.25；组合方案约92%性能、63%成本。Orchestrator模式：Fable 5作为编排者规划并向多个Sonnet 5 worker扇出任务。BrowseComp上，全Sonnet 5 77.8%/$16.01

## [蚂蚁集团周俊AICon演讲：从Token数量到Token密度，万亿参数模型效率优先](https://aihot.virxact.com/items/cmrbdsefa02yjihl17gg7mhx3)

`Wed, 08 Jul 2026 01:00:00 GMT`

蚂蚁集团副总裁周俊在AICon演讲指出，万亿参数模型每运行15分钟算力成本约等于一辆特斯拉，效率是智能体时代最需解决的问题。团队提出从"更多Token"转向"更高Token密度"策略，采用7份Lightning Attention加1份MLA的混合线性注意力架构，使256K长上下文成本从指数级降至线性级，算力更多用于思考。通过Kpop算法区分工具调用与自然语言Token，结合思维链剪枝、自蒸馏等，Token输出减少约4倍而能力不降。在LongBench、BFCL等基准上提升显著，千亿参数模型在Agent任务中超越部

## [《人生设计课》Prompt实测：用Claude设计人生的四个阶段](https://aihot.virxact.com/items/cmrbc048n02j2ihl1all0ymge)

`Wed, 08 Jul 2026 00:12:06 GMT`

作者将斯坦福《人生设计课》理论体系制成Prompt，通过Claude逐步提问、追问和分析。Prompt融合设计思维、心流理论和积极心理学，分为看清现状、找到指南针、寻路、制定奥德赛计划四阶段，主线问题控制在6到9个。AI引导用户给健康、工作、娱乐、爱打分，区分重力问题与可设计的真问题，生成三个五年人生版本，最终输出8000至12000字的《个人人生设计蓝图》。作者实测效果超预期。 🔗 阅读原文：https://mp.weixin.qq.com/s/VDlBdkspV0SQNFJYLxOogQ via AI HOT 

## [Krea 2 身份保留功能上线](https://aihot.virxact.com/items/cmrb4j2zx00n4ihl14u6xv7kz)

`Tue, 07 Jul 2026 20:22:46 GMT`

Krea 2 的身份保留功能已发布，配套模型和 ComfyUI 节点也已上线。🔥 🔗 阅读原文：https://x.com/krea_ai/status/2074589965653303321 via AI HOT · https://aihot.virxact.com/items/cmrb4j2zx00n4ihl14u6xv7kz

## [Meta Superintelligence Labs 推出 Muse Image 和 Muse Video](https://aihot.virxact.com/items/cmrb2mxmc0072ihl1mx0aw1bz)

`Tue, 07 Jul 2026 19:33:53 GMT`

Meta Superintelligence Labs 发布首个媒体生成模型 Muse Image 和 Muse Video。Muse Image 是目前最先进的图像生成模型，能精确遵循指令、精准编辑、多参考构图，并利用 Instagram 社交上下文。它还具备智能体工具使用能力并集成 Muse Spark。用户可通过 Meta AI 应用、网页、Instagram Stories 和 WhatsApp 试用，初始限于部分国家。Muse Video 基于相同预训练基础，实现高视觉保真度并原生支持音频。 🔗 阅读原文

## [微软为降成本在Copilot中用自研MAI模型替换OpenAI和Anthropic模型](https://aihot.virxact.com/items/cmrb0u6pv02qtihogovduu795)

`Tue, 07 Jul 2026 18:35:58 GMT`

微软正用自研MAI模型替换Copilot产品中的OpenAI和Anthropic模型以降低支出。MAI模型已在Excel和Outlook中每周处理数万次请求，但占比仍小。Build大会上发布推理模型MAI-Thinking 1，声称编码媲美Sonnet 4.6和Opus 4.6，但基准测试大幅落后，仅与DeepSeek V3.2相当。AI负责人承认目标是削减并消除对Anthropic的支出。CEO暗示未来可能按用量计费，MAI为默认，第三方模型付费附加。微软称MAI使用干净商业许可数据，实际基于Common Cra

## [YC CEO声称每日用AI部署3.7万行代码，开发者审查发现前端代码大量臃肿低效](https://aihot.virxact.com/items/cmrayv5ja0293ihog3rixaqua)

`Tue, 07 Jul 2026 17:52:12 GMT`

Y Combinator CEO Garry Tan在X上宣称，他与AI编码代理每天在五个项目中部署37000行代码，并保持连续72天发布记录。波兰开发者Gregorein深入审查Tan网站前端代码，发现大量臃肿与低效问题：页面加载169次请求、总计6.42MB数据（对比Hacker News仅7次12KB）；包含28个测试文件、78个未使用的JavaScript控制器、八种格式Logo（含空文件）、未压缩的旧PNG等。Gregorein指出，AI虽能快速生成代码，但质量仍应优先于数量。 🔗 阅读原文：https:

## [NotebookLM短视频概览正式上线](https://aihot.virxact.com/items/cmray36fg021nihogfo205417)

`Tue, 07 Jul 2026 17:48:50 GMT`

短视频概览功能已正式在移动端和网页端面向所有英语用户全面上线！ 一如既往，您的意见对我们至关重要。请在下方分享您最喜欢的作品，并告诉我们接下来需要添加哪些功能！❤️ 🔗 阅读原文：https://x.com/NotebookLM/status/2074551227594264799 via AI HOT · https://aihot.virxact.com/items/cmray36fg021nihogfo205417
