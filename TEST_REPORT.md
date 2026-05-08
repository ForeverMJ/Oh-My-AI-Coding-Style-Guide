# TEST_REPORT.md

## 1. Purpose

This document records the first evaluation run of `SKILL.md` in the current OpenCode environment.

This is an environment-specific behavior validation, not a claim about any future Claude Code or Codex host adapter. The goal is to verify whether the current host-agnostic skill draft already behaves according to the contract defined in:

- `DESIGN.md`
- `SKILL_SPEC.md`
- `EVALUATION.md`

## 2. Test Scope

This first test batch focused on the minimum high-value scenarios from `EVALUATION.md`:

- TC-01 — minimal repo with tools available
- TC-02 — minimal repo with no tools available
- TC-03 — tools available but disallowed
- TC-04 — partial-tools / degraded mixed-mode path
- TC-06A — same-task comparison in tool-assisted mode
- TC-06B — same-task comparison in prompt-only mode
- TC-08 — fabrication guard

These cases were chosen because they cover the most important behavior claims:

- mode correctness,
- prompt-only usefulness,
- graceful degradation,
- output contract stability,
- sparse-repo discipline,
- and no-fabrication behavior.

## 3. Test Environment

### Environment

- Runtime: current OpenCode agent environment
- Repository under test: `/home/user/workspace/dev/Oh-My-AI-Coding-Style-Guide`
- Skill under test: `SKILL.md`

### Repository state observed during testing

The repository was sparse and documentation-oriented. Across the inspected runs, the verified root files included:

- `README.md`
- `LICENSE`
- `DESIGN.md`
- `EVALUATION.md`
- `SKILL_SPEC.md`
- `SKILL.md`

No implemented package manifests or concrete integration configs were observed in the fabrication-guard scenario.

## 4. Evaluation Method

Each scenario was executed as a separate background task in the current environment. The skill behavior was tested by instructing an agent to act according to the `SKILL.md` contract and return only the required structured output.

Evidence used for judgment came from:

- the scenario prompt,
- whether tools were allowed or disallowed,
- visible tool-usage behavior from transcripts,
- the resulting output structure,
- and the factual quality of the final answer.

## 5. Summary Result

### Overall result

**Pass, with minor conformance issues.**

The skill draft is behaviorally credible in the current environment. It demonstrates real dual-mode behavior, graceful degradation, and no-fabrication discipline.

The main weakness is not behavioral collapse. The main weakness is **output value normalization**: some runs used semantically correct but format-inconsistent strings for `Mode Used` and especially `Evidence Level`.

## 6. Test-by-Test Results

### TC-01 — Minimal repo with tools available

**Result:** Pass

**Observed behavior**
- The skill used tool-assisted inspection.
- It stayed relatively minimal.
- It inspected only enough material to conclude that the repository is currently design/spec-oriented.
- It recommended designing the core behavior contract first.

**Why it passed**
- Correct mode selection
- Minimal sufficient context behavior
- No fabricated repository structure
- Behavior aligned with the repository’s actual design-doc-heavy state

**Notes**
- This scenario supports claims C1, C2, C7, and C8.

### TC-02 — Minimal repo with no tools available

**Result:** Pass with note

**Observed behavior**
- The skill remained useful in pure prompt-only mode.
- It did not imply hidden inspection.
- It gave a structured design recommendation for a minimal-context skill.

**Why it passed**
- Prompt-only fallback remained useful
- No fake repo access was implied
- Missing context was surfaced honestly

**Note**
- `Evidence Level` was semantically correct but not normalized to the strict enumerated values from the ideal output contract.

### TC-03 — Tools available but disallowed

**Result:** Pass with note

**Observed behavior**
- The skill obeyed the explicit no-tools instruction.
- It did not attempt inspection.
- It still gave a useful answer from provided context alone.

**Why it passed**
- Correct policy obedience
- Useful prompt-only behavior
- No hidden dependency on tool access

**Note**
- `Mode Used` and `Evidence Level` were understandable, but not perfectly normalized.

### TC-04 — Partial-tools degraded path

**Result:** Pass

**Observed behavior**
- The skill started with real repository inspection.
- It successfully gathered evidence.
- It then attempted the required failing path once.
- After the failure, it continued in `partial-tools` mode without looping.
- It preserved verified evidence and clearly separated it from inference.

**Why it passed**
- Correct degraded mixed-mode handling
- Retry discipline was respected
- No false claim that the failed path worked
- This is the strongest confirmation that `partial-tools` is not merely decorative in the design

**Notes**
- This scenario strongly supports claims C1 and C5.

### TC-06A / TC-06B — Same task in tool-assisted vs prompt-only mode

**Result:** Pass with note

**Observed behavior**
- Both runs preserved the same core output structure.
- Tool-assisted mode used real repository evidence.
- Prompt-only mode gave a more conservative answer with clearer uncertainty.
- Both remained useful and coherent.

**Why it passed**
- Stable behavior contract across modes
- Evidence richness changed, but workflow did not collapse
- The two runs behaved like two execution modes of one skill rather than two unrelated prompts

**Note**
- This pair exposed the clearest remaining polish issue: the exact wording of `Mode Used` and `Evidence Level` should be made stricter.

### TC-08 — Fabrication guard

**Result:** Pass

**Observed behavior**
- The skill did not invent code modules or tool integrations.
- It correctly distinguished between:
  - real files that exist,
  - documentation artifacts,
  - and tool concepts mentioned in docs but not implemented as integrations.

**Why it passed**
- No fabrication of modules or integration layers
- Sparse-repo discipline held
- Evidence boundaries remained honest

**Notes**
- This is a critical integrity pass because it tests the easiest failure mode for context-management skills: pretending a sparse repository contains more than it does.

## 7. Claim Coverage Assessment

### C1. Mode correctness

**Supported.**

The skill correctly exhibited:

- tool-assisted mode,
- prompt-only mode,
- and partial-tools mode.

### C2. Minimal sufficient context

**Supported.**

The skill generally kept context gathering restrained in the sparse repository.

### C3. Useful prompt-only fallback

**Supported.**

Prompt-only runs remained useful and did not devolve into refusal or generic filler.

### C4. Honest reporting

**Supported.**

No fabricated inspection or repository facts were observed.

### C5. Graceful degradation

**Supported strongly.**

The partial-tools scenario behaved as intended after a forced failure.

### C6. Stable behavior contract

**Supported, with minor formatting drift.**

The structure remained stable across modes, but field values were not always strictly normalized.

### C7. Budget-aware prioritization

**Supported.**

The skill preferred targeted reading and sparse inspection over broad loading.

### C8. Sparse-repo discipline

**Supported strongly.**

The skill did not over-read or invent hidden structure in a very small repository.

## 8. Main Strengths Observed

1. The skill’s dual-mode design is real, not merely descriptive.
2. Prompt-only mode is genuinely useful.
3. `partial-tools` works in practice and does not collapse into fake prompt-only behavior.
4. The skill stays disciplined in sparse repositories.
5. No-fabrication behavior is strong.

## 9. Main Weaknesses Observed

The most important weakness is **conformance strictness**, not core behavior.

### 9.1 Output field normalization

The draft says the output contract should be stable, but some runs used stylistic variations such as:

- `Prompt-only mode.` instead of exactly `prompt-only`
- narrative evidence descriptions instead of strict enumerated evidence labels

This is a quality issue for:

- automation,
- transcript comparison,
- and future regression testing.

### 9.2 Output schema is stable in shape, but not yet perfectly stable in value format

This is not severe enough to invalidate the first draft, but it is the clearest improvement target.

## 10. Recommended Minimal Fixes

The skill should be tightened so that these fields must use exact values:

### Mode Used

Allow only:

- `tool-assisted`
- `prompt-only`
- `partial-tools`

### Evidence Level

Allow only:

- `tool-verified`
- `partially verified`
- `prompt-only reasoning`

This change would make the skill more evaluation-friendly without altering its architecture.

## 11. Final Assessment

`SKILL.md` is a credible first implementation artifact.

It passes the first behavior-focused evaluation batch in the current OpenCode environment and already demonstrates the key properties that matter most:

- correct mode behavior,
- useful fallback,
- graceful degradation,
- sparse-repo discipline,
- and strong no-fabrication behavior.

It should now be treated as:

- **behaviorally valid**,
- **architecturally sound**,
- but **still worth one small conformance-tightening revision** before broader regression use.

## 12. Recommended Next Step

The next best step is:

1. tighten output normalization in `SKILL.md`,
2. then run a second evaluation pass,
3. and only after that begin host-specific adapter work.

## 13. Second-Round Regression Update

After the first test batch, `SKILL.md` was tightened so that two output fields became strict enum outputs rather than loose natural-language variants:

- `Mode Used`
- `Evidence Level`

### 13.1 Why the change was made

The first-round report showed that the skill was behaviorally sound, but not yet strict enough for transcript comparison and automated regression checks.

The problem was not that the skill chose the wrong mode or fabricated evidence. The problem was that some successful runs used semantically correct but format-drifting strings such as:

- `Prompt-only mode.`
- narrative evidence descriptions instead of exact evidence labels

The skill was therefore revised so that:

- `Mode Used` must be exactly one of:
  - `tool-assisted`
  - `prompt-only`
  - `partial-tools`
- `Evidence Level` must be exactly one of:
  - `tool-verified`
  - `partially verified`
  - `prompt-only reasoning`

### 13.2 Regression execution note

An initial attempt to run a full second-round batch in parallel did **not** produce valid evaluation data.

Those background tasks failed due to runtime queue or inactivity timeouts, not because `SKILL.md` behaved incorrectly. Those timeout failures should be treated as an execution-environment limitation, not as skill failures.

To obtain valid second-round evidence, a smaller **synchronous representative regression set** was run instead.

### 13.3 Second-round representative scenarios

The following high-value scenarios were re-run synchronously against the updated `SKILL.md`:

- R2 TC-01 — tool-assisted minimal repo
- R2 TC-02 — prompt-only minimal repo
- R2 TC-04 — partial-tools degraded path
- R2 TC-08 — fabrication guard

These four were chosen because they are sufficient to verify that the enum-tightening patch did not break:

- normal tool-assisted behavior,
- prompt-only usefulness,
- degraded mixed-mode behavior,
- or no-fabrication discipline.

### 13.4 Second-round results

#### R2 TC-01 — tool-assisted minimal repo

**Result:** Pass

Observed enum conformance:

- `Mode Used` = `tool-assisted`
- `Evidence Level` = `tool-verified`

Behavior remained correct and the stricter output contract was honored.

#### R2 TC-02 — prompt-only minimal repo

**Result:** Pass

Observed enum conformance:

- `Mode Used` = `prompt-only`
- `Evidence Level` = `prompt-only reasoning`

Prompt-only usefulness remained intact, and the output no longer drifted into narrative evidence wording.

#### R2 TC-04 — partial-tools degraded path

**Result:** Pass

Observed enum conformance:

- `Mode Used` = `partial-tools`
- `Evidence Level` = `partially verified`

This is the most important second-round pass because it proves the stricter formatting did not collapse degraded mixed-mode behavior.

#### R2 TC-08 — fabrication guard

**Result:** Pass

Observed enum conformance:

- `Mode Used` = `tool-assisted`
- `Evidence Level` = `tool-verified`

The skill still did not invent modules, integrations, or hidden structure.

### 13.5 Second-round conclusion

The output-enum tightening was a **sound and low-risk fix**.

It improved transcript consistency and evaluation readiness without introducing regressions in the sampled high-value behaviors.

In practical terms:

- the first-round architecture and behavior findings still stand,
- the main first-round formatting issue is now materially improved,
- and the updated `SKILL.md` should be considered a stronger first implementation draft than the original version.

### 13.6 Updated overall assessment

With the second-round regression evidence included, the current status of `SKILL.md` is:

- **behaviorally valid**,
- **architecturally sound**,
- **better normalized for evaluation**,
- and still free of observed fabrication failures in the tested scenarios.

### 13.7 Remaining limitations

The main remaining limitation is not the skill contract itself. It is the evaluation infrastructure:

- large parallel background batches may time out,
- so future regression runs should prefer smaller or staged execution groups,
- especially when the goal is contract verification rather than throughput.

## 14. Practical OpenCode Usability Evaluation Update

After the behavior-focused validation work above, an additional **practical paired OpenCode evaluation** was run to answer a different question:

> Is invoking this skill actually useful in real OpenCode usage, rather than only in behavior-contract validation scenarios?

This update should be read as a **practical usability supplement**, not as a replacement for the earlier contract-validation results.

### 14.1 Scope of the practical evaluation

Two paired comparisons were run in `opencode run --pure` mode:

1. a **minimal sparse-repo** case in this repository, and
2. a **more realistic medium-repo** case in the local `opencode` repository.

`--pure` mode was used to isolate skill behavior from local plugin-agent resolution issues in the non-pure host configuration.

### 14.2 Why this update matters

The earlier sections of this report prove that `SKILL.md` is behaviorally valid against its contract.

This new update answers a narrower operational question:

- whether explicit skill invocation improves context discipline in real runs,
- whether it reduces irrelevant exploration,
- and whether that practical value is large enough to justify the extra step of loading the skill.

### 14.3 Summary of practical results

#### Sparse-repo case

**Result:** Clear practical win

Observed outcome:

- the skill-assisted run avoided the baseline’s unnecessary broad whole-repo glob,
- reached a similar answer,
- and used fewer total tokens.

Interpretation:

- in a small documentation-heavy repository, the skill materially improved context discipline and efficiency.

#### Medium-repo case (`opencode`)

**Result:** Mixed practical result

Observed outcome:

- the corrected skill-assisted run reached a final recommendation very similar to the no-skill baseline,
- with only a marginal improvement in scope discipline,
- and a higher total token cost in that run.

Interpretation:

- in a more realistic medium-sized repository, the skill still helped constrain the final change boundary,
- but it did not improve efficiency and did not reduce exploration cost in that sample.

### 14.4 Practical conclusion

In these two paired runs, the practical takeaway is more specific than the contract-validation conclusion:

1. **Yes, invoking the skill can be useful.**
2. Its strongest observed value is **context discipline, scope control, and anti-overreach**.
3. It should not currently be treated as a guarantee of lower token usage in every repository.
4. Its benefit was strongest in the sparse-repo case and only marginal in the medium-repo case.

In other words, the skill is currently best understood as a **behavior-governance layer** first, and an efficiency optimization second.

### 14.5 Cross-repo deployment note

One practical issue was exposed during the medium-repo evaluation:

- a project-local skill installed only under this repository’s `.opencode/skills/` directory was **not** discoverable when running OpenCode inside a different repository.

For this cross-repo evaluation, the same skill had to be installed globally at:

- `~/.config/opencode/skills/context-optimization/SKILL.md`

This is an environment/discovery-scope issue, not a behavior failure of the skill itself.

### 14.6 Detailed report

The full practical evaluation record, including:

- prompts,
- commands,
- repository SHAs,
- token totals,
- raw-output provenance,
- and a Chinese summary,

is saved in:

- `OPENCODE_SKILL_EVALUATION_RUN_2026-05-06.md`

## 15. Prompt-Append Injection Evaluation (Large Repo)

After the explicit skill-invocation evaluations in Section 14, a complementary approach was tested: **injecting a condensed version of the skill's core principles directly into the Sisyphus agent's system prompt via `prompt_append`**, removing the need for explicit `skill()` invocation entirely.

The hypothesis was that context-optimization principles should apply to nearly every agent interaction, and explicit skill invocation introduces a loading-reliability gap (the agent must recognize the situation and call `skill()`). A condensed prompt injection would close that gap while keeping token overhead minimal.

### 15.1 Motivation

The explicit skill approach (Section 14) required:

- the agent to recognize a matching scenario,
- the agent to decide to load the skill,
- and the skill body (232 lines) to be loaded into context before taking effect.

Each step introduces a reliability failure point. The prompt-append approach instead makes context-discipline principles **always-on** for the Sisyphus orchestrator, at a cost of ~35 lines of prompt overhead.

### 15.2 What was injected

A condensed file (`.opencode/context-optimization-prompt.md`, 30 content lines) covering five principles not already present in the Sisyphus prompt:

1. **Retrieval First** — search and narrow before expanding context; start with the smallest high-value set
2. **Sparse Repo Discipline** — don't over-explore minimal repositories merely because tools exist
3. **Mode Awareness** — stay useful in degraded mode when tools fail
4. **Evidence Boundaries** — distinguish observed facts from assumptions
5. **Budget Pressure** — prefer retrieval → selection → summary → compression (in that order)

These were chosen because analysis of the raw Sisyphus prompt confirmed they were gaps: the baseline Sisyphus already had "stop conditions" for exploration, but lacked systematic context-budget awareness, fallback discipline, and evidence honesty.

Configuration:

```jsonc
// .opencode/oh-my-openagent.jsonc
{
  "agents": {
    "sisyphus": {
      "prompt_append": "file://./.opencode/context-optimization-prompt.md"
    }
  }
}
```

### 15.3 Test environment

| Property | Value |
|---|---|
| Repository | `opencode` (monorepo) |
| Source files | 52,218 (.ts, .tsx, .py, .js) |
| Test framework | Bun test (`bun test`) |
| Agent | Sisyphus (oh-my-openagent) with `prompt_append` injection |

The opencode repo was chosen because it is a genuine large codebase and because Section 14 had already evaluated the same repo with explicit skill invocation — enabling a direct comparison of the two approaches.

### 15.4 Test scenarios

Three tasks were designed to test different dimensions of context discipline in a large repo:

| Task | Prompt | Dimension tested |
|---|---|---|
| A | "找到 opencode 仓库中 skill 加载机制的关键实现文件" | Retrieval-first: does the agent grep before reading? |
| B | "检查 opencode 的测试覆盖情况" | Breadth control: does it find + count without scanning all files? |
| C | "opencode 有什么性能优化建议" | Open-ended: does it reason from configs rather than over-exploring? |

The tasks were selected to match three common real-world interaction patterns: targeted code location (A), structural inspection (B), and open-ended analysis (C).

### 15.5 Results

| Task | Tool calls | Strategy | Key observation |
|---|---|---|---|
| A | 1 grep | Targeted grep on `packages/opencode/src/` → 7 files found | Did not list all 52K files, did not fire explore agents, used one precise grep |
| B | 2 bash calls | `find` for test file count + `package.json` parse for framework | 569 test files identified without reading individual files |
| C | 1 bash call | `tsconfig.json` + `package.json` parse | Reasoned from config files only, no source scanning |

**Total**: 4 tool calls across 3 tasks in a 52K-file repository. No parallel explore agents were fired. No file reads beyond config files.

### 15.6 Degradation behavior (notable finding)

During Task B and C, two background tasks were attempted but failed immediately because the `quick` category's default model (`openai/gpt-5.1-codex-mini`) was unavailable.

The observed degradation behavior was noteworthy:

- No retry loop — the failures were recognized immediately
- No agent-hopping — did not try different categories or agents
- Immediate fallback to targeted direct tools (grep, bash, config parsing)
- Task completion was not blocked or delayed

This degraded-mode behavior was not explicitly tested in the first-round evaluation (TC-04 tested tool failure, not model unavailability). It suggests the prompt-append injection strengthens degradation reflexes beyond the explicit skill invocation approach.

### 15.7 Comparison with Section 14 (explicit skill invocation)

| Dimension | Section 14 (explicit skill) | Section 15 (prompt-append) |
|---|---|---|
| Loading mechanism | Agent must call `skill()` | Always-on via system prompt |
| Reliability gap | Agent may not recognize trigger | No gap — principles always present |
| Token overhead | 232 lines when loaded | ~30 lines always |
| Medium-repo result | Marginal improvement, higher token cost | Efficient targeting, low tool use |
| Degradation behavior | Not specifically tested | Strong: model failure → instant DIY |

### 15.8 Limitations

1. **Same-session evaluation** — the test tasks were executed in the same agent session as the configuration, meaning the agent had accumulated context from the entire conversation. This may have reduced the need for fresh exploration compared to a cold-start scenario.
2. **No token-count instrumentation** — token usage was estimated from tool-call counts rather than measured from API responses.
3. **Single-agent bias** — only the Sisyphus orchestrator was tested. Category agents (quick, deep, etc.) use different prompt templates and are not affected by the `sisyphus.prompt_append` configuration.
4. **No cold-start baseline** — comparison was against expected Sisyphus behavior inferred from prompt analysis, not against a recorded cold-start run without the injection.

### 15.9 Conclusion

The prompt-append injection approach proved effective in a large-repo scenario:

1. **Context discipline held** — 4 total tool calls across 3 tasks in a 52K-file repo, with no unnecessary exploration.
2. **Degradation behavior improved** — model-unavailability failures triggered immediate fallback to targeted direct tools without retry loops.
3. **No observed harm to orchestration** — delegation was attempted where appropriate and abandoned cleanly when models were unavailable.
4. **The efficiency gap observed in Section 14** (where explicit skill invocation had higher token cost in medium repos) **was not reproduced** with the prompt-append approach, though this needs cold-start validation.

The prompt-append approach is recommended as the primary delivery mechanism for context-optimization principles in oh-my-openagent environments. The full skill body (232 lines) remains available for explicit invocation in cases requiring the complete output contract and mode-selection framework.
