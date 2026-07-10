---
name: gather
description: This skill should be used when the user invokes "/inkstone:gather", asks to "采集素材", "把这个感悟采集一下", "抓取这个链接", "搜一下这个话题", "整理素材来源", "gather sources", or provides a reading-notes file path / a URL / a topic to be collected as raw material for copywriting. Collects heterogeneous sources (bookworm reading notes, web links, topics) into raw material, decides which copywriting subdirectory the output belongs to, and establishes the 选题 directory. 触发于采集阅读感悟、抓取链接、搜索话题作为文案素材时。
---

# 前采集素材

把感悟文档 / 链接 / 话题采集成原始素材，是三阶段流水线的第一步。只采集不评判、不改写素材，并决定文案归属目录、建立选题目录。

## 1. 何时使用

- 用户运行 `/inkstone:gather <素材> [选题名]`
- 用户给感悟文档路径，要求采集
- 用户给链接，要求抓取作为素材
- 用户给话题，要求搜索资料作为素材
- methodology 自动串链路时，前置触发本 skill

## 2. 输入

- **素材**（必填）：感悟文档路径 / 网址 / 话题描述，三者其一。未提供则询问用户。
- **选题名**（可选）：选题目录名。未提供则按第 5 节生成。

## 3. 识别来源类型

按素材形态分流到对应采集手法：

| 形态 | 来源类型 | 采集手法 | 详见 |
|------|---------|---------|------|
| 文件路径（.md / 含 `books/` 前缀） | book（感悟文档） | Read 读取 + 提取关键章节 | `references/from-doc.md` |
| 网址（http/https） | url（链接） | WebFetch 抓取 + 清洗正文 | `references/from-url.md` |
| 自然语言话题描述 | topic（话题） | WebSearch 搜资料 + 参考竞品 | `references/from-topic.md` |

判断不准时（如路径既是文件又像话题），向用户确认是哪种来源。每种采集手法的详细步骤、清洗规则、健壮性处理见对应 reference。

## 4. 决定文案归属

按素材路径前缀判断文案归属目录（详见 `../methodology/references/pipeline.md` 第 4 节）：

- 素材路径在 `books/<书名>/` 下 → 文案落 `copywriting/<书名>/`
- 其余位置（链接、话题、项目外文件）→ 文案落 `copywriting/<其他>/`

链接和话题无文件路径，一律落 `copywriting/<其他>/`。

## 5. 建立选题目录与命名

按归属目录建选题目录：

```
copywriting/<书名或选题>/<选题>/
```

选题目录名：

- 书来源：用书名 slug（取自 `books/` 下的目录名）。
- 非书来源：用户显式传选题名则用之；否则从链接标题 / 话题内容自动生成 slug；都没有则用 `topic-<日期>` 兜底（日期向用户确认，不在 skill 内取系统时间）。

同一选题目录已存在时，询问用户是覆盖重建还是追加采集。

## 6. 采集产物

采集本身不写 source.md（那是 organize 的职责），但在选题目录下留一份**原始素材留底**，供 organize 整理时参考：

- book：按 source.md 字段方向提取感悟文档关键章节，写入 `<选题>/raw-source.md`（大文件可只记路径，避免重复拷贝）。
- url：把清洗后的正文存到 `<选题>/raw-source.md`。
- topic：把搜索要点和竞品摘要存到 `<选题>/raw-source.md`。

留底是为了 organize 能反复参考、不必重新抓取。完成后向用户报告：来源类型、归属目录、选题目录路径、采集到的素材摘要。

## 7. 健壮性

- **感悟文档读不到**：检查路径、确认是 bookworm consolidate 产物；不是则提示用户提供感悟文档路径。
- **链接抓取失败 / 付费墙 / 反爬 / 登录墙**：报错并提示用户手动粘贴正文，不静默失败（详见 `references/from-url.md`）。
- **话题搜索无结果**：换关键词重试一两次；仍无果则向用户报告，请其细化话题或换表述。
- **来源类型识别错**：向用户确认后再采集，不臆测。

## 8. 不做什么

- 不整理成 source.md（那是 organize 的职责），只留原始素材。
- 不评判素材好不好、不改写素材内容。
- 不主动扫描 `books/` 找感悟文档——必须用户显式传路径。
- 不决定发哪个平台（那是 adapt 阶段的事）。

## 9. 参考资源

- **`references/from-doc.md`** — 感悟文档采集手法：读取 bookworm consolidate 产物的结构、提取核心观点/我的理解等关键章节、关联 framework.md 与 pre-read 的用法。
- **`references/from-url.md`** — 链接采集手法：WebFetch 抓取、正文清洗规则、付费墙/反爬/登录墙的报错与手动粘贴兜底。
- **`references/from-topic.md`** — 话题采集手法：WebSearch 搜资料、参考竞品（看别人怎么写这个话题）、搜索要点提炼。
- **`../methodology/references/pipeline.md`** — 目录约定、归属判断规则、选题命名兜底逻辑、三条铁律（第 6 节，含第 6.3 节「前后端对称扩展」：扩展新来源只在本 skill 加 `references/<来源>.md` 并登记一行）。
