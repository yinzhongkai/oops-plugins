---
name: framework
description: This skill should be used when the user invokes "/bookworm:framework", asks to "梳理全书框架", "提炼全局结构", "全书在讲什么", "全书的根本问题", "build the book framework", "overview the whole book". Reads all chapters and produces a global view — the fundamental question the book answers, the argument arc, and the logical relationships between chapters. 触发于建立全书全局框架时。
---

# 全书框架

读全部章节，提炼全书在回答什么根本问题、论证脉络、章节间逻辑关系。先有全局地图再深入细节。每本书一次。

## 1. 何时使用

- 用户运行 `/bookworm:framework [书名]`
- 用户要求梳理全书结构、提炼全局视角
- 拆解完成后，用户想知道全书在讲什么

## 2. 输入

- **书名**（可选）：不带则按"确定当前书"规则定位（见 `../methodology/references/cycle.md` 第 4 节）。再读取其 raw/ 目录。

## 3. 前置检查

- 确认 `books/<书名>/raw/` 存在且非空。若未拆解，引导用户先运行 `/bookworm:disassemble`。

## 4. 执行步骤

### 4.1 分批顺序读取全部章节

**单 agent 顺序读 + 分批策略**（不并行）：读 3-4 章后做阶段性小结，再读下一批。边读边累积全局感，使提炼更准确。避免并行子 agent——它们缺乏全局视野，且 framework 的难点在“合”不在“分”。

### 4.2 提炼全局框架

在通读基础上回答：

1. **根本问题**：全书在回答什么核心问题？要解决什么？
2. **论证脉络**：作者如何展开论证？从哪里出发、经过哪些转折、到达何处？
3. **章节关系**：各章之间的逻辑关系——递进、并列、总分、对比？画出章节间的依赖与衔接。
4. **核心概念图谱**：全书反复出现的关键概念及其关系（如《聪明的投资者》的市场先生、安全边际、防御型/进攻型投资者）。

### 4.3 写 framework.md

产物存到 `books/<书名>/framework.md`，结构：

```markdown
# 《书名》全局框架

## 根本问题
<一句话核心问题 + 展开说明>

## 论证脉络
<作者的论证主线，可含阶段划分>

## 章节关系
| 章 | 标题 | 在全书的位置 | 与前后章的逻辑 |
|----|------|-------------|----------------|
| 1 | ... | 起点 | 引出XX |
| ... |

## 核心概念图谱
<关键概念及其关系>
```

### 4.4 登记 progress

在 progress.md “环节记录”表追加：② 全局框架完成。

## 5. 注意

- **framework 是地图不是摘要**：提炼结构和脉络，不逐章复述内容。详细内容留给预读和精读。
- **全局视角先行**：这正是“先有全局视角再深入细节”的体现。后续 pre-read 和 explain 引用本文件来定位单章在全书的位置。
- **大书**：若章节数多导致读取量大，分批策略已覆盖；仍卡顿可只读每章首尾段做粗框架，但须告知用户做了简化。

## 6. 完成后

向用户展示 framework.md 摘要（根本问题 + 章节关系），并提示下一步：每读一章前运行 `/bookworm:pre-read <章号>`，带着问题读原文。

## 7. 参考资源

- **`../methodology/references/cycle.md`** — 闭环顺序、目录约定、progress.md 结构。
