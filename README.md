# Oh-My-AI-Coding-Style-Guide

`Oh-My-AI-Coding-Style-Guide` is a publishable context-optimization skill project for coding agents.

The repository contains:

- the design contract for the skill,
- the implementation-facing skill spec,
- the actual host-agnostic `SKILL.md`,
- evaluation plans and test reports,
- and a one-command installer for OpenCode, Claude Code, and Codex.

## What this project solves

The skill helps agents operate under:

- limited context windows,
- real token cost,
- uncertain tool availability,
- and sparse repositories.

Its core behavior is:

- prefer retrieval over broad expansion,
- prefer selection over full loading,
- prefer summary before compression,
- and remain useful even in prompt-only fallback mode.

## Install in one command

After publishing this repository, users can install the skill with a single command.

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

### Project-local install instead of user-global

```bash
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target claude --scope project
```

### Auto-detect target

If the target project already contains exactly one supported host directory, auto-detection can be used:

```bash
python3 install.py --target auto --scope project
```

## What gets installed

The installer writes the wrapped skill to the documented skill locations for each host:

- **Claude Code**
  - user: `~/.claude/skills/context-optimization/SKILL.md`
  - project: `.claude/skills/context-optimization/SKILL.md`

- **OpenCode**
  - user: `~/.config/opencode/skills/context-optimization/SKILL.md`
  - project: `.opencode/skills/context-optimization/SKILL.md`

- **Codex**
  - user: `~/.agents/skills/context-optimization/SKILL.md`
  - project: `.agents/skills/context-optimization/SKILL.md`

These install paths are based on the documented skill-discovery locations for each host. This repository verifies path generation and file installation locally. You should still validate skill discovery in the exact host version you plan to use.

## Safe installer behavior

The installer supports:

- `--dry-run` to preview writes,
- `--force` to overwrite a different existing file,
- `--scope user|project`,
- `--target auto|claude|opencode|codex`.

Examples:

```bash
python3 install.py --target opencode --dry-run
python3 install.py --target claude --scope project
python3 install.py --target codex --force
```

## Codex note

Codex works best when always-on repository guidance also exists in `AGENTS.md`.

This repository includes an optional snippet at:

```text
snippets/CODEX_AGENTS_SNIPPET.md
```

To print that snippet directly:

```bash
python3 install.py --print-codex-agents-snippet
```

## Verify locally

Run the installer tests:

```bash
python3 -m unittest tests/test_install.py
```

Try a dry run:

```bash
python3 install.py --target claude --dry-run
```

## Repository files

- `DESIGN.md` — behavior contract
- `SKILL_SPEC.md` — implementation-facing skill specification
- `SKILL.md` — source-of-truth host-agnostic skill body
- `EVALUATION.md` — test plan
- `TEST_REPORT.md` — observed evaluation results
- `install.py` — one-command installer

## Sharing this project

The simplest release flow is:

1. publish this repo,
2. keep `install.py` available on the default branch,
3. ask users to run the one-line install command for their target host.
