# oops-plugins

Claude 插件大杂烩 —— 围绕「阅读、整理、输出」工作流的一组 Claude 插件。

| 项目 | 说明 |
|------|------|
| 仓库 | <https://github.com/yinzhongkai/oops-plugins> |
| 许可证 | MIT |
| 作者 | yinzhongkai (<yinzhongkai@yeah.net>) |

## 1. 简介

本仓库收录了三个互相独立的 Claude 插件，分别解决内容创作流程中的不同环节：

- **formatter**：Markdown 格式化与结构编号规范化。
- **bookworm**：「读透经典书」方法论工具，通过拆解 → 框架 → 预读 → 精读 → 巩固五环节闭环，把难啃的经典书真正读进去。
- **inkstone**：中文社媒文案改造器，把阅读感悟、链接、话题等素材改造成适配微信公众号、知乎、小红书等平台的文案。

三个插件都遵循「规则内置、少依赖、可扩展」的设计：formatter 与 inkstone 零运行时依赖；bookworm 仅依赖 Python 标准库解析 EPUB。

## 2. 安装

在 Claude Code 对话中直接执行：

```
/plugin marketplace add yinzhongkai/oops-plugins
```

添加 marketplace 后，即可安装其中某个插件。marketplace 名取自 `.claude-plugin/marketplace.json` 顶层的 `name` 字段（本仓库为 `oops-plugins`），安装命令格式为 `/plugin install <插件名>@<marketplace名>`：

```
/plugin install formatter@oops-plugins
/plugin install bookworm@oops-plugins
/plugin install inkstone@oops-plugins
```

可用 `/plugin list --available` 查看该 marketplace 下的所有插件。

## 3. 插件一览

### 3.1 formatter

对 Markdown 文件做格式化与结构编号规范化。

- **功能**：统一排版（标题空行、列表、代码块、表格、段落）、修正/补全章节编号、规范文件路径标注与文件列表自然序排序。
- **核心约束**：只改格式与结构，不改语义内容。
- **用法**：`/formatter:markdown <文件或目录>`
- **路径**：[`plugins/formatter`](./plugins/formatter)

### 3.2 bookworm

通用的「读透经典书」方法论工具。

- **五环节闭环**：
  1. `/bookworm:disassemble` — 整本书原文按章节存档
  2. `/bookworm:framework` — 建立全书全局框架
  3. `/bookworm:pre-read` — 章节预读，带着问题读原文
  4. `/bookworm:explain` — 精读释疑，卡住时被动答疑
  5. `/bookworm:consolidate` — 巩固检验，共忆 → 费曼 → 关联 → 成稿
- **设计原则**：给地图不给答案、先验证后成稿、被动释疑、方法论通用。
- **环境要求**：需要 Python 环境解析 EPUB（仅标准库，无 pip 依赖）。
- **路径**：[`plugins/bookworm`](./plugins/bookworm)

### 3.3 inkstone

中文社媒文案改造器。

- **三阶段流水线**：
  1. `/inkstone:gather` — 前采集：把感悟/链接/话题采集成原始素材
  2. `/inkstone:organize` — 中整理：把异构素材整理成统一中间格式 `source.md`
  3. `/inkstone:adapt` — 后适配：按平台风格改造成公众号/知乎/小红书文案
- **设计原则**：改造而非创作、前后端对称扩展、统一中间格式、口语化真人感、用户确认中间格式。
- **环境要求**：零外部运行时依赖。
- **路径**：[`plugins/inkstone`](./plugins/inkstone)

## 4. 目录结构

```
.
├── .claude/
│   └── settings.local.json          # 本地权限配置
├── .claude-plugin/
│   └── marketplace.json             # 插件集市场清单
├── plugins/
│   ├── formatter/                   # Markdown 格式化插件
│   │   ├── .claude-plugin/plugin.json
│   │   ├── README.md
│   │   └── skills/markdown/
│   │       ├── SKILL.md
│   │       └── references/formatting-rules.md
│   ├── bookworm/                    # 读透经典书插件
│   │   ├── .claude-plugin/plugin.json
│   │   ├── README.md
│   │   ├── scripts/parse_epub.py    # EPUB 解析脚本（Python 标准库）
│   │   └── skills/
│   │       ├── disassemble/
│   │       ├── framework/
│   │       ├── pre-read/
│   │       ├── explain/
│   │       ├── consolidate/
│   │       └── methodology/
│   └── inkstone/                    # 中文社媒文案改造器插件
│       ├── .claude-plugin/plugin.json
│       ├── README.md
│       └── skills/
│           ├── gather/
│           ├── organize/
│           ├── adapt/
│           └── methodology/
├── LICENSE                          # MIT 许可证
└── README.md                        # 本文件
```

## 5. 许可证

MIT License — 详见 [LICENSE](./LICENSE)。
