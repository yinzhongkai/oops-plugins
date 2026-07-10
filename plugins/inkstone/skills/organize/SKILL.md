---
name: organize
description: This skill should be used when the user invokes "/inkstone:organize", asks to "整理成中间格式", "整理素材", "把素材整理一下", "生成 source.md", "转成 source.md", "确认中间格式", "organize the material", or when gather has finished and the next step is to normalize raw-source.md into the unified source.md intermediate format.
---

# 整理素材（organize）

把 gather 采集的异构原始素材整理成统一中间格式 source.md，是三阶段流水线的第二步。只整理不创作、不针对任何平台。整理完必须经用户确认才进 adapt。

## 1. 何时使用

- 用户运行 `/inkstone:organize [选题名]`
- gather 采集完成后，自动衔接触发
- methodology 自动串链路时，前置阶段跑完触发本 skill
- 用户已有 raw-source.md，要求整理成 source.md

## 2. 输入

- **选题名 / 选题目录**（可选）：定位要整理的选题。未提供则询问用户，或列出 `copywriting/` 下有 `raw-source.md` 但无 `source.md` 的选题供选。

## 3. 前置检查

- 确认选题目录存在、且有 `raw-source.md`（gather 的留底）。无则提示用户先跑 `/inkstone:gather`。
- 读取 `raw-source.md`，识别来源类型（frontmatter 的 `来源类型` 字段：book / url / topic）。
- 若选题目录已存在 `source.md`，询问用户是覆盖、追加还是取消，不擅自覆盖。

## 4. 整理成 source.md

按 `../methodology/references/pipeline.md` 第 5 节的中间格式契约，把 raw-source.md 的内容归一成 source.md 字段。整理规则见 `references/normalize.md`，要点：

| source.md 字段 | 整理方式 | 来源 / 取值规则 |
|----------------|---------|----------------|
| frontmatter | 选题、来源类型、来源路径或链接、整理时间 | 选题与来源类型取自 raw-source.md frontmatter；来源路径/链接按原始素材形态记录；整理时间由用户提供或交互确认，**不在 skill 内取系统时间**。 |
| 核心观点 | 浓缩成一句话主轴；话题来源观点缺失时标注待用户确立 | 优先从 raw-source.md「提取要点 → 核心观点」归纳。 |
| 关键论据素材 | 归纳支撑观点的论据、数据、例子 | 取自 raw-source.md「提取要点 → 关键论据素材」。 |
| 可引用金句 | 挑出适合直接用的原句/感悟 | 取自 raw-source.md「提取要点 → 可引用金句」。 |
| 受众 | 从素材推断；推断不出则标注待补 | 感悟文档通常缺失，链接/话题可推断。 |
| 备注 | 风格倾向、禁忌、平台倾向建议、待深入点 | 感悟文档带入「待深入」；链接/话题加原创性提醒。 |

整理时遵循「改造而非创作」铁律：只归纳提炼素材里已有的信息，不编造素材里没有的论据和观点。素材不足的字段标注「待补」，不强填。

## 5. 来源差异处理

三种来源整理侧重不同（详见 `references/normalize.md`）：

- **book（感悟文档）**：素材已是结构化表达，核心观点通常清晰。重点是浓缩主轴、提炼金句、带入「待深入」标注。
- **url（链接）**：素材是别人内容。重点标注原创性提醒，核心观点须是用户基于素材的再表达，勿照搬原文主张。
- **topic（话题）**：信息最少，核心观点常缺失。重点是把各方观点和竞品角度呈现给用户，请用户在确认时确立自己的核心观点与差异化定位。

## 6. 展示并等用户确认（铁律）

整理完 source.md 后，**必须展示给用户确认/编辑后才能进 adapt**。这是三条铁律之一（见 `../methodology/references/pipeline.md` 第 6 节）：

1. 把整理好的 source.md 完整展示给用户。
2. 明确请用户确认或修改：「以上是整理出的中间格式，请确认或修改。确认后我再按你指定的平台适配。」
3. 用户确认前不进 adapt。methodology 自动串链路时也在此停下等用户。
4. 用户修改则更新 source.md 后再确认；用户补充信息（如确立话题的核心观点）则并入对应字段。

确认这一步是质量分水岭——把中间格式的把关权交给用户，避免在错的素材基底上适配出三个平台的废稿。

## 7. 完成后

用户确认后：

- source.md 落盘到 `<选题>/source.md`。
- 向用户报告：source.md 路径、核心观点摘要、提示下一步 `/inkstone:adapt <平台>`。
- 不主动进 adapt——是否适配、适配哪个平台由用户决定（目标平台在 adapt 阶段定，不写进 source.md）。

## 8. 不做什么

- 不针对任何平台整理（那是 adapt 的职责），source.md 是平台无关的。
- 不写平台文案。
- 不替用户确立话题的核心观点（呈现各方观点请用户定）。
- 不跳过用户确认直接进 adapt。
- 不编造素材里没有的论据和观点。

## 9. 参考资源

- **`references/normalize.md`** — 三种来源的整理规则、字段缺失处理、话题来源确立观点的引导话术、source.md 完整模板。
- **`../methodology/references/pipeline.md`** — 中间格式契约（第 5 节）、三条铁律（第 6 节）、目录约定。
