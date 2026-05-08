# Oh-My-AI-Coding-Style-Guide

`Oh-My-AI-Coding-Style-Guide` 是一个可发布的上下文优化技能项目，专为编码 Agent 设计。

本仓库包含：

- 技能的行为契约文档
- 面向实现的技能规范
- 宿主无关的 `SKILL.md` 技能主体
- 评估计划和测试报告
- 一键安装脚本（支持 OpenCode、Claude Code、Codex）

## 项目解决的问题

该技能帮助 Agent 在以下环境中高效工作：

- 上下文窗口有限
- Token 成本有实际开销
- 工具可用性不确定
- 仓库内容稀疏

核心行为原则：

- 优先检索，而非盲目扩展
- 优先选择，而非全量加载
- 优先摘要，而非过早压缩
- 在仅有 prompt 的降级模式下仍然可用

## 一键安装

### Claude Code

```bash
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target claude
```

### OpenCode

```bash
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode
```

### Codex

```bash
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target codex
```

### 项目本地安装（而非用户全局）

```bash
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target claude --scope project
```

### 自动检测目标

如果目标项目已包含唯一受支持的宿主目录，可使用自动检测：

```bash
python3 install.py --target auto --scope project
```

## 安装产物

安装器将技能主体和配套原则文件写入各宿主的技能目录：

- **Claude Code**
  - 用户级：`~/.claude/skills/context-optimization/SKILL.md`
  - 项目级：`.claude/skills/context-optimization/SKILL.md`

- **OpenCode**
  - 用户级：`~/.config/opencode/skills/context-optimization/SKILL.md`
  - 项目级：`.opencode/skills/context-optimization/SKILL.md`

- **Codex**
  - 用户级：`~/.agents/skills/context-optimization/SKILL.md`
  - 项目级：`.agents/skills/context-optimization/SKILL.md`

配套的 `principles.md`（浓缩版上下文优化规则）始终与 `SKILL.md` 安装在同一目录。

使用 `--scope project` 配合 `--init-always-on` 时，安装器会额外将原则注入宿主的常驻 prompt 机制：

- **OpenCode (oh-my-openagent)**：创建 `.opencode/oh-my-openagent.jsonc`，通过 `prompt_append` 指向 `principles.md`
- **Claude Code**：将原则追加到 `CLAUDE.md`
- **Codex**：将原则追加到 `AGENTS.md`

## 常驻上下文纪律

`--init-always-on` 参数使上下文优化原则对宿主的主 Agent **始终生效**，无需显式调用技能。推荐希望在每次交互中都保持 Token 预算意识和检索纪律的用户使用。

```bash
# 项目级常驻注入
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode --scope project --init-always-on

# 用户全局安装
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode --init-always-on
```

各宿主的常驻注入机制：

| 宿主 | 常驻机制 | 写入文件 |
|---|---|---|
| OpenCode | oh-my-openagent `prompt_append` | `.opencode/oh-my-openagent.jsonc` |
| Claude Code | `CLAUDE.md` 自动注入 | `CLAUDE.md` |
| Codex | `AGENTS.md` 自动注入 | `AGENTS.md` |

## 安装器安全行为

安装器支持：

- `--dry-run` 预览写入操作
- `--force` 覆盖已存在的不同文件
- `--scope user|project`
- `--target auto|claude|opencode|codex`
- `--init-always-on` 将上下文优化原则注入宿主常驻 prompt 文件

示例：

```bash
python3 install.py --target opencode --dry-run
python3 install.py --target claude --scope project
python3 install.py --target codex --force
```

## Codex 说明

Codex 在 `AGENTS.md` 中存在常驻仓库引导时效果最佳。

本仓库提供可选代码片段：

```text
snippets/CODEX_AGENTS_SNIPPET.md
```

直接打印该片段：

```bash
python3 install.py --print-codex-agents-snippet
```

## 本地验证

运行安装器测试：

```bash
python3 -m unittest tests/test_install.py
```

试运行：

```bash
python3 install.py --target claude --dry-run
```

## 仓库文件

- `DESIGN.md` — 行为契约
- `SKILL_SPEC.md` — 面向实现的技能规范
- `SKILL.md` — 宿主无关的技能主体（源文件）
- `EVALUATION.md` — 测试计划
- `TEST_REPORT.md` — 评估结果记录
- `install.py` — 一键安装脚本

## 评估结果

该技能已按 `EVALUATION.md` 中的测试计划完成评估。结果记录在 `TEST_REPORT.md`。关键发现：

- **总体：通过。** 技能行为在三种运行模式（tool-assisted、prompt-only、partial-tools）下均表现可信。
- **首轮 8 个核心测试用例全部通过**，覆盖模式正确性、优雅降级、稀疏仓库纪律和反捏造行为。
- **第二轮回归**确认输出枚举收紧（`Mode Used` 和 `Evidence Level` 为严格枚举）提升了行为一致性，未破坏核心行为。
- **实际可用性测试**表明该技能在稀疏仓库中效果显著（更好的上下文纪律、更少 Token），在中等规模仓库中作为行为治理层仍有价值，但原始 Token 节省有限。
- 技能的核心价值在于**上下文纪律和范围控制**，而非保证的原始效率。

详细结果、追溯矩阵和通过标准见 `TEST_REPORT.md`。

## 量化 Token 节省

在 `opencode` 仓库（52,218 个源文件）上使用 Codex 进行了量化测试，对比有无常驻原则注入时的 Token 消耗。测试了 6 个不同复杂度的任务。

### 测试结果

| 任务 | 基线 | 使用技能 | 节省 |
|---|---|---|---|
| T1：定位 skill 加载文件 | 187,766 | 162,846 | **-13.3%** |
| T2：统计测试文件数 | 26,248 | 18,342 | **-30.1%** |
| T3：查找测试命令 | 17,105 | 17,769 | -3.9% |
| T4：配置加载逻辑 | 超时 | 387,750 | *技能完成* |
| T5：列出 MCP 文件 | 142,849 | 91,391 | **-36.0%** |
| T6：分析构建工具链 | 超时 | 434,018 | *技能完成* |
| **合计** | **373,968** | **290,348** | **-22.4%** |

### 关键发现

- **平均 Token 节省：22.4%**
- **文件探索类任务**（T1、T5）收益最大，节省 13-36%。
- **简单配置查询**（T3）差异极小。
- **复杂任务**（T4、T6）在无技能时超时，使用技能后成功完成，表明技能除 Token 效率外还提升了任务完成的可靠性。
- 技能的核心价值在于**上下文纪律**：在大仓中防止过度探索，同时保持答案质量。

## 分享此项目

最简发布流程：

1. 发布本仓库
2. 保持 `install.py` 在默认分支可用
3. 让用户为目标宿主运行一行安装命令
