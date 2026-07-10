---
title: AI 每日日报
description: 自动订阅 AI Hot 每日日报 feed
---

# AI 每日日报

> 数据来源：[AI Hot 每日日报](https://aihot.virxact.com/feed)，最近更新：2026-07-10 06:43:24 +0000

## [Claude Code v2.1.206 发布](https://aihot.virxact.com/items/cmreax6su01ozihyy4xtirms5)

`Fri, 10 Jul 2026 01:45:26 GMT`

Claude Code v2.1.206 发布，主要更新包括：为 `/cd` 命令添加目录路径建议；新增 `/doctor` 检查以建议修剪 CLAUDE.md 文件中模型可从代码库推导的内容；`/commit-push-pr` 现在自动允许 git push 到仓库配置的推送远程仓库；`/login` 支持 Anthropic 运营的公共网关端点；后台智能体在更新后自动升级。修复了过期登录导致所有模型报错、`claude --resume` 和 `--continue` 在启动时无键盘响应、MCP 服务器忽略 `

## [Google Research 推出 SensorFM：面向可穿戴健康数据的通用基础模型](https://aihot.virxact.com/items/cmre6wsva00lzihyym47wp98b)

`Fri, 10 Jul 2026 00:20:20 GMT`

Google Research 发布 SensorFM，一个在超过 100 万亿分钟多模态传感器数据上预训练的大规模基础模型，数据来自 500 万同意参与者，涵盖 100 多个国家及 20 余款 Fitbit 和 Pixel Watch 设备。SensorFM 学习通用的人体生理表征，可迁移至心血管、代谢、睡眠、心理健康及生活方式等 35 项健康预测任务，支持标签高效适配与数据填充，并可作为个人健康智能体的基础工具。该模型旨在解决传统可穿戴健康模型针对单一终点、难以泛化的问题。 🔗 阅读原文：https://res

## [Show HN： 如何在我的低配置电脑上运行 GLM-5.2](https://aihot.virxact.com/items/cmre3p4ne005fihrad1xjqjru)

`Thu, 09 Jul 2026 22:18:12 GMT`

colibrì v1.0 引擎以纯 C 实现、零运行时依赖，可在约 25 GB RAM 的消费级电脑上运行 744B 参数的 GLM-5.2 MoE 模型。模型经 int4 量化后磁盘占用约 370 GB，常驻内存仅 9.9 GB，通过流式加载磁盘专家实现推理。冷解码速度约 🔗 阅读原文：https://github.com/JustVugg/colibri via AI HOT · https://aihot.virxact.com/items/cmre3p4ne005fihrad1xjqjru

## [Elon Musk称赞Anthropic并承诺不切断其算力](https://aihot.virxact.com/items/cmre1vdj600h8ihwk2g9d8r99)

`Thu, 09 Jul 2026 21:57:42 GMT`

Elon Musk近日在X上承认此前对Anthropic的判断有误，称其"显然是当前AI领域的领导者"，盛赞Mythos/Fable模型"目前最好"，并承诺不会恶意切断其计算资源。2026年7月起，Anthropic成为SpaceX最大客户之一--双方5月签署协议，Anthropic以每月12.5亿美元（至2029年5月，总计约400亿美元）购买xAI旗下Colossus 1数据中心300兆瓦全部算力。Musk以特斯拉开放专利、超充网络等先例佐证其"不挤压竞争对手"的风格，合同条款也提供了保障。 🔗 阅读原文：ht

## [AI 能否回答 3 万亿美元的问题？](https://aihot.virxact.com/items/cmre1vdj600h9ihwkt35yib2l)

`Thu, 09 Jul 2026 21:47:50 GMT`

Sequoia 合伙人 David Cahn 更新 AI 基础设施支出估算：2026 年全球投入达 1.5 万亿美元，行业需产生 3 万亿美元收入才能回本。Anthropic 年化收入（ARR）达 600 亿美元，OpenAI 2025 年收入 130 亿美元（11 月称 ARR 200 亿美元），但缺口仍大。Apollo 首席经济学家指出，谷歌、Meta、微软、亚马逊均预测 2028 年自由现金流加速，但风险在于更多组织转向更便宜的开放权重模型（尤其中国模型），且 OpenAI 最新模型编码任务 token 效率

## [社交媒体AI生成内容泛滥：LinkedIn超过40%长文为AI写作](https://aihot.virxact.com/items/cmre2mjan00msihwkpuxq0462)

`Thu, 09 Jul 2026 21:46:29 GMT`

安全公司Pangram通过Chrome扩展收集超100万条帖子，分析发现社交媒体AI生成内容泛滥。整体AI检测率13.8%，长文（超250词）中25.72%完全由AI生成。LinkedIn最为严重，超40%长文帖子被标记为完全AI生成，占全部AI内容的62%；X/Twitter近一半文章（23.9%完全AI+22.9%混合）为AI写作。Reddit整体AI率仅4.4%，但顶层帖子AI率达11.6%。分析使用Pangram 3.3模型，假阳性率0.01%。Substack上长文AI率反而略低。 🔗 阅读原文：http

## [Bun 被 Anthropic 收购后用 Rust 重写，月下载超 2200 万](https://aihot.virxact.com/items/cmre2mjao00ncihwk7foifcuk)

`Thu, 09 Jul 2026 21:46:21 GMT`

Bun 于 2025 年 12 月被 Anthropic 收购，作者使用预发布版 Claude Fable 5 进行了大量 Rust 重写。Bun 最初用 Zig 在一年内构建，如今 CLI 月下载超 2200 万，被 Claude Code 等采用。广泛功能带来稳定性挑战，v1.3.14 修复了多项 use-after-free、内存泄漏等 bug。团队通过 ASAN、Fuzzilli 模糊测试等系统性预防，并借助 Rust 的内存安全特性减少此类缺陷。 🔗 阅读原文：https://bun.com/blog/b

## [微软发布Flint：面向AI智能体的可视化语言](https://aihot.virxact.com/items/cmre2mjao00nmihwkz4nz0e46)

`Thu, 09 Jul 2026 21:46:19 GMT`

微软研究院推出Flint，一种可视化中间语言，让AI智能体通过简洁的人类可编辑spec自动生成美观图表。用户只需提供数据、语义类型和图表类型，Flint编译器即可推导坐标轴、配色、布局等底层参数。支持46种图表类型，可渲染到Vega-Lite、ECharts和Chart.js三个后端。项目通过npm安装（TypeScript/JavaScript），并提供MCP服务器用于智能体工作流集成。采用弹性布局模型自动优化图表尺寸与间距，已开源。 🔗 阅读原文：https://microsoft.github.io/flin

## [Cognition 推出 SWE-1.7，接近 GPT 5.5 与 Opus 智能水平](https://aihot.virxact.com/items/cmre2mjao00nrihwkhnv9ahqj)

`Thu, 09 Jul 2026 21:46:17 GMT`

Cognition 发布迄今最强模型 SWE-1.7，基于 Kimi K2.7 基座训练，通过强化学习管线改进（基础设施、训练稳定性、数据质量、长程任务技术）实现前沿智能水平并大幅降低成本。在 FrontierCode 1.1 Main 基准上达 42.3%（Kimi K2.7 Code 为 30.1%，GPT-5.5 为 43.0%，Opus 4.8 为 46.5%），Terminal-Bench 2.1 达 81.5%，SWE-Bench Multilingual 达 77.8%。模型针对长周期异步任务优化，现

## [ChatGPT Sites将创意变可发布网站](https://aihot.virxact.com/items/cmre1bxqr00bhihwk8z3bz5qs)

`Thu, 09 Jul 2026 21:27:27 GMT`

将一个想法变成可发布和分享的实时网站 以下是OpenAI团队的一些成员用Sites构建的示例👇 @prd_008 用Sites将一个想法变成了个人专注应用： 🔗 阅读原文：https://x.com/OpenAIDevs/status/2075331020090687666 via AI HOT · https://aihot.virxact.com/items/cmre1bxqr00bhihwk8z3bz5qs

## [Google 推出 LiteRT.js：高性能 Web AI 推理运行时](https://aihot.virxact.com/items/cmre0j0vj002sihwk71qvktk7)

`Thu, 09 Jul 2026 21:21:08 GMT`

Google 发布 LiteRT.js，这是 LiteRT 跨平台边缘 AI 运行时的最新成员，专为 JavaScript 开发者设计，可直接在浏览器中运行机器学习模型。LiteRT.js 基于 WebGPU 和即将推出的 WebNN 实现 SOTA 推理性能，同时支持回退到 WebAssembly CPU 方案。 🔗 阅读原文：https://developers.googleblog.com/litertjs-googles-high-performance-web-ai-inference via AI HO

## [Anthropic发起"硬问题"倡议，邀请公众提出AI相关尖锐问题](https://aihot.virxact.com/items/cmrdslwmv06tcih4bzp5l7ivy)

`Thu, 09 Jul 2026 17:40:42 GMT`

Anthropic作为公益公司，发起"硬问题"倡议，邀请公众就AI对就业、社会、家庭、科学医学等领域的影响提出最尖锐的问题。此前已通过多种方式收集看法：首轮调查询问5.2万美国人；通过Anthropic Interviewer调查了159个国家70种语言的8.1万Claude用户；开展数十场线下焦点小组；并基于匿名真实数据研究Claude使用情况。公司还设立了Anthropic Institute和Long-Term Benefit Trust以监督公益使命进展。Anthropic承诺将公开追踪并报告针对这些问题的
