---
title: AI 每日日报
description: 自动订阅 AI Hot 每日日报 feed
---

# AI 每日日报

> 数据来源：[AI Hot 每日日报](https://aihot.virxact.com/feed)，最近更新：2026-07-05 06:40:16 +0000

## [26000名学生研究显示AI隐藏学习成本需两年才显现](https://aihot.virxact.com/items/cmr65ieko002tslf0xiomac0c)

`Sat, 04 Jul 2026 09:08:41 GMT`

一项追踪26000名7-12年级中学生30个月的面板数据研究发现：使用AI后作业分数提升18%，完成时间从64分钟降至45分钟，但闭卷考试分数下降20%，升学考试成绩下降18%至24%，且完全影响约两年才显现。81%长期用户作业完成时间低于50分钟（外包迹象）。社会学科下降27%，STEM下降22%，英语下降17%，语文下降9%。每周使用AI一小时损失约5%，五小时损失30%。早期损失从约25%降至16%但未消失。 🔗 阅读原文：https://the-decoder.com/a-26000-student-stu

## [NVIDIA 联合多所大学提出 ASPIRE：自我改进机器人框架，零样本成功率最高提升 77 分](https://aihot.virxact.com/items/cmr5zuihg0739slc7nv4mlc5r)

`Sat, 04 Jul 2026 06:32:47 GMT`

NVIDIA 联合密歇根大学、UIUC、UC Berkeley 等提出 ASPIRE，一个持续学习机器人框架。它通过协调器-执行器架构、闭环执行引擎、技能库和进化搜索，编写并优化机器人控制程序。编程智能体使用 Claude Code（Claude Opus 4.6，1M token 上下文窗口）。在 LIBERO-Pro 上最高比最强基线提升 77 分；Robosuite 双手交接成功率从 20% 提升至 92%；BEHAVIOR-1K 收音机拾取任务从 56% 提升至 88%。利用 LIBERO-90 积累的技能

## [我国研制全球首款基于可控存内计算的忆阻器神经动力学芯片](https://aihot.virxact.com/items/cmr5wizx2067eslc7xynzcf9y)

`Sat, 04 Jul 2026 05:01:02 GMT`

北京大学集成电路学院联合中科院上海微系统所，发布全球首款基于可控存内计算的忆阻器神经动力学芯片，首次将单步运算时延压缩至2.12毫秒。芯片采用40纳米工艺，存内计算阵列与外围电路总面积0.28平方毫米，运行频率50 MHz，单步积分仅需9级流水。在脑皮层重建等任务中较当前GPU提速50至478倍，突破神经动力学实时计算瓶颈。相关成果7月3日发表于《科学》。 🔗 阅读原文：https://www.ithome.com/0/972/526.htm

## [pxpipe：通过图像化压缩输入token降低Claude Code成本](https://aihot.virxact.com/items/cmr5cef1q017islc779xjrcy6)

`Fri, 03 Jul 2026 19:19:45 GMT`

pxpipe是一个本地代理，将系统提示、工具文档和历史记录等密集文本渲染为PNG图像，利用图像token成本取决于像素尺寸的特性压缩输入token。在Fable 5模型上，约25k文本token压缩为约2.7k图像token，端到端账单降低59-70%。SWE-bench Lite 10个实例全部通过，成本从$54降至$27；SWE-bench Pro 19对测试中18对判定一致，单次请求成本降低约60%。该方法有损（精确ID等需保持文本），默认仅处理`claude-fable-5`请求，可通过`PXPIPE_MO

## [Fable 的判断力：Simon Willison 从 Claude Code 团队获得的效率技巧](https://aihot.virxact.com/items/cmr5blxyu00ykslc7kiaaxqam)

`Fri, 03 Jul 2026 18:51:06 GMT`

Simon Willison 在 AIE 上与 Claude Code 团队交流后建议，让 Fable（以及 Opus）用自己的判断力工作，而非硬性规定行为。例如，直接让 Fable 自行决定何时编写测试，比给出具体规则更好。为应对价格即将上涨、节省 Fable token，Jesse Vincent 的另一个技巧是告诉 Fable 将较小任务委托给较低功耗模型（Sonnet 用于实质性实现、Haiku 用于机械修改），主循环保留判断、审计和数据合成等任务。Willison 已将提示词存入 Claude Code 

## [藏师傅PPT与Pencil结合使用技巧](https://aihot.virxact.com/items/cmr4wyzef05r3sll5oxo52f8j)

`Fri, 03 Jul 2026 12:25:20 GMT`

用户将藏师傅的AI生成PPT导入Pencil设计软件，可在Pencil中一次性浏览所有页面并手动调整AI常见的排版问题，如元素重叠、对齐不准、字体错误。Pencil提供比PPT更强的编辑能力（对齐、嵌套、打组），支持导出网页和编辑文件，也可导出PNG后直接放入PPT演示。这种工作流昨天经朋友分享验证，大幅提升AI生成内容的可编辑性。 🔗 阅读原文：https://x.com/op7418/status/2073020264083050811

## [全球首例 AI Agent 勒索攻击曝光，从漏洞利用到数据库加密全程自主完成](https://aihot.virxact.com/items/cmr4w2clt05kasll56e54tanx)

`Fri, 03 Jul 2026 11:57:00 GMT`

安全厂商 Sysdig 首次记录到 AI Agent"JADEPUFFER"自动完成的勒索攻击。攻击利用暴露的 Langflow 服务漏洞 CVE-2025-3248 远程执行 Python 代码，随后自主收集 OpenAI、Anthropic、DeepSeek、Gemini 等 API 密钥及阿里云、腾讯云、华为云、AWS、Google Cloud、Azure 等云平台凭证，通过 MinIO 默认密码访问对象存储并创建每 30 分钟连接的计划任务。横向移动到 MySQL 和 Nacos 服务器，利用数据库 Roo

## [生数科技发布 Vidu S1，推动视频生成迈向"实时交互"新时代](https://aihot.virxact.com/items/cmr53vzsc07l3sll5x8mfscz3)

`Fri, 03 Jul 2026 11:17:47 GMT`

7月3日，生数科技在2026全球数字经济大会上发布Vidu S1实时交互模型，支持实时视频通话和语音控制视频走向，实现无限时长连续互动。模型采用自回归扩散路线，基于已生成画面和语音指令持续预测后续内容；无需传统建模，一张图片即可创建角色并自定义音色。Vidu S1在540P分辨率下实现25FPS（最高42FPS）实时生成，通过TurboDiffusion等技术降低计算成本，已开启内测。 🔗 阅读原文：https://mp.weixin.qq.com/s/RuukpnoOA2tI0ERCNrLgtQ

## [JoyAI App 上线 UGC 数字人功能，用户可"捏"出专属虚拟玩伴](https://aihot.virxact.com/items/cmr53w14307lfsll5fo2cq53p)

`Fri, 03 Jul 2026 10:03:25 GMT`

JoyAI App 近日上线 UGC 数字人功能，用户只需上传一张照片即可生成专属虚拟数字分身，支持一键复刻写实形象或通过模板重塑为卡通风格，搭配用户自己的语音即可解锁专属陪伴。该功能复用"万能博士"技术底座，集成 JoyAI 语言、语音、数字人大模型，实现行业领先的全双工对话，支持随时打断、自然接话。数字人兼具情绪陪伴与全能助手属性，可提供点外卖、金融咨询、学英语、规划行程等生活服务。 🔗 阅读原文：https://mp.weixin.qq.com/s/XfpxdblzNWa5HxahRoT9pg

## [面向 Web 开发者的 Safari MCP 服务器](https://aihot.virxact.com/items/cmr4s179804l5sll5u47j7031)

`Fri, 03 Jul 2026 09:59:42 GMT`

Safari Technology Preview 247 推出 Safari MCP 服务器，基于 Model Context Protocol，允许任何 MCP 兼容客户端连接 Safari 浏览器窗口。智能体可获取 DOM、网络请求、截图、控制台输出等信息，自主完成调试、性能分析、可访问性检查等任务。内置 `browser_console_messages`、`screenshot`、`evaluate_javascript`、`list_network_requests` 等工具。开发者安装后启用"远程自动

## [国家网信办就《互联网信息服务管理办法》再次征求意见，首设"智能信息服务"专章规范AI服务](https://aihot.virxact.com/items/cmr4rs02404h6sll50myozvz0)

`Fri, 03 Jul 2026 09:15:08 GMT`

7月3日，国家互联网信息办公室就《互联网信息服务管理办法（修订草案征求意见稿）》再次公开征求意见。草案新增"智能信息服务"专章，要求AI服务提供者公示技术基本原理、训练数据来源，对生成合成内容进行标识，禁止强制用户使用智能服务或利用算法扰乱网络舆论。草案还强化用户账号管理，明确对超过6个月不登录账号可依约注销；要求平台建立网络暴力信息特征库，提供屏蔽、禁止转载等防护选项。意见反馈截止8月2日。 🔗 阅读原文：https://www.ithome.com/0/972/341.htm

## [面壁智能发布AI全自动预训练框架ForgeTrain，8小时追平Megatron-LM](https://aihot.virxact.com/items/cmr4righa04d8sll54465w8z3)

`Fri, 03 Jul 2026 09:12:17 GMT`

面壁智能发布全球首个完全由AI编写、无人类干预的生产级大模型预训练框架ForgeTrain。该框架针对特定模型和硬件从零自动"锻造"专用训练代码。基准测试显示，ForgeTrain在8小时内追平Megatron-LM，1.5至2天内实现稳定反超，模型FLOPS利用率提升约8%~10%，且可迁移至不同模型（MiniCPM4-0.5B/8B）和硬件（H100及昇腾NPU）。其采用四阶段Harness优化流程，全程自动判定。面壁智能将其工程思想概括为Forge Engineering。 🔗 阅读原文：https://mp
