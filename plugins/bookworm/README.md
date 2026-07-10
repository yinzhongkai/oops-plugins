# bookworm

通用的「读透经典书」方法论工具。通过五环节闭环帮助读者真正读透难啃的经典书——先有全局地图再深入细节，带着问题读原文，最后用自己的话产出可发布文稿。

## 1. 解决什么问题

读经典书时常见的三个痛点：**读不懂、读完就忘、没有获得感**。本插件不替你读、不替你理解，而是提供一套可复用的方法论，从全局到细节、从输入到输出，逼你亲自走完阅读的全过程。

## 2. 五环节闭环

| 环节 | Skill | 做什么 |
|------|-------|--------|
| ① 拆解 | `/bookworm:disassemble` | 整本书原文 → 按章节存档 |
| ② 全局框架 | `/bookworm:framework` | 全书根本问题、论证脉络、章节间逻辑 |
| ③ 章节预读 | `/bookworm:pre-read` | 每章骨架 + 引导问题，带着问题读原文 |
| ④ 精读释疑 | 自动 / `/bookworm:explain` | 被动释疑：解释概念、拆难句、补背景 |
| ⑤ 巩固检验 | `/bookworm:consolidate` | 共忆 → 费曼 → 关联 → 成稿 |

另有 `methodology` 总览 skill 自动激活，判断你处于闭环哪一步并引导到正确环节。

## 3. 设计原则

- **给地图不给答案**：预读提供骨架和引导问题，不剧透内容，逼你亲自读原文
- **先验证后成稿**：成稿是走完共忆、费曼、关联后的奖赏，Claude 不独立从原文合成文稿
- **被动释疑**：精读环节不主动插话，你问才答
- **方法论通用**：换书只需新建书名目录，不改动插件

## 4. 书目目录约定

书目原文放在项目根的 `books/` 目录下，一本书一个子目录（英文 kebab-case 目录名，中文名登记在 progress.md）：

```
<project>/
└── books/
    └── intelligent-investor/
        ├── raw/                       # 按章切分的原文
        │   ├── ch01.md
        │   └── ch02.md
        ├── <原始文件>                 # disassemble 拷贝留底
        ├── framework.md               # ② 全局框架产物
        ├── notes/                     # 各环节产物
        │   ├── ch01.pre-read.md        # ③ 预读产物
        │   └── ch01.consolidate.md     # ⑤ 成稿产物
        └── progress.md                # 阅读进度（methodology 判断步骤用）
```

## 5. 环境要求

- **Python**：解析 EPUB 电子书时需要（仅用标准库，零 pip 依赖）。txt/md 与 PDF 由 Claude 原生读取能力处理。
- **EPUB 解析失败时**：插件会提示你先用阅读器把 EPUB 导出成 txt/md 再喂入。

## 6. 快速上手

1. 把整本书原文（路径）给到 Claude，运行 `/bookworm:disassemble <原文路径> <书名>`
2. `/bookworm:framework` 建立全局视角
3. 每读一章前 `/bookworm:pre-read <章号>`，带着问题读原文
4. 读时卡住直接问（自动触发 explain，或 `/bookworm:explain`）
5. 读完一章 `/bookworm:consolidate <章号>` 巩固并产出文稿

## 7. 许可

MIT
