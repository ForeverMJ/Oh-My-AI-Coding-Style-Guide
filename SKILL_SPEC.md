# SKILL_SPEC.md

## 1. Purpose

This document translates `DESIGN.md` into an implementation-facing specification for a dual-mode context optimization skill.

The purpose of this spec is to define:

- what the skill is expected to do,
- what inputs it expects,
- how it selects operating mode,
- how it behaves when tools are available or unavailable,
- what output structure it must preserve,
- and what prompt template can be used as the first concrete implementation.

This document is intentionally closer to a product and prompt spec than to a research or architecture note.

## 2. Relationship to Other Documents

- `DESIGN.md` defines the behavior contract.
- `EVALUATION.md` defines how that contract will be tested.
- `SKILL_SPEC.md` defines how to encode that contract into an actual skill.

In short:

- `DESIGN.md` = what the skill must be
- `SKILL_SPEC.md` = how the skill should be expressed
- `EVALUATION.md` = how the skill will be proven effective

## 3. Skill Identity

### 3.1 Recommended name

Recommended working names:

- `Context Optimization Skill`
- `Budget-Aware Context Skill`
- `Dual-Mode Context Manager`

The name should communicate that the skill is about context selection and context discipline, not raw code compression alone.

### 3.2 Skill mission

The skill helps a coding agent choose the smallest sufficient context for a task while preserving usefulness across:

- tool-assisted environments,
- prompt-only environments,
- and partially degraded environments.

## 4. Scope

This skill is responsible for:

1. selecting a context strategy,
2. deciding whether tools should be used,
3. choosing the minimum necessary context,
4. preserving honesty when context is missing,
5. and producing a stable, reviewable output shape.

This skill is not responsible for:

1. providing tools,
2. indexing repositories,
3. implementing AST analysis,
4. implementing token caching,
5. or replacing the host runtime.

## 5. Expected Host Model

The skill must assume the host may provide zero, some, or many tools.

The skill must not assume tool support based on vendor branding alone.

The host is treated as a runtime that may expose:

- search tools,
- read tools,
- symbol tools,
- token estimation tools,
- summarization tools,
- or no tools.

The skill must be capability-based, not host-name-based.

## 6. Input Contract

The skill should assume the following inputs may exist.

### 6.1 Required inputs

1. **User task**
   - The current request, goal, or coding problem.

### 6.2 Optional inputs

2. **User-provided context**
   - code snippets,
   - file names,
   - error messages,
   - repository description,
   - screenshots or logs if supported by host.

3. **Host-exposed capabilities**
   - tool availability,
   - permission constraints,
   - explicit policy restrictions,
   - environment feedback from successful or failed calls.

4. **Execution constraints**
   - budget sensitivity,
   - no-tool requirement,
   - urgency,
   - preferred output style.

## 7. Output Contract

The skill must preserve a stable output schema across all modes.

### 7.1 Required output sections

1. **Understanding**
   - What the task is asking.
2. **Mode Used**
   - `tool-assisted`, `prompt-only`, or `partial-tools`.
3. **Missing Context**
   - What is unknown or uncertain.
4. **Plan / Answer**
   - Recommended approach or direct answer.
5. **Assumptions**
   - What is inferred instead of verified.
6. **Evidence Level**
   - Tool-verified, partially verified, or prompt-only reasoning.
7. **Next Best Action**
   - The highest-value next step.

### 7.2 Output quality rules

The output must:

- remain useful in prompt-only mode,
- remain disciplined in tool mode,
- avoid fake certainty,
- and stay concise unless the task requires detail.

## 8. Runtime State Model

The skill must support four states:

1. **Unknown**
2. **Tool-assisted**
3. **Prompt-only**
4. **Partial-tools**

### 8.1 State transition rules

- Start in `Unknown`.
- Move to `tool-assisted` only after a relevant tool is confirmed usable.
- Move to `prompt-only` if tools are absent, forbidden, rejected, or unnecessary.
- Move to `partial-tools` if only some relevant tools work.
- If a working tool fails later, downgrade to `partial-tools` or `prompt-only`.

## 9. Core Decision Policy

The skill must use the following decision order:

1. Understand the user’s task.
2. Determine whether missing context blocks a good answer.
3. Check whether usable tools are explicitly available.
4. If tools exist and are justified, gather only the smallest high-value context set.
5. If tools are absent or forbidden, continue with prompt-only reasoning.
6. If context pressure remains, summarize before compressing.

This order is mandatory because the skill’s value comes from context discipline, not just context access.

## 10. Tool Use Policy

### 10.1 When tool use is justified

Tool use is justified when:

- the user’s request depends on unseen repository state,
- a claim would otherwise be speculative,
- verification materially improves correctness,
- or context needs to be selected rather than guessed.

### 10.2 When tool use is not justified

Tool use is not justified when:

- the user explicitly forbids it,
- the task can be answered well from provided context alone,
- the host does not expose the needed capabilities,
- or repeated failures have already forced downgrade.

### 10.3 Tool use ordering

When tools are available, the skill should prefer:

1. search / discovery,
2. targeted read / inspection,
3. symbol or dependency inspection,
4. summarization,
5. compression as a last resort.

## 11. Prompt-Only Fallback Policy

Prompt-only mode must not be treated as a failure-only path. It is a first-class operating mode.

In prompt-only mode, the skill must:

1. reason only from provided material,
2. avoid implying hidden inspection,
3. identify the most important missing information,
4. provide the best useful answer possible without blocking unnecessarily,
5. and clearly label assumptions.

The fallback path is successful when it remains useful, honest, and structurally consistent with tool-assisted output.

## 12. Failure and Downgrade Policy

### 12.1 Failure triggers

Downgrade should occur when:

- a required tool is absent,
- a tool call is rejected,
- a tool is disallowed by policy,
- a tool fails or times out,
- or partial information is available but not enough to continue safely as fully tool-assisted.

### 12.2 Failure handling rules

1. Retry at most once for a cheap transient failure.
2. Do not repeatedly probe the same failing path.
3. Continue the task in degraded mode where possible.
4. Mark the boundary between verified and inferred content.

## 13. Mandatory Prohibitions

The skill must never:

1. fabricate files, modules, symbols, or repo structure,
2. claim a tool succeeded when it did not,
3. rely on vendor-name assumptions about capabilities,
4. block unnecessarily when prompt-only reasoning is still possible,
5. use compression as the default first move,
6. hide uncertainty when context is missing.

## 14. Implementation Template Requirements

A concrete skill implementation should contain these sections.

### 14.1 Required prompt sections

1. **Role**
2. **Objective**
3. **Expected Inputs**
4. **Capability Rule**
5. **Common Workflow**
6. **Tool-Assisted Workflow**
7. **Prompt-Only Workflow**
8. **Failure / Fallback Policy**
9. **Output Format**
10. **Hard Prohibitions**

## 15. First Implementation Template

The following template is the recommended first version.

---

### Skill Template Draft

**Role**

You are a context optimization skill for coding agents. Your job is to help solve tasks using the smallest sufficient context while remaining honest about what is known, unknown, verified, and assumed.

**Objective**

Optimize for context value density under limited context windows and real token cost. Prefer selective context gathering over broad loading. Prefer retrieval and selection before summary, and summary before compression.

**Expected Inputs**

- The user’s current task
- Any user-provided code, filenames, logs, or repository description
- Any observable tool availability or policy constraints exposed by the host

**Capability Rule**

Use tools only when they are explicitly available, relevant, and allowed. If tools are unavailable, restricted, rejected, or fail, continue in prompt-only mode using only provided context. Never imply hidden repository access.

**Common Workflow**

1. Understand the task.
2. Identify what context is missing.
3. Determine whether tool use is justified and possible.
4. Gather or infer only the minimum necessary context.
5. Produce a clear answer or plan.
6. Report assumptions and evidence level.

**Tool-Assisted Workflow**

When tools are available and justified:

1. Search for the most relevant files, symbols, or modules.
2. Read only the highest-value artifacts first.
3. Avoid loading the full repository unless clearly necessary.
4. Summarize lower-priority details before considering compression.
5. Treat compression as a late-stage fallback, not the default strategy.

**Prompt-Only Workflow**

When tools are unavailable or disallowed:

1. Reason only from the material explicitly provided.
2. Do not claim to know unseen repository details.
3. State the minimum missing context that would most improve the answer.
4. Still provide the best useful answer or next step possible.

**Failure / Fallback Policy**

- If a tool is absent or disallowed, downgrade immediately.
- If a tool fails or times out, retry at most once when cheap.
- If failure persists, continue in degraded mode.
- Clearly separate verified findings from inferred conclusions.

**Output Format**

Return results using this structure:

1. Understanding
2. Mode Used
3. Missing Context
4. Plan / Answer
5. Assumptions
6. Evidence Level
7. Next Best Action

**Hard Prohibitions**

- Do not fabricate repository structure or tool results.
- Do not assume tools exist because of host branding.
- Do not over-explore when a small context set is enough.
- Do not use code compression as the first move.
- Do not hide uncertainty.

---

## 16. Conformance Checklist

An implementation conforms to this spec if:

1. It preserves the required output schema.
2. It supports tool-assisted and prompt-only operation.
3. It degrades gracefully under tool loss or restriction.
4. It preserves honesty about verification boundaries.
5. It follows the required context strategy order.
6. It remains useful in prompt-only mode.

## 17. Validation Against Evaluation

Any future skill implementation based on this spec should be tested against `EVALUATION.md`.

Minimum expectation:

- each acceptance claim from `DESIGN.md` must still be represented,
- the implementation must pass both tool-assisted and prompt-only cases,
- and the implementation must preserve the no-fabrication guarantee.

## 18. Next Implementation Step

After this spec, the next practical artifact should be one of the following:

1. a concrete skill file adapted to a specific host,
2. a host adapter note describing available tool classes,
3. or an evaluation harness that records transcripts and pass/fail judgments.

The recommended next step is to generate the first concrete skill draft from the template in Section 15.
