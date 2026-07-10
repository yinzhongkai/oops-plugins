---
name: adapt
description: This skill should be used when the user invokes "/inkstone:adapt", asks to adapt content for a specific platform (e.g., "改成公众号文案", "适配知乎", "写成小红书笔记", "改造成平台文案", "适配 <平台>", "adapt for WeChat/Zhihu/Xiaohongshu"), or when source.md is confirmed and a target platform is specified.
---

# 后适配平台

把确认过的 source.md 中间格式，按指定平台风格规范改造成平台文案，是三阶段流水线的第三步。只适配不改义，每次只产一个平台，由用户指定。

## 1. 何时使用

- 用户运行 `/inkstone:adapt <平台>`
- 用户说「改成公众号 / 适配知乎 / 写成小红书笔记」
- source.md 已确认，用户指定目标平台
- methodology 自动串链路时，organize 确认后触发本 skill

## 2. 输入

- **平台**（必填）：公众号 / 知乎 / 小红书。未指定则询问用户。每次只产一个平台。
- **选题**（可选）：定位 source.md。未提供则询问或列出 `copywriting/` 下有 `source.md` 的选题供选。

## 3. 前置检查

- 确认选题目录有 `source.md` 且**已经用户确认**。未确认则提示先回 `/inkstone:organize` 确认——不在未确认的中间格式上适配（铁律，见 `../methodology/references/pipeline.md` 第 6 节）。
- 读取 source.md，确认核心观点字段非空。核心观点缺失则不进适配，回 organize 补。

## 4. 平台路由

按用户指定平台加载对应风格规范：

| 平台 | 风格规范文件 | 产出文件 |
|------|-------------|---------|
| 公众号 | `references/wechat.md` | `<选题>/wechat.md` |
| 知乎 | `references/zhihu.md` | `<选题>/zhihu.md` |
| 小红书 | `references/xiaohongshu.md` | `<选题>/xiaohongshu.md` |

本表即后端平台登记表——新增平台时在此加一行 + 加 `references/<平台>.md`（详见 `../methodology/references/pipeline.md` 第 6.3 节「前后端对称扩展」）。

执行适配前**必读**对应平台的 reference——它定义该平台的标题/结构/语感/排版/标签等全部规范。SKILL.md 只讲公共工作流，平台差异全在各 reference。

## 5. 公共适配工作流

所有平台共用这套工作流，平台差异体现在各步骤的具体做法（详见各 reference）：

1. **读 source.md**：核心观点为主轴，关键论据素材为血肉，可引用金句为抓手，受众定语气，备注守禁忌。
2. **选结构**：按平台规范搭骨架（如公众号长文结构、知乎论证递进、小红书短平快）。
3. **填内容**：把素材填进结构，按平台详略取舍。严守「改造而非创作」——不编 source.md 里没有的论据和观点，素材不足处诚实标注或回退。
4. **调语感**：套平台语感（详见 `../methodology/references/pipeline.md` 第 7 节中文语感基准 + 各平台 reference 的调性）。默认自然口语化中文，避免 AI 腔。
5. **加平台要素**：标题钩子、排版、标签等平台特有要素（各 reference 详述）。
6. **产出文件**：写入 `<选题>/<平台>.md`。

## 6. 改造而非创作

adapt 的输入是 source.md，输出是适配调性的文案。铁律（见 `../methodology/references/pipeline.md` 第 6 节）：

- 核心观点不得偏离 source.md 已确认的主轴。
- 不编造 source.md 里没有的论据、数据、案例。需要更多素材时回 gather/organize 补，不在 adapt 里编。
- 可引用金句用 source.md 里的；链接/话题来源的金句注意版权与转述（source.md 备注应已标注）。
- source.md 备注里的「待深入」「禁忌」点，adapt 时严守——不强行展开标注的「待深入」点、不触碰标注的禁忌。

## 7. 完成后

- 文案写入 `<选题>/<平台>.md`。
- 向用户展示文案，报告路径。
- 提示：可继续 `/inkstone:adapt <另一平台>` 产出其他平台版本（同一 source.md 一鱼多吃，逐个产）。
- 不自动连续产出多平台——每次只产用户指定的一个。

## 8. 不做什么

- 不在未确认的 source.md 上适配。
- 不一次产出多平台（每次只产用户指定的一个）。
- 不编造 source.md 里没有的素材。
- 不回原始素材重新采集（那是 gather 的事）。
- 不修改 source.md（中间格式已确认，adapt 只消费）。

## 9. 参考资源

- **`references/wechat.md`** — 公众号适配规范：标题钩子、正文结构、金句点睛、排版。
- **`references/zhihu.md`** — 知乎适配规范：开头破题、论证层次、专业感、引用。
- **`references/xiaohongshu.md`** — 小红书适配规范：首图标题、正文节奏、emoji+话题标签、钩子。
- **`../methodology/references/pipeline.md`** — 中间格式契约（第 5 节）、中文语感基准（第 7 节）、三条铁律（第 6 节，含第 6.3 节「前后端对称扩展」：扩展新平台只在本 skill 加 `references/<平台>.md` 并登记一行）。
