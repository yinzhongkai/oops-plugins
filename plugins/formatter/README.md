# formatter

对 Markdown 文件做格式化与结构编号规范化。纯规则内置，零外部依赖。

## 1. 功能

- 统一排版：标题空行、列表符号、代码块、表格对齐、段落空行、行尾空格
- 修正/补全章节编号（`1.` ↔ `##`、`1.1` ↔ `###` 等）
- 规范文件路径标注（行内代码）与文件列表自然序排序
- 只改格式与结构，不改语义内容

## 2. 安装

本插件是 `claude-plugins` marketplace 的组成部分。添加该 marketplace 后安装：

```bash
# 远程（发布后）
/plugin marketplace add https://gitee.com/nullstack/oops-plugins.git
/plugin install formatter@oops-plugins

# 本地
/plugin marketplace add C:\Users\zhongkai.yin\Desktop\claude-plugins
/plugin install formatter@oops-plugins
```

或开发期本地直接加载单插件：

```bash
cc --plugin-dir C:\Users\zhongkai.yin\Desktop\claude-plugins\plugins\formatter
```

## 3. 使用

```
/formatter:markdown <文件或目录>
```

- 不带参数：格式化当前对话中最近提及/编辑的 Markdown 文件
- 带文件路径：格式化该文件
- 带目录路径：递归格式化目录下所有 `.md` 文件

也可用自然语言触发，如“格式化这个 md”、“规范 README.md”。

## 4. 规则

详细规则见 [`skills/markdown/references/formatting-rules.md`](skills/markdown/references/formatting-rules.md)。

### 4.1 章节编号行为

- 文档已有编号 → 按层级补全/连续化，父级缺失则补全，使编号体系完整不断层
- 文档无编号但含子章节 → 主动为全文加编号
- 混合编号（部分有部分无）→ 统一为有编号体系
- 单章且无子章节 → 不编号

## 5. 许可证

MIT
