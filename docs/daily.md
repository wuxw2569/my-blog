---
title: AI 每日日报
description: 自动订阅 AI Hot 每日日报 feed
---

# AI 每日日报

> 数据来源：[AI Hot 每日日报](https://aihot.virxact.com/feed)，最近更新：2026-07-07 06:50:23 +0000

## [MIRA：可玩多人世界模型，20 FPS实时生成"火箭联盟的梦"](https://aihot.virxact.com/items/cmra67abw003vihup3mg75wsc)

`Tue, 07 Jul 2026 04:22:22 GMT`

MIRA是一个可玩、多人的世界模型，被形容为"火箭联盟的梦"。它基于10k小时公开机器人收集的数据训练，学习四玩家游戏动态，根据按键实时生成画面，帧率达20 FPS。模型由General Intuition与Kyutai Labs联合构建，Epic Games提供协作。Ethan Mollick称从最早的扩散DOOM玩过来，多人20 FPS效果出色。演示、技术报告及开源代码已公开，在ICML Booth 111现场展示。 🔗 阅读原文：https://x.com/emollick/status/2074348274

## [Sysdig 澄清首例"智能体勒索软件"JadePuffer：AI 执行攻击但人类仍负责设置与选目标](https://aihot.virxact.com/items/cmr9wjj3g00jhih9kuibhf720)

`Mon, 06 Jul 2026 23:56:14 GMT`

云安全公司 Sysdig 记录了首例"智能体勒索软件"攻击 JadePuffer，AI 智能体独立完成入侵、窃取凭证、横向移动、加密超 1，300 条配置记录并撰写赎金信，还能在 31 秒内修复失败登录并以自然语言注释解释推理过程。但 Sysdig 高级威胁研究总监 Michael Clark 澄清，人类仍负责设置攻击基础设施、选择受害目标、提供通过此前入侵获取的数据库凭证。Sysdig 未能识别驱动该智能体的具体模型；AI 智能体在攻击中窃取了 OpenAI、Anthropic、DeepSeek 和 Gemini

## [Gemini Spark 可智能追踪话题实时反应](https://aihot.virxact.com/items/cmr9wgeoh00hvih9kcga5y5uj)

`Mon, 06 Jul 2026 23:52:57 GMT`

Gemini Spark 现在可以智能追踪话题并实时反应事件。 试试下一篇帖子中的提示词，在你支持的球队比赛结束后，获取定制化的比赛分析邮件。 🔗 阅读原文：https://x.com/GeminiApp/status/2074280473581572600 via AI HOT · https://aihot.virxact.com/items/cmr9wgeoh00hvih9kcga5y5uj

## [OfficeCLI：为AI智能体设计的开源Office套件](https://aihot.virxact.com/items/cmr9u2kma003gihdb8r5drdfd)

`Mon, 06 Jul 2026 23:03:34 GMT`

OfficeCLI是全球首个专为AI智能体设计的开源Office套件，以单二进制文件运行，无需安装Office或任何依赖。它内置HTML渲染引擎，可将.docx/.xlsx/.pptx转换为HTML或PNG，形成"渲染→查看→修复"的视觉闭环，使AI代理能自主创建、读取和修改Word、Excel、PowerPoint文档。支持公式、图表、条件格式、RTL布局、修订追踪、表格、数据透视表等复杂功能。提供CLI命令和基于自然语言的桌面应用AionUi，并可一键安装到Claude Code、Cursor、Windsurf

## [Claude Code v2.1.202 发布](https://aihot.virxact.com/items/cmr9u1olo002sihdbunnazaoz)

`Mon, 06 Jul 2026 22:51:16 GMT`

Claude Code v2.1.202 在 `/config` 中新增"Dynamic workflow size"设置，可控制动态工作流的 agent 数量规模（小/中/大），作为指导性建议而非硬性上限。工作流派生的 agent 现在会发射 `workflow.run_id` 和 `workflow.name` 的 OpenTelemetry 属性。修复了 mTLS 握手失败、远程控制发送命令失败、移动端发送无说明图片被静默丢弃、语音听写在麦克风故障时无限重试（改为暂停输入）、重载已有技能导致重复指令等问题。改

## [Claude Code 团队详解四种智能体循环类型](https://aihot.virxact.com/items/cmr9lm48z00u7ihe85tjkvn5t)

`Mon, 06 Jul 2026 19:08:45 GMT`

Claude Code 团队将"设计循环"定义为智能体重复工作直到满足停止条件，划分四种类型：1）回合循环--手动提示触发，Claude 自判完成，适合短任务，可通过 SKILL.md 提升验证；2）目标循环--`/goal` 手动触发，达成目标或达最大轮数停止，需确定性完成标准（如测试通过数）；3）时间循环--`/loop` 和 `/schedule` 按间隔触发，适合同步消息、检查 PR 等重复任务，可云端运行；4）主动循环--事件或计划触发，无人实时参与，每个子任务独立退出。建议从最简单方案开始，选择性使用复

## [2026年科技公司AI裁员名单：Microsoft、Oracle、GitLab等十家公司裁减数千岗位](https://aihot.virxact.com/items/cmr9kq74q00mkihe8o68fnq9t)

`Mon, 06 Jul 2026 18:35:00 GMT`

2026年以来，多家科技公司以AI为由大规模裁员。Microsoft裁减约4800岗位（2.1%），Oracle裁减21000人（13%），GitLab裁减350人（14%）以投资AI基础设施，Google Cloud持续裁减员工（外界估计1500-3000+工程师），Intuit裁减3000人（17%），Meta裁减8000人（10%）并转岗7000人至AI，Cisco裁减近4000人（5%），Cloudflare裁减1100人（20%），GM裁减500-600 IT岗位，Coinbase裁减700人（14%）。

## [Claude Fable实地指南：发现你的未知](https://aihot.virxact.com/items/cmr9jp8hl00fdihe850djojos)

`Mon, 06 Jul 2026 18:20:11 GMT`

Claude Fable是第一款要求用户主动澄清未知才能获得高质量工作的模型。与Claude Fable协作是一个在实现前后迭代发现未知的过程。通过将问题分解为已知的已知、已知的未知、未知的已知和未知的未知四类，用户可以借助Claude Fable和Claude Code进行盲点检查、头脑风暴、原型设计、实现笔记记录以及答辩解释，从而高效挖掘并解决深藏于代码库和设计与实现中的潜在问题。 🔗 阅读原文：https://claude.com/blog/a-field-guide-to-claude-fable-find

## [OpenClaw 登陆 HuggingFace 本地应用](https://aihot.virxact.com/items/cmr9jbw7a0085ihe85luucw73)

`Mon, 06 Jul 2026 17:45:30 GMT`

OpenClaw 登陆 @huggingface 本地应用 🦞🤝🤗 1. 在 hf 上挑任意 GGUF/MLX 模型 2. 复制 openclaw onboard 设置 3. Voila，你得到一个完全本地的工具调用智能体。无云端、无密钥、无人监控。 让你的 claw 本地化到极致。抵抗是徒劳的 🦞 🔗 阅读原文：https://x.com/openclaw/status/2074187998602871212 via AI HOT · https://aihot.virxact.com/items/cmr9jbw

## [SGLang 集成 DSpark 推测解码：置信度驱动的可变长度验证](https://aihot.virxact.com/items/cmr9h98co0470slsmqqc2ilv1)

`Mon, 06 Jul 2026 17:11:47 GMT`

SGLang 团队将 DSpark 推测解码算法集成到开源推理引擎中。该算法采用半自回归块起草器一次生成一组 token，并利用置信度头与顺序温度缩放（STS）为每个请求动态分配可变验证长度，从而在高负载下裁剪无效验证成本。SGLang 支持密集模型（如 Qwen3）和稀疏模型（如 DeepSeek-V4），通过全 CUDA 图处理不规则的每请求验证长度。提供三种验证模式：`static`（全长）、`compact`（生产路径）和 `cap-accept`（接受上限测量）。还引入了零开销调度、基于离线成本表的在线调

## [Google 更新隐私设置，默认用媒体数据训练 AI，用户可手动退出](https://aihot.virxact.com/items/cmr9hhq6k04anslsmg761vie9)

`Mon, 06 Jul 2026 17:04:58 GMT`

Google 于 6 月通过客户邮件低调更新了搜索服务隐私设置，新增"搜索服务历史"和"个性化推荐"两项开关，默认将用户上传的图片、文件、音频和视频录制等媒体数据保存并用于训练 AI 模型。该更新适用于搜索、地图、购物、航班、酒店、翻译、新闻等服务。用户可通过取消勾选"保存媒体"框来退出，同时可设置数据自动删除周期（3/18/36 个月）。此前独立的网络与应用活动设置不再影响搜索服务数据保留。Meta 等其他公司也在大规模收集用户媒体数据用于 AI 训练。 🔗 阅读原文：https://techcrunch.com

## [字节 Seed 发布 EdgeBench：衡量真实世界环境学习，发现新 Scaling Law](https://aihot.virxact.com/items/cmra3zy5200p0ihx88zih8ib8)

`Mon, 06 Jul 2026 16:00:00 GMT`

字节 Seed 发布超长程评测集 EdgeBench，含 134 个真实任务（覆盖六大领域），每个任务支持 Agent 持续工作至少 12 小时。基于约 38000 小时交互数据，发现 Agent 环境学习表现遵循高精度 log-sigmoid 曲线（平均 R2=0.998）；自 2025 年 9 月至 2026 年 5 月，前沿模型学习速度约每三个月翻一倍。EdgeBench 已开源 51 个任务及完整评测框架。 🔗 阅读原文：https://seed.bytedance.com/zh/blog/edgebenc
