# Oh-My-AI-Coding-Style-Guide

一个为编码 Agent 设计的上下文优化技能。帮助 Agent 用最少的上下文工作，避免过度探索，诚实区分已知与推测。

## 解决的问题

编码 Agent 浪费 Token 的常见原因：

- 只需要几个文件，却加载了整个仓库
- 为了显得「全面」而广泛探索
- 上下文已经足够，却继续读取
- 无法区分已验证的事实和推测

该技能提供一组原则，约束 Agent 的探索行为，在保持答案质量的同时减少 Token 消耗。

## 安装方式

### 方式一：按需加载（默认）

将技能安装到宿主的技能目录。Agent 在识别到匹配场景时，通过宿主原生的技能发现机制按需加载。

```bash
# Codex
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target codex

# Claude Code
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target claude

# OpenCode
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode
```

### 方式二：常驻原则（推荐）

将浓缩版上下文优化原则注入宿主的常驻 prompt 文件。Agent 在每次交互中自动遵循这些原则，无需加载完整技能。

```bash
# Codex（注入到 AGENTS.md）
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target codex --scope project --init-always-on

# Claude Code（注入到 CLAUDE.md）
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target claude --scope project --init-always-on

# OpenCode（创建 oh-my-openagent.jsonc，配置 prompt_append）
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode --scope project --init-always-on
```

### 两种方式的区别

| 安装方式 | 发生了什么 | Agent 行为 |
|---|---|---|
| 默认 | 技能文件安装到技能目录 | Agent 在识别到匹配场景时按需加载 |
| 常驻原则 | 浓缩版原则注入宿主 prompt | Agent 在每次交互中自动遵循原则 |

## 测试效果

### 行为评估

在不同大小的仓库上，跨三种运行模式（tool-assisted、prompt-only、partial-tools）进行了测试：

- **8 个核心测试用例全部通过** — 模式正确性、优雅降级、稀疏仓库纪律、反捏造行为
- **输出契约稳定** — tool-assisted 和 prompt-only 模式下行为结构一致
- **无捏造** — 技能不会虚构文件、模块或工具输出

详细结果：`TEST_REPORT.md`

### 量化 Token 节省

在 `opencode` 仓库（52,218 个源文件）上使用 Codex 测试，对比有无常驻原则时的 Token 消耗：

| 任务 | 基线 | 使用技能 | 节省 |
|---|---|---|---|
| T1：定位 skill 加载文件 | 187,766 | 162,846 | **-13.3%** |
| T2：统计测试文件数 | 26,248 | 18,342 | **-30.1%** |
| T3：查找测试命令 | 17,105 | 17,769 | -3.9% |
| T4：配置加载逻辑 | 超时 | 387,750 | *技能完成* |
| T5：列出 MCP 文件 | 142,849 | 91,391 | **-36.0%** |
| T6：分析构建工具链 | 超时 | 434,018 | *技能完成* |
| **合计** | **373,968** | **290,348** | **-22.4%** |

关键发现：

- **平均 Token 节省 22.4%**
- 文件探索类任务收益最大（13-36% 节省）
- 无技能时超时的复杂任务，使用技能后成功完成
- 技能的核心价值在于**上下文纪律**：在大仓中防止过度探索，同时保持答案质量

## 仓库文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 宿主无关的技能主体（源文件） |
| `DESIGN.md` | 行为契约和验收声明 |
| `SKILL_SPEC.md` | 面向实现的规范 |
| `EVALUATION.md` | 测试计划 |
| `TEST_REPORT.md` | 评估结果 |
| `install.py` | 一键安装脚本 |
| `tests/test_install.py` | 安装器测试 |
| `tests/test_quantitative.py` | 量化 Token 测试脚本 |

## 本地验证

```bash
# 运行安装器测试
python3 -m unittest tests/test_install.py

# 试运行（预览，不写入文件）
python3 install.py --target codex --scope project --init-always-on --dry-run
```
