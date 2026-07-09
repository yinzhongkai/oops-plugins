---
name: consolidate
description: This skill should be used when the user invokes "/bookworm:consolidate", asks to "巩固这一章", "检验我读透了没", "一起回忆这章", "把这章写成文章", "做费曼复述", "consolidate chapter N", "produce a publishable article". Runs the internal gated pipeline: co-recall → Feynman recount → cross-chapter linking → publishable article. Verifies understanding before allowing the article. 触发于读完一章后做巩固检验、产出可发布文稿时。
---

# 巩固检验

读完一章后，通过共忆、费曼、关联检验读没读透，最后产出可发布文稿。先验证后成稿。每章读后一次。

## 1. 何时使用

- 用户运行 `/bookworm:consolidate [章号]`
- 用户读完一章，想检验掌握程度
- 用户想把本章理解整理成文章

## 2. 输入

- **章号**（可选）：未提供则读 progress.md 看下一未巩固章，或交互询问。

## 3. 前置检查

- 确认 `<书名>/raw/chXX.md` 存在（作共忆校验的事实依据）。
- 若存在 `framework.md` 和 `notes/chXX.pre-read.md`，读它们作关联和定位参考。

## 4. 内部门控流水线（必须顺序走）

成稿是走完前三步的奖赏。**不得跳过、不得乱序**。

### 4.1 共忆

对话式重建本章内容。**用户主讲、Claude 配合**：

- 先让用户主动回忆本章讲了什么、核心论点、关键例子。
- 用户卡壳时，Claude 给**线索**（提示性的、指向性的），不直接给答案。
- Claude 补事实空白：用户漏掉的关键事实可补，但标注“这是原文的，你回忆时没提到”（补充的事实仅供校验，不得进入 ⑤ 成稿——成稿内容必须来自用户自己讲的话）。
- **对照原文校验**：从 raw/ 读原文，标记用户回忆与原文的出入，以原文为准指出偏差。Claude 在此充当事实裁判，但不替用户回忆。

### 4.2 费曼复述

要求用户**用自己的话**讲清本章核心观点，假定讲给一个不懂的人听。这是检验“能用自己的话讲清楚”的环节。若用户讲不清，说明没读透——回到原文或 explain 补，再复述。不放过关。

### 4.3 关联检验

把本章放进全书脉络：

- 本章承接了前面哪些章节的论点？
- 为后续哪些章节铺路？
- 引用 framework.md 校验关联的准确性。

### 4.4 成稿

走完 4.1-4.3 后，把**用户讲出来的理解**组织成可发布文稿。Claude 只做结构组织 + 文字润色，**不独立从原文合成**。详细规范见 `references/publishing.md`。

产物存到 `<书名>/notes/chXX.consolidate.md`，在 progress.md 追加：⑤ 巩固 章 X 完成。

## 5. 铁律：先验证后成稿

- 成稿前必须走完共忆、费曼、关联。这三步是闸门，逼用户真的读进去了。
- 若用户在共忆/费曼时大量讲不出、答非所问，说明没读透——**不进入成稿**，提示用户回原文精读或用 explain 补，再回来。
- 文稿内容来自用户自己讲的话，Claude 凭原文补全的部分不得进文稿（堵死第二根拐杖）。回忆不全处如实标“待深入”。

## 6. 完成后

向用户展示文稿，提示：
- “待深入”部分可日后补；
- 继续下一章，回到 `/bookworm:pre-read <下一章号>`；
- 或回头补本章遗漏。

## 7. 参考资源

- **`references/publishing.md`** — 文稿结构、内容来源铁律、质量标准、成稿后处理。执行 4.4 时必读。
- **`../methodology/references/cycle.md`** — “先验证后成稿”铁律。
