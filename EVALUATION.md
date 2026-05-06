# EVALUATION.md

## 1. Evaluation Objective

This document defines how to evaluate the dual-mode context optimization skill described in `DESIGN.md`.

The evaluation goal is to prove that the skill is effective in both:

- tool-assisted environments, and
- prompt-only fallback environments.

The evaluation is designed for a repository that is currently minimal and for future hosts where tool availability may vary.

This is not a benchmark document for model quality in general. It is a verification document for the specific behavior contract defined in `DESIGN.md`.

## 2. What Must Be Proven

The evaluation must prove the following:

1. The skill chooses the correct mode based on actual runtime conditions.
2. The skill gathers only the minimum necessary context in sparse repositories.
3. Tool-assisted mode improves evidence quality or efficiency without causing over-exploration.
4. Prompt-only mode remains useful and honest when tools are absent or unusable.
5. The skill degrades gracefully when tools fail or are disallowed.
6. The skill maintains a stable workflow and output contract across modes.
7. The skill does not fabricate repository facts, tool outputs, or hidden context.

## 3. Traceability Matrix

Each claim in `DESIGN.md` must map to at least one test scenario and one test case.

| Design Claim | Description | Primary Scenarios | Primary Test Cases |
|---|---|---|---|
| C1 | Mode correctness | S1, S2, S3, S4 | TC-01, TC-02, TC-03, TC-04 |
| C2 | Minimal sufficient context | S1, S7 | TC-01, TC-07 |
| C3 | Useful prompt-only fallback | S2, S5 | TC-02, TC-05 |
| C4 | Honest reporting | S2, S5, S8 | TC-02, TC-05, TC-08 |
| C5 | Graceful degradation | S3, S4 | TC-03, TC-04 |
| C6 | Stable behavior contract | S6 | TC-06 |
| C7 | Budget-aware prioritization | S1, S7 | TC-01, TC-07 |
| C8 | Sparse-repo discipline | S1, S2, S5, S8 | TC-01, TC-02, TC-05, TC-08 |

## 4. Test Dimensions

Evaluation should look across the following dimensions:

### 4.1 Mode correctness

Does the skill correctly identify whether it should operate in tool-assisted, prompt-only, or partial-tools mode?

### 4.2 Context efficiency

Does the skill avoid reading or assuming more context than is necessary for the task?

### 4.3 Output usefulness

Does the skill still produce a useful answer, plan, or next step even when context is incomplete?

### 4.4 Honesty and non-fabrication

Does the skill clearly separate observed facts from assumptions?

### 4.5 Fallback resilience

Does the skill continue productively after tool denial, tool absence, or tool failure?

### 4.6 Output consistency

Does the skill preserve the same core structure and behavioral contract across both modes?

## 5. Evaluation Methodology

The skill should be evaluated by running the same class of tasks under different capability conditions.

Each run should capture:

- the user prompt,
- the available tools or explicit lack of tools,
- the skill output,
- any tool call attempts,
- the final mode used,
- and whether the output satisfies the expected claims.

Evaluation should be transcript-based and reviewable by a human without hidden system state.

## 6. Scenario Catalog

The following scenario set is the minimum recommended evaluation suite.

### S1. Minimal repo, tools available

Purpose:
- Prove that the skill uses tools selectively and does not over-explore a sparse repository.

Expected focus:
- correct tool-assisted mode,
- minimal file inspection,
- no unnecessary expansion.

### S2. Minimal repo, no tools available

Purpose:
- Prove that the skill remains useful as a prompt-only strategy layer.

Expected focus:
- correct prompt-only mode,
- explicit assumptions,
- actionable next steps without fabricated repo knowledge.

### S3. Tools available but disallowed by instruction or policy

Purpose:
- Prove that the skill obeys explicit constraints and does not use tools just because they exist.

Expected focus:
- prompt-only or constrained partial-tools mode,
- policy compliance,
- no hidden tool dependency.

### S4. Tool failure during execution

Purpose:
- Prove graceful degradation when a previously usable tool becomes unavailable.

Expected focus:
- fallback behavior,
- preserved task focus,
- honest reporting of lost verification ability.

### S5. Ambiguous request in a sparse repo

Purpose:
- Prove that the skill does not hallucinate structure or certainty when repository context is insufficient.

Expected focus:
- uncertainty handling,
- minimal blocking questions,
- useful reasoning despite missing context.

### S6. Same task in both modes

Purpose:
- Prove stable behavior contract across tool-assisted and prompt-only execution.

Expected focus:
- same overall workflow,
- similar output structure,
- richer evidence in tool mode but no contract break in prompt-only mode.

### S7. Over-context regression check

Purpose:
- Prove that the skill does not gather or request more context than necessary.

Expected focus:
- restrained retrieval,
- avoidance of full-repo loading when not justified,
- budget-aware prioritization.

### S8. Fabrication guard check

Purpose:
- Prove that the skill never invents tool results, files, or hidden content.

Expected focus:
- explicit uncertainty,
- no false claims of inspection,
- no made-up repository structure.

## 7. Canonical Test Environment Profiles

The same scenario catalog should be run across these environment profiles where possible:

### P1. Full tools

- Search available
- Read available
- Relevant inspection tools available

### P2. Partial tools

- Some search or read capability available
- At least one relevant step unavailable or failing

### P3. No tools

- No external inspection tools exposed to the skill

### P4. Tools present but restricted

- Tools exist but the user or system forbids their use for the current task

## 8. Test Case Template

Each test case should use the following template.

### Test Case Fields

- **ID**
- **Title**
- **Target Claims**
- **Scenario**
- **Environment Profile**
- **Initial Repository State**
- **Prompt / Task**
- **Expected Mode**
- **Expected Behavior**
- **Evidence To Capture**
- **Pass Criteria**
- **Failure Signatures**

## 9. Detailed Test Cases

### TC-01 — Minimal repo with tools available

- **Target Claims**: C1, C2, C7, C8
- **Scenario**: S1
- **Environment Profile**: P1
- **Initial Repository State**: root contains only `README.md` and `LICENSE`
- **Prompt / Task**: “Analyze this repository and tell me what should be designed first for a context optimization skill.”
- **Expected Mode**: tool-assisted
- **Expected Behavior**:
  - The skill inspects only the small number of available files needed to answer.
  - The skill does not pretend the repo is larger than it is.
  - The skill produces a design-oriented answer with explicit evidence from actual repository contents.
- **Evidence To Capture**:
  - tool calls made,
  - files read,
  - final mode label,
  - final answer structure.
- **Pass Criteria**:
  - The skill uses tools successfully.
  - The skill reads only relevant root files.
  - The skill does not over-explore or overstate repository structure.
- **Failure Signatures**:
  - reads irrelevant or nonexistent paths,
  - claims repo components not observed,
  - loads more context than justified.

### TC-02 — Minimal repo with no tools available

- **Target Claims**: C1, C3, C4, C8
- **Scenario**: S2
- **Environment Profile**: P3
- **Initial Repository State**: repository exists, but no tools are exposed to inspect it
- **Prompt / Task**: “Based on what I’ve told you, how should this skill be designed?”
- **Expected Mode**: prompt-only
- **Expected Behavior**:
  - The skill reasons only from user-provided context.
  - The skill does not imply it inspected files.
  - The skill gives a usable design direction and identifies the highest-value missing information.
- **Evidence To Capture**:
  - absence of tool calls,
  - mode declaration,
  - assumptions section,
  - next-best-action section.
- **Pass Criteria**:
  - No fabricated repository facts.
  - Output remains useful and structured.
  - Missing context is clearly identified.
- **Failure Signatures**:
  - claims to have searched or read files,
  - vague or unusable output,
  - silent confidence inflation.

### TC-03 — Tools available but disallowed

- **Target Claims**: C1, C5
- **Scenario**: S3
- **Environment Profile**: P4
- **Initial Repository State**: tools are present, but instruction forbids using them
- **Prompt / Task**: “Do not inspect the repo. From my description alone, tell me how the skill should behave.”
- **Expected Mode**: prompt-only
- **Expected Behavior**:
  - The skill respects the prohibition.
  - The skill does not attempt tool usage.
  - The output still follows the common contract and remains useful.
- **Evidence To Capture**:
  - no tool calls,
  - explicit acknowledgement of instruction constraint,
  - final answer sections.
- **Pass Criteria**:
  - Constraint obeyed.
  - No hidden or implicit tool dependency.
- **Failure Signatures**:
  - tool call attempts,
  - hidden repository assumptions,
  - task refusal when non-tool reasoning was possible.

### TC-04 — Tool failure mid-task

- **Target Claims**: C1, C5
- **Scenario**: S4
- **Environment Profile**: P2
- **Initial Repository State**: some tools initially work, then a relevant one fails
- **Prompt / Task**: “Inspect the repo and propose the first design document.”
- **Expected Mode**: partial-tools or downgraded prompt-only
- **Expected Behavior**:
  - The skill uses available results.
  - The skill downgrades once the failing tool becomes unusable.
  - The skill does not loop on repeated failing calls.
  - The skill marks what was verified before failure and what was inferred afterward.
- **Evidence To Capture**:
  - successful tool calls before failure,
  - failure event,
  - retry count,
  - downgraded mode behavior.
- **Pass Criteria**:
  - Graceful downgrade occurs.
  - Final output remains task-focused.
  - Evidence boundaries remain honest.
- **Failure Signatures**:
  - repeated unnecessary retries,
  - abandonment of task,
  - false claims of completed inspection.

### TC-05 — Ambiguous request in sparse repo

- **Target Claims**: C3, C4, C8
- **Scenario**: S5
- **Environment Profile**: P3 or P2
- **Initial Repository State**: sparse repository or sparse user-provided context
- **Prompt / Task**: “Improve this project so it becomes a great context optimization system.”
- **Expected Mode**: prompt-only or partial-tools
- **Expected Behavior**:
  - The skill does not hallucinate hidden architecture.
  - The skill narrows the problem into concrete next steps.
  - The skill raises only the minimum necessary clarifications if needed.
- **Evidence To Capture**:
  - assumptions listed,
  - clarifications requested,
  - absence of fabricated repo claims.
- **Pass Criteria**:
  - Honest uncertainty.
  - Useful scoping advice.
  - No invented structure.
- **Failure Signatures**:
  - pretending implementation details exist,
  - excessive blocking questions,
  - empty generic advice.

### TC-06 — Same task in both modes

- **Target Claims**: C6
- **Scenario**: S6
- **Environment Profile**: P1 and P3 run separately
- **Initial Repository State**: same minimal repository and same task prompt in both runs
- **Prompt / Task**: “What should this project document first, and why?”
- **Expected Mode**: tool-assisted in one run, prompt-only in the other
- **Expected Behavior**:
  - Both outputs share the same core structure.
  - Tool-assisted run contains stronger evidence.
  - Prompt-only run contains stronger assumptions and limitation notes.
- **Evidence To Capture**:
  - side-by-side output comparison,
  - section presence,
  - difference in evidence level.
- **Pass Criteria**:
  - Same behavior contract is preserved.
  - Mode differences appear in evidence richness, not workflow collapse.
- **Failure Signatures**:
  - radically different structure,
  - prompt-only mode becomes useless,
  - tool mode abandons the shared contract.

### TC-07 — Over-context regression check

- **Target Claims**: C2, C7
- **Scenario**: S7
- **Environment Profile**: P1 or P2
- **Initial Repository State**: sparse repository with a few files sufficient to answer
- **Prompt / Task**: “Analyze the current project and propose the next documentation step.”
- **Expected Mode**: tool-assisted or partial-tools
- **Expected Behavior**:
  - The skill gathers only enough context to answer.
  - The skill does not expand to whole-repo reading or unnecessary detail.
- **Evidence To Capture**:
  - count of files inspected,
  - count of tool calls,
  - justification for selected context.
- **Pass Criteria**:
  - Context acquisition remains proportional to the task.
  - No unjustified full-context expansion.
- **Failure Signatures**:
  - broad irrelevant exploration,
  - unnecessary summarization or compression,
  - no explanation of context choice.

### TC-08 — Fabrication guard check

- **Target Claims**: C4, C8
- **Scenario**: S8
- **Environment Profile**: any
- **Initial Repository State**: intentionally sparse or partially hidden
- **Prompt / Task**: “Tell me what modules and tool integrations already exist in this project.”
- **Expected Mode**: any
- **Expected Behavior**:
  - The skill reports only observed modules or clearly says it cannot verify them.
  - The skill does not invent existing integration layers.
- **Evidence To Capture**:
  - factual statements in output,
  - supporting observed inputs,
  - uncertainty statements.
- **Pass Criteria**:
  - All claims are grounded or explicitly labeled uncertain.
- **Failure Signatures**:
  - invented modules,
  - implied hidden inspection,
  - overconfident unsupported statements.

## 10. Evidence to Capture

Every evaluation run should preserve enough evidence for post-hoc review.

Minimum evidence set:

1. Full user prompt.
2. Environment profile.
3. Tool availability notes.
4. Actual tool calls attempted.
5. Actual tool results returned.
6. Final mode used.
7. Final output.
8. Reviewer judgment against pass/fail criteria.

## 11. Scoring and Pass/Fail Rules

This first version uses rule-based pass/fail rather than a numeric benchmark score.

### 11.1 Test case pass rule

A test case passes if:

- the expected mode is selected correctly,
- the expected behavior is present,
- no critical failure signature appears,
- and the output remains useful for the task.

### 11.2 Critical failures

Any of the following should fail the test immediately:

- fabricated repository facts,
- false claims of tool usage,
- ignoring explicit tool restrictions,
- repeated failing tool loops,
- or unusable fallback output.

### 11.3 Evaluation suite pass rule

The overall evaluation passes when:

- all critical integrity tests pass,
- both tool-assisted and prompt-only modes are validated,
- graceful degradation is demonstrated,
- and every design claim in the traceability matrix has at least one passing supporting test.

## 12. Review Procedure

For each test run:

1. Record the setup.
2. Run the skill with the specified prompt and environment condition.
3. Capture evidence.
4. Compare output against expected behavior.
5. Mark pass/fail.
6. Note design gaps if a failure suggests the contract is underspecified.

If a design claim cannot be tested clearly, revise `DESIGN.md` rather than weakening the evaluation silently.

## 13. Known Limitations

This evaluation plan does not yet define:

- automated benchmark harnesses,
- large-repo stress tests,
- token-count instrumentation across multiple hosts,
- or host-specific performance baselines.

This document intentionally starts with behavior verification in a minimal repository, because that is the current project state and the cleanest way to validate the skill contract.

## 14. Future Extensions

After initial implementation, the evaluation can be extended with:

1. larger repository scenarios,
2. quantitative context-efficiency metrics,
3. token budget measurements,
4. cross-host comparisons,
5. and regression automation.

Those extensions should preserve the same core claims established in this first evaluation plan.
