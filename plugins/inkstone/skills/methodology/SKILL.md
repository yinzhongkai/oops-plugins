---
name: methodology
description: This skill should be used when the user asks to "帮我写文案", "改写成公众号", "改成知乎回答", "变成小红书笔记", "把这个感悟发出去", "写一篇公众号", "把链接变成文案", "把这个话题写成文案", "inkstone 流程", "现在该用哪一步", or describes wanting to turn reading notes / a link / a topic into social-media copy for WeChat Official Account (公众号), Zhihu (知乎), or Xiaohongshu (小红书). Acts as the router for the inkstone three-stage pipeline (gather → organize → adapt), locating which stage the user is in, auto-chaining prior stages when skipped, and routing to the correct skill. 触发于用户想用阅读感悟、链接或话题产出社媒文案、或对 inkstone 流程/进度的整体询问时。
---

# 文案改造三阶段总览

本 skill 是 inkstone 插件的路由层。不替任何阶段干活，只做两件事：判断用户处于「前采集 → 中整理 → 后适配」哪一阶段，并引导到对应 skill；缺前置阶段时自动串起全链路。

## 1. 何时激活

- 用户想写平台文案：「帮我写篇公众号」「把这个感悟改成知乎回答」「把这个链接变成小红书笔记」
- 用户描述素材来源但没说清流程：「我有个链接想发」「这段感悟能改成啥」
- 用户询问 inkstone 流程或当前进度

## 2. 三阶段流水线

把素材改造成平台文案分三阶段，按顺序推进。各阶段定义见 `references/pipeline.md`，本 skill 仅做快速定位：

| 阶段 | skill | 一句话 |
|------|-------|--------|
| ① 前采集 | `/inkstone:gather` | 把感悟文档/链接/话题采集成原始素材，决定文案归属 |
| ② 中整理 | `/inkstone:organize` | 把异构素材整理成统一中间格式 source.md |
| ③ 后适配 | `/inkstone:adapt` | 按指定平台风格规范产出平台文案 |

## 3. 目录约定

阅读笔记（输入）与文案（输出）分目录存放：

```
<project>/
├── books/<书名>/notes/chXX.consolidate.md   # 感悟文档（gather 的主要素材，bookworm 产出）
└── copywriting/
    ├── <书名>/<选题>/source.md              # 中间格式（organize 产出）
    └── <其他>/<选题>/source.md
```

gather 不主动扫描感悟文档，由用户显式传素材路径。详细约定见 `references/pipeline.md` 第 4 节。

## 4. 定位用户当前阶段

### 4.1 从用户表述判断

- **只给了素材，没说要发哪**：用户在 ① 或想从 ① 开始 → 引导 `/inkstone:gather <素材>`
- **素材已整理成 source.md，指定了平台**：用户在 ③ → 引导 `/inkstone:adapt <平台>`
- **有 source.md 但没指定平台**：用户在 ③ 入口 → 询问目标平台后引导 adapt
- **表达迷茫**：「不知道接下来干啥」「这素材能改成啥」→ 按下方诊断排查

### 4.2 检查选题目录状态

定位到选题目录（`copywriting/<书名或选题>/<选题>/`）后，按目录内容判断进度：

- **目录不存在或无 source.md** → 还没采集/整理 → 从 ① gather 开始
- **有 source.md，无任何平台 .md** → 已整理未适配 → 进 ③ adapt（询问平台）
- **有 source.md 且已有部分平台 .md** → 该选题已产出过某平台 → 询问是补产其他平台还是重做

找不到选题目录时，询问用户：「素材是什么？想发哪个平台？」据此决定从哪阶段切入。

## 5. 自动串起全链路（跳阶段时）

用户最常见的入口是直接说「帮我把这个感悟改成知乎回答」——只指定了素材和目标平台，跳过了中间环节。此时不要停在某阶段让用户手动补，而是**自动按序串起所需阶段**：

1. 素材未采集 → 先跑 ① gather（用户显式给的素材路径/链接/话题）
2. 无 source.md → 跑 ② organize 整理成中间格式
3. organize 完成后**必须等用户确认** source.md（铁律，见 `references/pipeline.md` 第 6 节），确认后才进 ③
4. 按用户指定的平台跑 ③ adapt，产出文案

只有 organize 后的确认这一步需要停下等用户，其余顺序衔接。串起时向用户简要说明「我先采集 → 整理 → 你确认后适配」，保持流程透明。

## 6. 诊断「不知道改成啥」

当用户拿着素材不知如何下手时，逐项排查：

1. **素材没采集干净？** 感悟文档信息不全 / 链接正文没抓到 / 话题没搜透 → 引导重跑 ① gather
2. **中间格式没定下来？** 没有 source.md 或 source.md 太单薄 → 引导 ② organize，整理时让用户确认
3. **没想好发哪个平台？** 素材偏理性深度适合知乎，偏短平快适合小红书，偏长文结构适合公众号 → 给建议并引导 ③ adapt

把诊断结论告诉用户，并引导到对应阶段。

## 7. 不做什么

- 不替任何阶段执行实际工作（不采集、不整理、不写文案）。
- 不主动修改 source.md 或平台产物（那是各阶段 skill 的职责）。
- 不绕过 organize 后的用户确认直接进 adapt。
- 不主动触发其他 skill——只告知用户该运行哪个命令、或按第 5 节自动串起全链路。

## 8. 参考资源

- **`references/pipeline.md`** — 三阶段完整定义、顺序约束、目录约定、中间格式契约、三条铁律。定位步骤或回答流程细节时查阅。
