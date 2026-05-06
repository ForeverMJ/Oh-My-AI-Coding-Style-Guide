# OpenCode Skill Evaluation Run — 2026-05-06

## Purpose

This document records two paired OpenCode evaluations for the local `context-optimization` skill:

1. a **minimal sparse-repo** case in this repository, and
2. a **more realistic medium-repo** case in the local `opencode` repository.

The goal was not to prove that the skill always improves outputs. The goal was to measure whether invoking the skill is materially useful in practice, and under what conditions.

## 中文摘要

这次评估一共做了两组 OpenCode 对照测试：

1. 一个在当前仓库上的**最小稀疏仓库**案例。
2. 一个在本地 `opencode` 仓库上的**更接近真实开发**案例。

结论可以概括为：

- **在小而稀疏的仓库里，这个 skill 明显有用。**
  - skill 版减少了无关探索，避免了不必要的全仓扫描。
  - 最终答案质量接近，但 token 消耗更低。

- **在这次中等规模、真实代码仓库案例里，这个 skill 仍然有用，但收益方式不同。**
  - 它更像一种“上下文治理”和“范围收紧”工具。
  - 它帮助 agent 更强调最小安全改动面，少把无关内部实现纳入修改范围。
  - 但在这次 run 里，它**没有节省 token**，反而因为 skill 加载和额外检索，整体成本更高。

- **因此，从这两次 run 看，更稳定观察到的价值不是保证更便宜，而是让行为更克制、更不容易过度探索。**

如果把结论说得更实用一些：

- 当仓库较小、任务较窄、默认 agent 容易乱扫上下文时，这个 skill 的收益最明显。
- 在这次 medium-repo run 里，它的价值更偏“约束 agent 的工作方式”，而不是“稳定降低 token”。
- 如果要跨 repo 直接发现这个 skill，应装到全局或目标 repo；只放在当前项目的 `.opencode/skills/` 里，不会被其他仓库发现。

## Environment and Constraints

- Date: 2026-05-06
- Runner: local OpenCode CLI
- Output mode: `--format json`
- Permission mode: `--dangerously-skip-permissions`
- Primary execution lane: `opencode run --pure`

### Why `--pure` was used

Normal plugin mode in this environment still had an agent-resolution problem:

- default agent configured as `"Sisyphus - Ultraworker"`
- `opencode run` could not resolve that display name correctly

Because of that, these evaluations were intentionally run in **pure OpenCode mode** so host/plugin instability would not contaminate the skill verdict.

This plugin-mode issue was observed during setup validation in this session, but it is **not** part of the paired run provenance listed at the end of this document.

### Skill deployment locations used

- Project-local skill:
  - `.opencode/skills/context-optimization/SKILL.md`
- Global skill for cross-repo discovery:
  - `~/.config/opencode/skills/context-optimization/SKILL.md`

The global copy was needed because project-local skill discovery is scoped to the current repository tree.

## Repository Revisions

- `Oh-My-AI-Coding-Style-Guide`: `1ab23edd8257df47b79541bfeb0c64aeacd1ea2b`
- `opencode`: `a457828a67548288276f120de2fd5bf4e60baed9`

---

## Test Case 1 — Minimal Sparse Repository

### Repository

- Path: `/home/taotao/workspace/dev/Oh-My-AI-Coding-Style-Guide`
- Commit: `1ab23edd8257df47b79541bfeb0c64aeacd1ea2b`

### Prompt

> Analyze this repository and tell me what should be designed first for a context optimization skill. Keep the answer concise.

### Commands

#### Baseline

```bash
opencode run --pure --dir "/home/taotao/workspace/dev/Oh-My-AI-Coding-Style-Guide" --format json --dangerously-skip-permissions "Analyze this repository and tell me what should be designed first for a context optimization skill. Keep the answer concise."
```

#### Skill-assisted

```bash
opencode run --pure --dir "/home/taotao/workspace/dev/Oh-My-AI-Coding-Style-Guide" --format json --dangerously-skip-permissions "First use the skill tool to load the context-optimization skill. Then analyze this repository and tell me what should be designed first for a context optimization skill. Keep the answer concise."
```

### Observed behavior

#### Baseline

- Read `README.md`
- Read local skill wrapper file under `.opencode/skills/context-optimization/SKILL.md`
- Ran a broad `glob("**/*")`
  - this pulled in a large amount of irrelevant `.opencode/node_modules` content
- Read:
  - `SKILL_SPEC.md`
  - `DESIGN.md`
  - `SKILL.md`
  - `EVALUATION.md`

#### Skill-assisted

- Successfully loaded `context-optimization`
- Read repository directory listing
- Ran a narrow but low-yield `glob("**/*context*")`
- Read:
  - `README.md`
  - `SKILL_SPEC.md`
  - `DESIGN.md`
- Did **not** do the broad whole-repo glob that the baseline run did

### Final answers

#### Baseline

Recommended designing the core behavior contract first, specifically:

- mode/state model
- context decision policy order
- stable output contract

#### Skill-assisted

Reached the same core conclusion, but with slightly cleaner framing around:

- behavior contract first
- mode transitions
- decision policy
- stable output structure

### Token totals

- Baseline: `24397`
- Skill-assisted: `16148`

### Verdict

**Clear win for the skill in the sparse-repo case.**

The answer quality was similar, but the skill-assisted run was more context-disciplined and materially cheaper. The baseline run performed an unnecessary full-repo glob that dragged in irrelevant local package artifacts.

---

## Test Case 2 — Realistic Medium Repository

### Repository

- Path: `/home/taotao/workspace/dev/opencode`
- Commit: `a457828a67548288276f120de2fd5bf4e60baed9`

### Task selection rationale

This case was chosen because it is a realistic development-analysis task:

- it targets a real CLI behavior,
- it requires locating the relevant command path,
- it requires identifying the smallest safe fix surface,
- and it requires identifying the narrowest tests to add or run.

### Prompt

> Analyze the opencode repository and identify the smallest code and test changes needed so `opencode run --agent <subagent>` fails fast with a clear error instead of silently falling back to the default agent. Do not modify files. Keep the answer concise and include: (1) files to inspect or change, (2) why each matters, (3) the narrowest tests to run.

### Commands

#### Baseline

```bash
opencode run --pure --dir "/home/taotao/workspace/dev/opencode" --format json --dangerously-skip-permissions "Analyze the opencode repository and identify the smallest code and test changes needed so 'opencode run --agent <subagent>' fails fast with a clear error instead of silently falling back to the default agent. Do not modify files. Keep the answer concise and include: (1) files to inspect or change, (2) why each matters, (3) the narrowest tests to run."
```

#### Skill-assisted

```bash
opencode run --pure --dir "/home/taotao/workspace/dev/opencode" --format json --dangerously-skip-permissions "First use the skill tool to load the context-optimization skill. Then analyze the opencode repository and identify the smallest code and test changes needed so 'opencode run --agent <subagent>' fails fast with a clear error instead of silently falling back to the default agent. Do not modify files. Keep the answer concise and include: (1) files to inspect or change, (2) why each matters, (3) the narrowest tests to run."
```

### Important setup note

An initial attempt failed to load the skill because only a project-local copy existed under the style-guide repo. From inside the `opencode` repo, OpenCode did not discover it.

That was corrected by installing the same skill globally at:

```text
~/.config/opencode/skills/context-optimization/SKILL.md
```

After that, `context-optimization` loaded successfully inside the `opencode` repo.

### Ground truth code anchors

The task is real and grounded in observed code:

- `packages/opencode/src/cli/cmd/run.ts`
  - currently warns and falls back when `--agent` resolves to a subagent or unknown agent
- `packages/opencode/src/session/prompt.ts`
  - explains why `agent: undefined` becomes default-agent behavior
- `packages/opencode/src/agent/agent.ts`
  - source of truth for agent lookup and mode values

### Observed behavior

#### Baseline

The baseline run:

- started with a very broad grep for `--agent|agent` across the whole repo
- ran a broad `glob("**/*run*")`
- read:
  - `packages/opencode/src/cli/cmd/run.ts`
  - `packages/opencode/src/agent/agent.ts`
  - `packages/opencode/src/cli/cmd/cmd.ts`
  - `packages/opencode/test/cli/github-action.test.ts`
  - `packages/opencode/test/cli/github-remote.test.ts`
- globbed all test files under `packages/opencode/test/**/*.test.ts`
- used targeted grep afterward to confirm the exact fallback warning strings and look for existing `process.exit`-style test patterns

Its final recommendation was broadly reasonable:

- change `run.ts`
- add a focused `run-agent.test.ts`
- optionally run `agent.test.ts`

#### Skill-assisted

The corrected skill-assisted run:

- successfully loaded `context-optimization`
- still performed some broad search work early
- read:
  - `packages/opencode/src/cli/cmd/run.ts`
  - `packages/opencode/src/agent/agent.ts`
  - `packages/opencode/src/session/prompt.ts`
  - `packages/opencode/src/server/server.ts`
  - `packages/opencode/src/cli/cmd/cmd.ts`
  - `packages/opencode/test/cli/github-action.test.ts`
- also globbed CLI test paths and related test locations

Its final recommendation was comparable to the baseline answer, but slightly tighter in wording:

- change only `packages/opencode/src/cli/cmd/run.ts`
- add only `packages/opencode/test/cli/run-agent.test.ts`
- explicitly avoid changing session internals
- justify fail-fast behavior by reference to existing fail-fast patterns in `run.ts`

### Final answer comparison

#### Baseline final answer

- good diagnosis
- slightly wider exploration footprint
- included an optional refactor helper suggestion

#### Skill-assisted final answer

- comparable diagnosis
- slightly stronger emphasis on “smallest safe scope”
- better at rejecting unrelated internals as change targets

### Token totals

- Baseline: `27037`
- Skill-assisted: `31444`

### Verdict

**Mixed result in the medium-repo case.**

The corrected skill-assisted run reached a very similar final recommendation to the no-skill baseline, with only a marginal improvement in scope discipline. It did **not** reduce exploration cost in this run. It spent extra budget on skill loading and still executed several broad searches before converging.

So, for this realistic repository:

- **quality / scope discipline:** only marginally better with the skill
- **efficiency / token savings:** not better in this run

---

## Overall Conclusion

### When the skill was clearly useful

In the sparse-repo case, the skill was useful in a straightforward way:

- less irrelevant exploration
- lower token cost
- similar or slightly cleaner answer quality

### When the skill was only partially useful

In the medium-repo case, the skill was useful more as a **behavior constraint** than as an efficiency optimization:

- it improved the final scoping discipline
- it did not improve tool-call efficiency
- it did not reduce token cost in that run

### Practical takeaway

In these two runs, the current evidence suggests:

1. **Yes, invoking the skill can be useful.**
2. Its strongest value today is **context discipline and anti-overreach**, not guaranteed token reduction.
3. It looked most compelling when:
   - the repository is sparse or moderately sized,
   - the task is narrow,
   - and the default agent might otherwise over-explore.
4. For cross-repo usage, the skill should be installed globally or per target repo, not only in one project-local `.opencode/skills/` directory.

---

## Provenance

Relevant raw output captures from this run:

- Minimal sparse-repo baseline capture:
  - `/home/taotao/.local/share/opencode/tool-output/tool_dfd933410001lue82vy0iN3sCy`
  - baseline session inside that run: `ses_2026cfa96ffeuE9I6zDjN2gLFD`
- Minimal sparse-repo skill-assisted capture:
  - session: `ses_2026cfa97ffeYUNcU1qt000dzQ`
  - shared OpenCode log containing that run: `/home/taotao/.local/share/opencode/log/2026-05-06T135603.log`
- Realistic medium-repo no-skill baseline:
  - `/home/taotao/.local/share/opencode/tool-output/tool_dfd9398ce001Jg5ceIrAuK6JDC`
- Initial failed realistic skill load (project-local scope issue only, not the true baseline):
  - `/home/taotao/.local/share/opencode/tool-output/tool_dfd937d0500183GHU15qXv7ako`
- Corrected realistic skill-assisted run (global skill installed):
  - `/home/taotao/.local/share/opencode/tool-output/tool_dfd9608f9001hY6eYQKEIzWG76`

These transcripts are the primary evidence for the observations above.
