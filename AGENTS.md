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
