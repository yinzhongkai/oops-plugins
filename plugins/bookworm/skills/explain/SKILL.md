---
name: explain
description: This skill should be used when the user, while reading the original text, asks "这段啥意思", "市场先生是什么", "这句话不懂", "读这段时解释一下", "这里卡住了", "what does this passage mean", "explain this concept", or expresses confusion about a specific passage/concept in the book being read. Provides on-demand clarification — explains concepts, breaks down hard sentences, and supplies background — passively, only when asked. Also triggers on "/bookworm:explain". Does NOT trigger during consolidate (co-recall / Feynman / linking) — confusion during consolidation belongs to consolidate, not explain; the "while reading the original text" scope excludes the consolidation phase. 触发于用户读原文时对具体段落/概念提出疑问时。被动响应，不主动插话；巩固环节的疑问归 consolidate，不触发本 skill。
---

# 精读释疑

用户读原文时卡住，被动提供释疑。解释概念、拆解难句、补充背景，并对照原文存档校验准确性。不落文件。

## 1. 何时使用

- **自动**：用户读原文时提出疑问（如"这段啥意思""市场先生是什么""第8章这句不懂"）。
- **斜杠**：用户运行 `/bookworm:explain` 后提问。

## 2. 何时不使用

巩固环节（consolidate 的共忆/费曼/关联）中用户表达困惑时，**不触发本 skill**——那属于 consolidate 的职责范围。仅在用户**正在读原文、对具体段落或概念提出疑问**时响应。"读原文"指精读阶段，非巩固阶段的回忆/复述。

## 3. 被动原则

**绝不主动插话**。不检测用户是否跳过难点、不主动提示"这里可能难懂"。只在用户明确提问后响应，保持用户自己的阅读节奏。

## 4. 输入

- 用户的疑问 + 涉及的原文片段或章号。

## 5. 执行步骤

### 5.1 定位原文

根据用户给的章号，或用户贴入的片段，从 `<书名>/raw/chXX.md` 读取对应原文，确保释疑基于准确文本。若用户未指定章号，从其引用的片段或上下文推断；推断不出则询问。

### 5.2 释疑

按疑问类型响应：

- **概念解释**：说清概念含义、为何重要、作者如何定义。用通俗话，必要时类比。
- **难句拆解**：把长难句拆成短句，讲清句法结构和指代关系。
- **背景补充**：补全成书年代、作者立场、相关术语体系等帮助理解的背景。

### 5.3 对照原文校验

释疑后回看 raw/ 原文，确认解释与原文一致、未曲解。若用户记忆的原文有出入，以原文为准并指出。

### 5.4 关联全局

若疑问涉及全书脉络（如某概念如何贯穿全书），引用 `framework.md` 把释疑放进全局视角。

## 6. 不做什么

- **不落文件**：释疑是对话内即时响应，不写进 notes/。结构化沉淀是 consolidate 的职责，释疑存档会与其产物重复、界限模糊。
- **不剧透未读章节**：用户问到未读章节的内容时，可提示"这是后续章节，读到了再细聊"，不提前剧透。
- **不主动出题或检验**：那是 consolidate 的活。

## 7. 参考资源

- **`../methodology/references/cycle.md`** — "被动释疑"铁律。
