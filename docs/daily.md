---
title: AI 每日日报
description: 自动订阅 AI Hot 每日日报 feed
---

# AI 每日日报

> 数据来源：[AI Hot 每日日报](https://aihot.virxact.com/feed)，最近更新：2026-06-19 08:31:10 +0000

## [我们在 Elasticsearch 上构建了一个持久化代理内存层，其召回率为0.89](https://www.elastic.co/search-labs/blog/agent-memory-elasticsearch)

`Fri, 19 Jun 2026 05:01:18 GMT`

Agent Builder 正式上市（GA）。基于 Elasticsearch 的持久化内存层将记忆分为情景、语义、程序三类，分别存入独立索引，各设不同写速率与过期规则。召回采用 BM25 与 Jina v5 稠密向量的 RRF 融合，再经交叉编码器重排序。在 168 道 QA 题评估中，R@10 平均 0.89，零跨租户泄漏。该层可通过支持 MCP 协议的客户端访问，不绑定特定运行时，已开源至 GitHub。

## [阿里开源向量数据库Zvec，UCSD黄碧薇教授提出因果AI第四代范式](https://x.com/AYi_AInotes/status/2067832098816250346)

`Fri, 19 Jun 2026 04:49:25 GMT`

阿里开源内部向量数据库Zvec，pip install zvec免费使用，对标Pinecone每月70美元能力。支持十亿向量毫秒级检索，无需单独起服务，全平台兼容；v0.5.0新增原生全文混合搜索。UCSD黄碧薇教授（causal-learn作者）提出AI四代范式：相关性小模型→因果小模型→相关性大模型（LLM）→因果大模型，认为当前正站在第四代门口。其创立的Aether AI完成首轮融资，致力于从视频中自动抽取物理规律，探索下一代因果AI范式。

## [DeepSeek研究员开源AutoResearch：AI自主跑通285B模型RL研究闭环](https://x.com/AYi_AInotes/status/2067819352926150953)

`Fri, 19 Jun 2026 03:58:46 GMT`

DeepSeek研究员Deli Chen将AutoResearch协议开源，并发布Self-play综述论文。其AI智能体首次完全自主地在DeepSeek 285B模型上完成完整RL研究闭环--从实验设计、写代码、提交GPU任务、debug到结论总结，全程零人工干预。系统调用了GRPO工具，被视为持续学习研究的开端。

## [Fable模型被美国临时关闭，AI安全管控时代来临](https://steve-yegge.medium.com/the-flat-curve-society-36c8b01eb33b)

`Fri, 19 Jun 2026 03:31:56 GMT`

美国政府短暂关闭了Mythos类中的Fable模型，标志着AI模型已越过危险门槛。作者预测最多两三代模型后，超级智能将像核武器一样被管控，大多数Fortune 500企业无法访问或仅受控使用。开源模型落后前沿约七个月，且面临算力和政府锁定的双重壁垒。人类的"辨别地平线"使许多人感觉模型进步停止，但实际指数增长未停--只是用户缺少足够困难的问题。Fable类已能解决此前Opus 4.8无法完成的复杂任务（如React客户端），AI将彻底改变编程和知识工作，但多数人只能使用当前等级模型。

## [Salesforce CodeGen教程：生成、验证并重排序Python函数（含单元测试与安全检查）](https://www.marktechpost.com/2026/06/18/salesforce-codegen-tutorial-generate-validate-and-rerank-python-functions-with-unit-tests-and-safety-checks)

`Fri, 19 Jun 2026 02:44:12 GMT`

本教程实现一个基于Salesforce CodeGen的端到端代码生成工作流。从HuggingFace加载CodeGen模型（支持350M、2B、codegen2-1B、codegen25-7b等版本），通过自然语言提示生成Python函数，随后进行函数提取、语法检查、静态安全检查、单元测试验证、best-of-N候选重排序、多步程序合成、提示词实验、基准可视化及导出。展示了CodeGen作为结构化代码生成流水线的能力，不仅完成代码补全，还能评估、筛选和组织生成结果。

## [这家韩国电信巨头是Anthropic"Mythos"争议的焦点](https://www.wired.com/story/sk-telecom-anthropic-mythos-export-controls)

`Fri, 19 Jun 2026 01:33:10 GMT`

美国政府对Anthropic最强大的AI模型Claude Mythos实施出口管制，导火索是该公司将访问权限授予韩国电信巨头SK Telecom，美方担忧SK Telecom与中国存在关联。随后亚马逊向白宫报告Mythos的公开版本Fable 5存在可被绕过的防护漏洞，加剧不信任。白宫命令Anthropic撤销所有外国国民（包括美国境内移民）对Mythos和Fable 5的访问权限，Anthropic因此完全禁用这两个模型。Mythos此前通过Project Glasswing向约150家组织开放，SK Telec

## [AI 员工 Viktor 登陆 Microsoft Teams，年化收入达 2000 万美元](https://x.com/rohanpaul_ai/status/2067755504613613699)

`Thu, 18 Jun 2026 23:45:03 GMT`

AI 员工 Viktor 在 Slack 上实现 2000 万美元年化收入（无销售团队、未大规模推广），现已正式进驻 Microsoft Teams。Viktor 定位为零门槛 AI：用户无需学习、无需提示词，像 @同事 一样提及即可获得完整工作成果，甚至无需主动 @ 也能自动完成。产品面向 Teams 的 3.2 亿用户，助力企业内部运营和管理人员零学习成本使用 AI。即日起免费试用，含 100 美元信用额度，无需绑定信用卡。

## [诺姆·沙齐尔加入OpenAI](https://twitter.com/NoamShazeer/status/2067400851438932297)

`Thu, 18 Jun 2026 20:29:15 GMT`

前Google研究员、Transformer架构共同作者诺姆·沙齐尔在X上宣布，他将加入OpenAI，并期待与那里的卓越团队合作。沙齐尔表示这是一个艰难的决定，同时对Google团队及其共同取得的成果感到无比自豪。

## [OpenAI IPO前连下两城：招揽Transformer共同作者及前白宫AI政策官员](https://techcrunch.com/2026/06/18/openai-is-bringing-on-some-big-guns-in-the-lead-up-to-its-ipo)

`Thu, 18 Jun 2026 19:59:22 GMT`

OpenAI在IPO前夕连招两位重量级人物：Google DeepMind AI先驱、Transformer架构共同作者Noam Shazeer，以及前特朗普白宫AI政策官员Dean Ball。Shazeer此前通过27亿美元收购协议重返Google，此次离职加盟OpenAI。Ball将于7月6日加入，领导新组建的Strategic Futures团队，向首席战略官Jason Kwon汇报，团队将负责前沿AI政策与内部治理，聚焦灾难性风险、递归自我改进、劳动力市场影响及前沿实验室与政府关系等议题。此举正值Anthr

## [OpenClaw 接入 OpenRouter](https://openrouter.ai/blog/tutorials/openclaw-openrouter)

`Thu, 18 Jun 2026 19:00:00 GMT`

OpenClaw 已内置 OpenRouter 支持，一条命令即可为 AI 智能体配置统一密钥、统一账单，并实现跨 300 多个模型的自动故障转移。同时提供具体设置步骤以及常见错误的修复方法。

## [Claude Code 现已支持 artifacts](https://claude.com/blog/artifacts-in-claude-code)

`Thu, 18 Jun 2026 18:54:47 GMT`

从今日起，Claude Code 可将工作进度生成为 artifacts--实时、可分享的交互式网页，涵盖 PR 走查、系统说明、仪表盘、发布清单等。artifacts 基于会话完整上下文（代码库、连接器、对话）自动构建，更新时页面原地刷新，同事即时可见。默认仅作者可见，可分享给组织内成员，由管理员通过组织层级开关和角色权限管控。内部测试中最常见用例为调试：工程师调查事件，Claude Code 分析日志并发布包含时间线、嫌疑提交和错误率图表的 artifact，团队无需再"走过场式汇报"。

## [MosaicLeaks： 你的研究智能体能保守秘密吗？](https://huggingface.co/blog/ServiceNow/mosaicleaks)

`Thu, 18 Jun 2026 18:13:13 GMT`

深度研究智能体在结合私有本地文档与外部网页检索时存在隐私泄露风险。MosaicLeaks 提出包含 1，001 条多跳研究链的新任务，每条链交错混合本地与公共子问题。测试发现智能体频繁泄露私有信息，单纯优化任务性能反而加剧泄露。基于此，研究提出隐私感知深度研究（PA-DR）强化学习训练方法，将严格链成功率从 48.7% 提升至 58.7%，同时将答案/全面信息泄露率从 34.0% 降至 9.9%。
