# Oh-My-AI-Coding-Style-Guide

A context-optimization skill for coding agents. Helps agents work with minimal context, avoid over-exploration, and stay honest about what they know versus what they assume.

## Problem

Coding agents waste tokens by:

- loading entire repositories when only a few files are relevant,
- exploring broadly to appear thorough,
- continuing to read when they already have enough context,
- failing to distinguish verified facts from assumptions.

This skill provides a set of principles that constrain the agent's exploration behavior, reducing token consumption while maintaining answer quality.

## Installation

### Option 1: On-demand skill (default)

Installs the skill to the host's skill directory. The agent loads it when needed via the host's native skill discovery.

```bash
# Codex
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target codex

# Claude Code
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target claude

# OpenCode
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode
```

### Option 2: Always-on principles (recommended)

Injects condensed context-optimization principles into the host's always-on prompt file. The agent follows these principles in every interaction without needing to load the full skill.

```bash
# Codex (injects into AGENTS.md)
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target codex --scope project --init-always-on

# Claude Code (injects into CLAUDE.md)
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target claude --scope project --init-always-on

# OpenCode (creates oh-my-openagent.jsonc with prompt_append)
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode --scope project --init-always-on
```

### Difference

| Install type | What happens | Agent behavior |
|---|---|---|
| Default | Skill files installed to skill directory | Agent loads skill on-demand when it recognizes a matching scenario |
| Always-on | Condensed principles injected into host prompt | Agent follows principles in every interaction automatically |

## Tested results

### Behavioral evaluation

Tested across three operating modes (tool-assisted, prompt-only, partial-tools) on repositories of different sizes:

- **8/8 core test cases passed** — mode correctness, graceful degradation, sparse-repo discipline, fabrication guards
- **Output contract stability** — same behavior structure across tool-assisted and prompt-only modes
- **No fabrication** — skill never invents files, modules, or tool outputs

Detailed results: `TEST_REPORT.md`

### Quantitative token savings

Tested on the `opencode` repository (52,218 source files) using Codex, comparing token usage with and without always-on principles:

| Task | Baseline | With Skill | Reduction |
|---|---|---|---|
| T1: Locate skill loading files | 187,766 | 162,846 | **-13.3%** |
| T2: Count test files | 26,248 | 18,342 | **-30.1%** |
| T3: Find test command | 17,105 | 17,769 | -3.9% |
| T4: Config loading logic | timeout | 387,750 | *skill completed* |
| T5: List MCP files | 142,849 | 91,391 | **-36.0%** |
| T6: Analyze build toolchain | timeout | 434,018 | *skill completed* |
| **Total** | **373,968** | **290,348** | **-22.4%** |

Key findings:

- **22.4% average token reduction** across all tasks
- File exploration tasks benefit most (13-36% savings)
- Complex tasks that timed out without the skill completed successfully with it
- The skill's primary value is **context discipline**: preventing over-exploration while maintaining answer quality

## Repository files

| File | Purpose |
|---|---|
| `SKILL.md` | Host-agnostic skill body (source of truth) |
| `DESIGN.md` | Behavior contract and acceptance claims |
| `SKILL_SPEC.md` | Implementation-facing specification |
| `EVALUATION.md` | Test plan |
| `TEST_REPORT.md` | Evaluation results |
| `install.py` | One-command installer |
| `tests/test_install.py` | Installer tests |
| `tests/test_quantitative.py` | Quantitative token test script |

## Local verification

```bash
# Run installer tests
python3 -m unittest tests/test_install.py

# Dry run (preview without writing)
python3 install.py --target codex --scope project --init-always-on --dry-run
```
