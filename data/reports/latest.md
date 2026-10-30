# AI Daily Radar · 2026-10-31

- 时间窗：过去 24 小时
- 原始条目：18，去重后：18，应用层相关：9
- 主题：AI 应用层趋势 → 今天能做什么实践

## 2-3 个趋势

- 开发者工具正在把 AI 融入日常操作链
- Agent 化工作流从演示走向可落地任务
- 多模态创作能力继续产品化

## 今天的最小实践方案

1. 选一个与你当前工作流最接近的场景，围绕「Gemini API 的 Computer Use 工具正式开放（GA）」写下 1 个可验证的小假设。
2. 用 30 分钟做一个最小原型：输入固定样例、产出固定格式，不追求自动化闭环。
3. 记录 3 个指标：节省时间、输出质量、是否愿意明天继续用。
4. 把验证结果沉淀成一条模板或 checklist，并标注来源：Gemini API：更新日志（网页）。

## 应用层信号

1. **Cursor 披露 Claude Code VS Code 扩展被植入恶意软件事件，最多影响 5000 用户** — X：Cursor (@cursor_ai)（行业与平台）
   2026-10-30 15:46 CST
   Cursor 发现通过其 IDE 扩展市场分发的 Claude Code VS Code 扩展被修改并植入恶意软件，最多影响 5000 用户，恶意版本并非 Anthropic 开发。Cursor 已于当日下午下线扩展市场，与相关提供方合作清除恶意软件并确认无进一步风险后重新上线，建议受影响用户参考博客说明排查，并升级到 Claude Code for VS Code 2.1.314。
   https://x.com/cursor_ai/status/2116074289053175808

2. **Kimi 官方教程：如何用 Kimi K3.1 Pro 创作 3D 作品** — 公众号：月之暗面（Kimi）（技巧与观点）
   2026-10-30 12:04 CST
   月之暗面（Kimi）发布官方教程，详解 Kimi K3.1 Pro 的 3D 创作工作流程，说明参数化建模与网格化建模两种方式及对应工具选择。文章分享了 4 个案例的具体操作，包括在 Unreal Engine 中构建东方天宫、制作可 3D 打印的台灯、纯代码调用 Blender 生成建筑、用 Tripo 和 Blender 搭建微缩城市，并给出图胜于言、先搭灰模再细化等 5 个使用技巧。
   https://mp.weixin.qq.com/s?__biz=MzkzMTY4NTIyNA%3D%3D&mid=2247484364&idx=1&sn=42491c3f098deb797ee8f2a17d147b3a

3. **Gemini API 的 Computer Use 工具正式开放（GA）** — Gemini API：更新日志（网页）（产品与应用）
   2026-10-30 08:00 CST
   Google 于 10 月 30 日宣布 Gemini API 的 Computer Use 工具正式可用（GA），覆盖 Interactions 和 GenerateContent 两套 API。
   https://ai.google.dev/gemini-api/docs/changelog#10-30-2026

4. **OpenRouter 实测 Claude Opus vs Sonnet vs Haiku 5.5 该选哪个** — OpenRouter：Announcements（RSS）（技巧与观点）
   2026-10-30 08:00 CST
   OpenRouter 实测 Claude Opus 5.5、Sonnet 5.5 与 Haiku 5.5 三档模型，建议默认用 Sonnet 5.5，高频与子智能体任务用 Haiku 5.5，长且容错成本高的任务用 Opus 5.5。
   https://openrouter.ai/blog/insights/claude-opus-vs-sonnet-vs-haiku/

5. **Figma 讲解如何训练专用画布编辑模型** — Figma AI / Agent / Make（技巧与观点）
   2026-10-30 05:00 CST
   Figma 介绍其为 agent 自研 Figma 编辑模型的训练方法，先用超过 25 万条合成样本做 SFT，让早期 Llama 3.3 70B 在编辑任务上接近当时顶级模型，后转向 RL 并结合确定性校验器与视觉评委做评测。
   https://www.figma.com/blog/training-a-figma-fluent-editing-model/

6. **Pika 基于MiniMax H3后训练并开源 Pika H3 Flex 视频生成模型** — X：卡兹克 (@Khazix0918)（模型能力）
   2026-10-30 04:07 CST
   Pika Labs 在 MiniMax H3 上做后训练，推出并开源 Pika H3 Flex，采样步数从 50 步压缩到 6 步，生成时间大幅降低且质量有所提升。
   https://x.com/Khazix0918/status/2115898252004622617

7. **腾讯混元发布 Hy-Nomas 技术报告并开源 Hy-Nomas-Bench** — X：腾讯混元 (@TencentHunyuan)（产品与应用）
   2026-10-30 01:00 CST
   腾讯混元发布 Hy-Nomas 开源交互式视频世界模型的技术报告（arXiv:2610.36729），并开源 Hy-Nomas-Bench 数据集用于可复现研究。官方还用 Hy-Nomas 重现 Genie 4 示例并放出对比视频，演示无需排队即可试用，地址为 https://hy-nomas.hy.tencent.com/。
   https://x.com/TencentHunyuan/status/2115851165904814283

8. **Codex 宣布即日起 Pro 及 Business Premium 各档位用量上限翻倍** — X：Tibo (@thsottiaux)（产品与应用）
   2026-10-30 00:56 CST
   Tibo 宣布即日起将 Pro 100/200/500 档位与 Business Premium 的所有用量上限翻倍。Pro 200 的上限不会下调，Work 与 Codex 用量保持不变；dots 的扩展用量上限继续提供，且仍与默认用量分开计算，后续还会通过更好的模型和效率改进提升实际可用量。
   https://x.com/thsottiaux/status/2115850175868727621

9. **Gemini 新增文档、PDF、演示文稿和表格的直接生成、预览与编辑功能** — X：Gemini (@GeminiApp)（产品与应用）
   2026-10-30 00:36 CST
   Google Gemini 宣布可直接在应用内生成、预览和编辑文档、PDF、演示文稿、表格等多种文件。支持把手写笔记转成 PDF 学习指南、手动调整内容、高亮部分让 Gemini 修改文字或视觉元素，并可继续追问。
   https://x.com/GeminiApp/status/2115845164824711247


## 后续推送接口预留

- 邮件：把本文件内容作为纯 Markdown 邮件正文发送。
- Telegram：把趋势和最小实践方案截短为消息摘要，附上本地报告路径或仓库链接。
- 飞书：把本文件 Markdown 转成云文档或群消息。
- Obsidian：把 `data/reports/latest.md` 同步到 vault 的 Daily Notes 目录。

## 生成说明

- 生成时间：2026-10-31 00:10 CST
- 数据来自 AI HOT 精选条目。
- Prompt：`prompts/ai_daily_radar.md`
