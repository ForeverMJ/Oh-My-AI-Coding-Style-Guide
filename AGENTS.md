# AGENTS.md — Oh-My-AI-Coding-Style-Guide

## Project

A context-optimization skill for coding agents that operates in tool-assisted,
prompt-only, and partial-tools modes. The skill helps agents use the smallest
sufficient context while staying honest about verification and fallback behavior.

## Skill Loading

<!-- context-optimization:skill-loader -->
Prioritize retrieval-led reasoning over pretrained-knowledge-led reasoning.
When a task involves sparse repositories, limited token budgets, or uncertain
tool availability, load the `context-optimization` skill before proceeding.

## Key Documents

- `DESIGN.md` — behavior contract and acceptance claims
- `SKILL_SPEC.md` — implementation-facing specification
- `SKILL.md` — host-agnostic skill body
- `EVALUATION.md` — test plan and scenario catalog
- `TEST_REPORT.md` — evaluation results

<!-- context-optimization:always-on -->
## Context Optimization Principles

Maximize output per token consumed. Every file read, every search run, every
agent fired costs real money and latency. Treat context budget as a first-class
constraint.

### Retrieval First
Prefer targeted inspection over broad exploration. Search and narrow before
expanding context:
- Start with the smallest high-value context set
- Expand only when genuinely blocked
- Never load entire repositories unless the task explicitly requires full audit

### Sparse Repo Discipline
If the repository is small (few files, documentation-heavy, no complex code):
- Do not over-explore merely because tools exist
- Do not assume or invent structure not present

### Mode Awareness
- If tools are available and relevant, use them, sparingly
- If tools fail or are absent, stay useful in degraded mode
- Never claim inspection not actually performed

### Evidence Boundaries
- Distinguish: observed facts / tool-verified findings / assumptions / unknown
- Do not fabricate files, modules, or tool outputs
- If not read, do not imply it was read

### Budget Pressure
- If context window is filling up, summarize low-priority material
- Compression is a last resort, not a first move
- Prefer: retrieval → selection → summary → compression
