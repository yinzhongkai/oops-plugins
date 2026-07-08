---
name: markdown
description: Trigger when the user asks to format Markdown (e.g. "format markdown", "格式化 markdown", "规范这个 md", "tidy up markdown", "整理 markdown 文档") or invokes /formatter:markdown. Reformats Markdown files for consistent layout, structural numbering, and Chinese punctuation without changing semantic content.
---

# Markdown 格式化

## 1. 用途

对 Markdown 文件做格式化与结构编号规范化：统一排版（标题空行、列表、代码块、表格、空行）、修正或补全章节编号、规范文件路径标注与文件列表排序。只改格式与结构，不改语义内容。

## 2. 何时使用

- 用户输入 `/formatter:markdown <文件或目录>`
- 用户用自然语言要求格式化 Markdown（如“格式化这个 md”、“规范 README”、“整理这份文档”）
- 用户在编辑 Markdown 后要求“把这份文档排整齐”

## 3. 参数

- 无参数：针对当前对话中最近提及或编辑的 Markdown 文件；无法判断时向用户询问目标文件
- 文件路径：格式化该文件
- 目录路径：递归查找并格式化目录下所有 `.md` 文件

## 4. 工作流程

1. 解析参数确定目标（单文件或目录）。目录用 Glob 递归匹配 `**/*.md`。
2. **先读取 `references/formatting-rules.md` 作为参考**，再逐个文件处理。
3. 逐个文件处理：用 Read 读取全文 → 应用下述规则 → 用 Write 写回完整文件。
4. 处理完成后汇总：列出改动文件数与每处主要改动类型，不做逐行 diff。

## 5. 核心规则

完整规则见 `references/formatting-rules.md`。**执行前务必加载该参考文件**，按其文档结构规则与排版规则逐条应用。概览：

- **1. 文档结构规则（1.1-1.4）**：章节编号层级与连续化、编号适用范围、文件路径行内代码标注、文件列表自然序排序。含子章节的文档主动为全文加编号（不区分原文是否已有编号）；非数字编号（中文序号/字母）统一转纯数字；改编号后同步更新同文件及目标目录下的跨文件引用；仅单章无子章节不加编号。
- **2. 排版规则（2.1-2.7）**：标题、列表、代码块、表格、段落/空行、行内格式、中文标点。

## 6. 行为约束

**只改格式与结构编号，不改语义内容**（不改正文措辞、不增删信息、不重排段落、不动代码块内部）。不确定时倾向不破坏原结构。完整约束见 `references/formatting-rules.md` 第 3 节。写回时用完整文件内容覆盖，避免逐行 Edit 漏掉多处空行/换行修正。

## 7. 输出

- 完成后输出汇总：共处理 N 个文件；列出每个文件的改动类型（如“补全章节编号”“统一列表符号”“表格对齐”）。不输出完整文件内容。
