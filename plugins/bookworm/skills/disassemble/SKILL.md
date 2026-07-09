---
name: disassemble
description: This skill should be used when the user invokes "/bookworm:disassemble", asks to "拆解这本书", "把书拆成章节", "导入一本书", "拆分原文", "parse the book into chapters", or provides a book file path to be split into chapters. Splits a whole book (txt/md/PDF/EPUB) into per-chapter markdown files under <project>/<book-name>/raw/, copying the original file and registering progress. 触发于拆解整本书原文、按章节存档时。
---

# 拆解整本书

把整本书原文按章节切分存档，是五环节闭环的第一步。每本书只需做一次。

## 1. 何时使用

- 用户运行 `/bookworm:disassemble <原文路径> <书名>`
- 用户提供书文件路径，要求拆解成章节
- 用户说“我要开始读这本书”并给出原文文件

## 2. 输入

- **原文路径**（必填）：书文件路径，支持 txt / md / pdf / epub。未提供则询问用户路径。
- **书名**（必填）：中文书名，用于显示和登记。未提供则询问。
  - 目录名由书名转成英文 kebab-case（如《聪明的投资者》→ `intelligent-investor`）。

## 3. 执行步骤

### 3.1 建目录

在当前项目根目录下创建书名目录：

```
<project>/<书名-kebab>/
├── raw/
└── notes/
```

### 3.2 拷贝原始文件留底

把用户提供的原文文件**拷贝**（非移动）进书名目录根下，保留原文件名。这保证原文不依赖外部路径、可随书移动。原始文件是后续所有环节的权威来源。

### 3.3 归一化为纯文本

按格式转纯文本，详细规则见 `references/chapter-splitting.md`：

| 格式 | 方式 |
|------|------|
| txt / md | 直接读取 |
| PDF | 用 Read 工具按页读取后拼接 |
| EPUB | 运行 `${CLAUDE_PLUGIN_ROOT}/scripts/parse_epub.py <epub> <output.txt>`（仅 Python 标准库） |
| 其他/失败 | 提示用户先用阅读器导出成 txt/md |

### 3.4 识别章节标记并切分

按 `references/chapter-splitting.md` 的模式识别章节边界，逐章写入 `raw/chXX.md`。首行为章节标题。

### 3.5 登记 progress.md

在书名目录下创建 `progress.md`，写入书名、目录名、拆解时间、章节数，并初始化“环节记录”表，记录 ① 拆解完成。结构见 `../methodology/references/cycle.md`。

## 4. 章节标记识别要点

支持中文“第X章”、英文“Chapter X”、Markdown 标题、独立行标题（兜底）。详见 `references/chapter-splitting.md` 的正则与样例。

- 中文数字需转阿拉伯数字作为章号。
- 提取不出数字时按标记出现顺序编号。
- 第一个标记前的前置内容（封面/目录/序言）存为 `raw/ch00-front.md`。

## 5. 健壮性

- **未识别到章节标记**：报告情况，向用户确认是整本作单章，还是请用户提供章节标记样例后重试。
- **章节数异常**（>200 或 =1）：向用户报告并请其确认。
- **EPUB 脚本运行失败**：检查 Python 是否可用；若环境缺 Python 或脚本报错，提示用户导出成 txt/md 再喂入，不要静默失败。

## 6. 完成后

向用户报告：书名、识别到的章节数、各章标题清单、raw/ 目录路径。并提示下一步运行 `/bookworm:framework` 建立全局视角。

## 7. 参考资源

- **`references/chapter-splitting.md`** — 输入格式归一化、章节标记正则、中文数字转换、切分算法、产物格式。执行切分时必读。
- **`../methodology/references/cycle.md`** — progress.md 结构与目录约定。
- **`${CLAUDE_PLUGIN_ROOT}/scripts/parse_epub.py`** — EPUB 转纯文本脚本。
