# DESIGN.md

## 1. Purpose

This document defines the design of a dual-mode context optimization skill for coding agents used in constrained environments such as Claude Code.

The skill is intended to help an agent operate effectively when:

- context windows are limited,
- token cost matters,
- tool availability is uncertain,
- and repository context may be sparse, incomplete, or expensive to load.

The design goal is not to create a code compression prompt in isolation. The goal is to define a reusable skill that improves context selection and context usage. When tools are available, the skill should become more precise and more efficient. When tools are unavailable, the skill should still remain useful as a prompt-only strategy layer.

## 2. Repository Context

This repository is currently minimal. At the time of writing, it contains only a small `README.md` and a `LICENSE` file.

As a result, this design is intentionally:

- self-contained,
- implementation-agnostic,
- host-agnostic,
- and independent from any existing codebase structure.

This document is written to define the behavior contract before implementation exists.

## 3. Problem Statement

Coding agents often face two related constraints:

1. Context windows are finite, so full repositories cannot always be loaded into the model at once.
2. Token usage has real cost in both money and latency, so loading more code than necessary reduces efficiency.

Naive solutions such as stuffing more files into context or aggressively compressing raw source code are not sufficient by themselves. A stronger approach is to optimize what context is selected, in what order it is expanded, and how it degrades when the environment lacks tools.

The skill defined here solves the following product problem:

> Help a coding agent choose the smallest sufficient context for a task, while preserving usefulness in both tool-assisted and prompt-only environments.

## 4. Goals

The skill must:

1. Work in two modes:
   - tool-assisted mode,
   - prompt-only fallback mode.
2. Prefer selective context gathering over full-repository loading.
3. Prefer retrieval and selection before summary, and summary before compression.
4. Stay useful even when no tools are available.
5. Avoid fabricated claims about files, repository structure, tool outputs, or completed verification.
6. Produce a stable output shape across both modes.
7. Degrade gracefully when tools are unavailable, denied, or fail during execution.
8. Be practical for real coding workflows rather than purely academic.

## 5. Non-Goals

This skill does not attempt to:

1. Replace the host runtime, tool system, or orchestration layer.
2. Guarantee optimal retrieval quality in every environment.
3. Perform repository-wide indexing by itself.
4. Act as a code minifier or compiler optimization system.
5. Depend on any single vendor, model family, or host implementation detail.
6. Assume the existence of AST analysis, symbol graphs, prompt caching, or external services.

## 6. Target Environments and Constraints

This design targets environments where a coding agent may have some combination of the following:

- file search tools,
- file read tools,
- symbol lookup tools,
- token estimation tools,
- summarization tools,
- or no tools at all.

The skill must not assume that tools exist merely because the host is known by name. The skill must rely on observable in-session affordances only.

Examples of constraints this design expects:

- tool access may be missing,
- tool access may be denied by policy,
- tool access may fail mid-task,
- repository context may be tiny or very large,
- the user’s request may change during execution,
- the user may provide incomplete code context.

## 7. Core Design Principles

The skill is built around the following principles:

### 7.1 Progressive enhancement

The skill must be fully meaningful in prompt-only mode. Tooling improves precision, speed, and verification, but tooling must not define the skill’s basic usefulness.

### 7.2 Retrieval first

When tools are available, the skill should search and narrow before expanding context.

### 7.3 Selection before expansion

The skill should prefer the smallest high-value context set over loading full files or full repositories.

### 7.4 Summary before compression

If budget pressure exists, the skill should summarize lower-priority context before attempting aggressive code compression.

### 7.5 Honest uncertainty

The skill must clearly distinguish:

- observed facts,
- tool-verified findings,
- prompt-only reasoning,
- and assumptions made due to missing context.

### 7.6 One behavior model, two execution paths

The skill should not be written as two unrelated prompts. It should be one skill with one core behavior contract and two execution modes.

## 8. Dual-Mode Operating Model

The skill operates in four runtime states:

1. **Unknown**
   - Initial state before tool capability is established.
2. **Tool-assisted**
   - Tools are available, allowed, and usable.
3. **Prompt-only**
   - Tools are unavailable, disallowed, or not usable.
4. **Partial-tools**
   - Some tools are usable and others are not.

### 8.1 Shared flow across all modes

Regardless of mode, the skill follows the same high-level flow:

1. Understand the task.
2. Identify missing context.
3. Acquire or infer the minimum necessary context.
4. Produce a plan or answer.
5. Report evidence level and assumptions.

### 8.2 Tool-assisted flow

If tools are available, the skill should:

1. Search for the most relevant files, symbols, or modules.
2. Read only the most relevant sources first.
3. Build a compact task-specific context set.
4. Estimate or respect token budget where possible.
5. Summarize lower-priority context if needed.
6. Only use code compression as a late-stage fallback.

### 8.3 Prompt-only flow

If tools are not available, the skill should:

1. Work only from user-provided materials.
2. Avoid implying hidden repository access.
3. Surface the minimum missing information that would most improve the outcome.
4. Still provide a useful plan, interpretation, or next step whenever possible.
5. Explicitly mark uncertainty and assumptions.

## 9. Mode Selection Rules

The skill must select mode by observed capability, not by host identity.

### 9.1 Enter tool-assisted mode only when

- tools are explicitly exposed,
- tool usage is allowed by policy and user instruction,
- and at least one relevant tool successfully works.

### 9.2 Enter prompt-only mode when

- no tools are exposed,
- tool usage is forbidden,
- tool calls are rejected,
- or the task can proceed sufficiently from provided context alone and no further tool use is justified.

### 9.3 Enter partial-tools mode when

- only some relevant tools work,
- some tools fail while others remain available,
- or the environment provides uneven capability across search, read, and verification steps.

## 10. Failure Handling and Fallback Rules

The skill must degrade cleanly.

### 10.1 Fallback rules

1. If a tool is absent, do not depend on it.
2. If a tool is denied by policy or permission, downgrade immediately.
3. If a tool call fails or times out, retry at most once when cheap.
4. After failure, continue in prompt-only or partial-tools mode rather than repeatedly probing.
5. Never claim that a file was searched, read, or verified unless the tool actually succeeded.

### 10.2 One-way downgrade rule

Once a tool has been shown to be unusable in the current session for a required step, the skill should not repeatedly attempt the same failing path unless the environment has clearly changed.

## 11. Context Optimization Strategy

The skill’s preferred strategy order is:

1. Clarify the task.
2. Identify the highest-value missing context.
3. Retrieve only the most relevant artifacts.
4. Select a compact subset.
5. Summarize low-priority details if budget pressure remains.
6. Compress code only if summary is still insufficient and the task truly benefits.

This ordering is central to the design. The skill should optimize for context value density, not raw compression ratio.

## 12. Output Contract

The skill should produce a stable response shape in both modes.

A recommended output schema is:

1. **Understanding**
   - What the task is asking.
2. **Mode Used**
   - `tool-assisted`, `prompt-only`, or `partial-tools`.
3. **Missing Context**
   - What information is absent or uncertain.
4. **Plan / Answer**
   - What the skill recommends or concludes.
5. **Assumptions**
   - What was inferred instead of verified.
6. **Evidence Level**
   - Tool-verified, partially verified, or prompt-only reasoning.
7. **Next Best Action**
   - Best next step to improve confidence or continue execution.

Tool-assisted mode may produce richer evidence. Prompt-only mode may produce more explicit assumptions. The output shape should remain stable across both.

## 13. Risks and Tradeoffs

### 13.1 Main tradeoffs

- Tool-assisted mode is more reliable but depends on host capability.
- Prompt-only mode is more portable but less precise.
- Aggressive context minimization can miss relevant information.
- Overly cautious fallback can become too passive.

### 13.2 Main failure risks

- Over-reading too much context in tool mode.
- Hallucinating hidden repository facts in prompt-only mode.
- Conflating verified tool output with reasoning.
- Designing the skill so tool mode is mandatory for usefulness.

## 14. Acceptance Claims

The following claims define what future evaluation must prove.

### C1. Mode correctness

The skill selects the correct operating mode based on actual capability, policy, and tool success or failure.

### C2. Minimal sufficient context

In tool-assisted mode, the skill seeks the smallest sufficient context set instead of loading everything available.

### C3. Useful prompt-only fallback

In prompt-only mode, the skill remains useful and produces actionable output from provided materials alone.

### C4. Honest reporting

The skill does not fabricate files, repository structure, tool results, or completed verification.

### C5. Graceful degradation

When tools are missing, denied, or fail mid-task, the skill degrades cleanly without losing task focus.

### C6. Stable behavior contract

Both modes preserve the same core workflow and output structure, even when evidence quality differs.

### C7. Budget-aware prioritization

The skill prefers retrieval and selection before summary, and summary before compression.

### C8. Sparse-repo discipline

In a minimal repository, the skill does not over-explore or invent structure that is not present.

## 15. Future Implementation Guidance

When implemented, this skill should be tested in at least three host conditions:

1. Full tools available,
2. partial tools available,
3. no tools available.

If future implementation introduces host-specific adapters, they should remain thin. The core skill behavior should remain capability-based and host-agnostic.

## 16. Out of Scope for This Document

This document does not specify:

- a concrete skill file format,
- a concrete MCP schema,
- implementation code,
- host integration code,
- or benchmark automation.

Those belong to later stages. This document only defines the behavior contract to be implemented and evaluated.
