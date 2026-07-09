---
name: pre-read
description: This skill should be used when the user invokes "/bookworm:pre-read", asks to "给这一章做个预读", "这章的骨架是什么", "读这章前先给我问题", "pre-read chapter N", "preview the chapter". Produces a skeleton and guiding questions for a single chapter — gives the map but NOT the answers, so the user reads the original with questions in mind. 触发于每章读前的预读导览时。
---

# 章节预读

每读一章前，给该章的骨架 + 引导问题，带着问题去读原文。给地图不给答案。每章一次。

## 1. 何时使用

- 用户运行 `/bookworm:pre-read [章号]`
- 用户准备读某章，想要预读导览
- 用户问“这章大概讲什么结构”

## 2. 输入

- **章号**（可选）：如 `3` 或 `ch03`，作用于当前书（当前书的确定见 `../methodology/references/cycle.md` 第 4 节）。未提供章号则读 progress.md 看下一未预读章，或交互询问。

## 3. 前置检查

- 确认 `<书名>/raw/chXX.md` 存在。若无则引导拆解。
- 若存在 `framework.md`，先读它以定位本章在全书的位置。

## 4. 执行步骤

### 4.1 读本章原文

读取 `raw/chXX.md` 全文。

### 4.2 提炼骨架

给出本章的**结构骨架**——不是内容摘要，而是“这章在讲什么、分几个部分、核心论点是什么”。一句话点出本章在全书论证中的位置（引用 framework.md）。

### 4.3 生成引导问题

生成 3-5 个引导问题，供用户带着读原文。问题设计原则：

- **指向关键点但不剧透**：问题问“作者为什么认为X？”而非直接给出答案。
- **引导主动思考**：问题应让用户在读时寻找论证，而非被动接受。
- **关联前后文**：至少一个问题串联本章与前后章的关系（借 framework.md）。
- **不给答案**：问题的价值在于“带着它去原文找”，提前给答案就破坏了。

### 4.4 写 pre-read.md

产物存到 `<书名>/notes/chXX.pre-read.md`：

```markdown
# 第X章 预读

## 本章位置
<一句话：本章在全书的什么位置>

## 骨架
<本章结构，核心论点>

## 引导问题
1. <问题1，不带答案>
2. <问题2>
3. <问题3>
...
```

### 4.5 登记 progress

在 progress.md “环节记录”表追加：③ 预读 章 X 完成。

## 5. 铁律：给地图不给答案

预读的唯一目的是让用户带着问题、带着结构感去读原文。**绝不剧透本章的具体论证和结论**。若把预读写成完整摘要，用户就不读原文了——预读会变成第一根拐杖。问题要带读、不答题。

## 6. 完成后

把骨架和引导问题呈现给用户，提醒用户：**现在带着这些问题去读原文**。读时卡住可直接问（explain 会自动响应）或运行 `/bookworm:explain`。读完后运行 `/bookworm:consolidate <章号>` 巩固。

## 7. 参考资源

- **`../methodology/references/cycle.md`** — 三条铁律之一即“给地图不给答案”。
