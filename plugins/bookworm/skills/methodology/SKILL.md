---
name: methodology
description: This skill should be used when the user asks to "读透一本书", "怎么开始读", "读到哪了", "接下来读什么", "读完没收获", "不知道接下来读哪一步", "阅读流程", "read through a book", or expresses confusion about where they are in reading a book. Acts as the navigator for the bookworm closed loop, locating which of the five phases the user is in and routing them to the correct skill. 触发于用户对阅读流程或阅读进度的整体询问、或表达"读完没有收获感"等迷茫时。
---

# 读透闭环总览

本 skill 是 bookworm 插件的路由层。不替任何环节干活，只做一件事：判断用户处于五环节闭环的哪一步，并引导到对应的 skill。

## 1. 何时激活

- 用户想开始读一本书，问“第一步干啥 / 怎么开始”
- 用户读到中途，问“接下来呢 / 现在该做什么”
- 用户表达迷茫：“读完没收获 / 读不懂 / 不知道卡在哪”
- 用户询问整体阅读流程

## 2. 五环节闭环

读透一本书分五环节，按顺序推进。详细定义见 `references/cycle.md`，本 skill 仅做快速定位：

| 环节 | skill | 一句话 |
|------|-------|--------|
| ① 拆解 | `/bookworm:disassemble` | 整本书原文按章存档 |
| ② 全局框架 | `/bookworm:framework` | 全书根本问题、论证脉络、章节关系 |
| ③ 章节预读 | `/bookworm:pre-read` | 每章骨架 + 引导问题，带着问题读 |
| ④ 精读释疑 | 自动 / `/bookworm:explain` | 卡住时被动释疑 |
| ⑤ 巩固检验 | `/bookworm:consolidate` | 共忆→费曼→关联→成稿 |

## 3. 定位用户当前步骤

### 3.1 有 progress.md 时

读取 `books/<书名>/progress.md`（书名目录下的进度文件）。根据“环节记录”表中每章的状态判断：

- **无任何记录** → 用户还没拆解，引导 `/bookworm:disassemble`
- **只有拆解记录** → 引导 `/bookworm:framework` 建立全局视角
- **有框架记录，某章无预读** → 引导该章 `/bookworm:pre-read`
- **某章已预读，无巩固记录** → 用户应在精读/释疑阶段；读完后引导 `/bookworm:consolidate`
- **某章已巩固** → 建议进入下一章，回到 ③

### 3.2 无 progress.md 或找不到书名目录时

询问用户：“你现在在读哪本书？是否已经把原文拆解存档？” 根据回答：

- 还没开始 → 引导 `/bookworm:disassemble <原文路径> <书名>`
- 已拆解但目录不同 → 确认书名目录位置

## 4. 诊断“读完没收获”

当用户说“读完没收获感”时，这是本 skill 最有价值的能力。逐项排查：

1. **跳过了全局框架？** 没读 framework.md → 没有“全局地图”，读细节会迷失。引导补 ②。
2. **跳过了预读直接扎进原文？** 没带问题读，缺乏方向。引导补 ③。
3. **只读不做巩固？** 缺 ⑤ 的检验和输出 → 读过的没沉淀成自己的理解。引导 ⑤。
4. **巩固时跳过了验证直接成稿？** 文稿是 Claude 的理解而非用户的，违反先验证后成稿。要求重走 consolidate 的共忆→费曼→关联三步。

把诊断结论告诉用户，并引导到对应的补救环节。

## 5. 不做什么

- 不替任何环节执行实际工作（不拆书、不总结、不出题、不成稿）。
- 不主动触发其他 skill——只告知用户该运行哪个命令、或该等哪个自动 skill 响应。
- 不修改 progress.md（那是各环节 skill 的职责）。

## 6. 参考资源

- **`references/cycle.md`** — 五环节闭环完整定义、目录约定、progress.md 结构、三条铁律。定位步骤或回答流程细节时查阅。
