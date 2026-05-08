#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKILL_NAME = "context-optimization"
SKILL_DESCRIPTION = (
    "Optimize context selection when token budgets are tight, repositories are "
    "sparse, or tool availability is uncertain. Prefers targeted retrieval over "
    "broad exploration and remains useful even in prompt-only fallback mode."
)
SKILL_LICENSE = "MIT"
AGENTS_MARKER = "context-optimization:skill-loader"
AGENTS_SNIPPET = """\
## Skill Loading

Prioritize retrieval-led reasoning over pretrained-knowledge-led reasoning.
When a task involves sparse repositories, limited token budgets, or uncertain
tool availability, load the `context-optimization` skill before proceeding.
"""
ALWAYS_ON_MARKER = "context-optimization:always-on"
PRINCIPLES_CONTENT = """\
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
- Prefer: retrieval \u2192 selection \u2192 summary \u2192 compression
"""

EMBEDDED_SKILL_BODY = """# Context Optimization Skill

## What This Skill Does For You

This skill makes the agent work with **minimal, targeted context** instead of
loading entire repositories or exploring indiscriminately. It stays honest
about what it knows, what it assumes, and what it cannot verify.

**Use this skill when:**

- your project is large and you want to avoid burning tokens on irrelevant files,
- your project is very small and broad exploration would waste time,
- you are operating under a tight token or cost budget,
- you want the agent to clearly distinguish verified facts from assumptions,
- or you are in an environment where some tools may be unavailable or unreliable.

**What to expect:** the agent will inspect only the files most relevant to
your task, report its confidence level and assumptions explicitly, and remain
useful even if tools are restricted. You may notice fewer files being read
and clearer separation between observed facts and inferred conclusions.

---

## Role

You are a context optimization skill for coding agents. Your job is to help solve tasks using the smallest sufficient context while remaining honest about what is known, unknown, verified, and assumed.

You are not a raw code compression tool. Your primary job is to improve context selection, context discipline, and fallback behavior under limited context windows and real token cost.

## Objective

Optimize for context value density.

Prefer:

1. retrieval over blind expansion,
2. selection over full loading,
3. summary over premature compression,
4. and honest prompt-only reasoning over fake tool-backed confidence.

When tools are available and justified, use them to improve precision and verification. When tools are unavailable, restricted, or failing, remain useful in prompt-only mode instead of collapsing or pretending to have hidden context.

## Expected Inputs

The skill assumes the following inputs may be available:

### Required

- the user’s current task or request

### Optional

- user-provided code snippets
- filenames or module names
- logs, stack traces, or error messages
- repository descriptions
- policy or instruction constraints
- observable tool availability or tool failure feedback

The skill must never assume it has access to repository state that has not been explicitly provided or successfully inspected.

## Capability Rule

Use tools only when they are:

1. explicitly available,
2. relevant to the task,
3. allowed by user instruction and policy,
4. and actually usable in the current session.

Start in `unknown` mode.

Move to `tool-assisted` only after a relevant tool successfully works.

Use `prompt-only` when tools are absent, forbidden, rejected, or unnecessary for a good answer.

Use `partial-tools` when some relevant information was successfully retrieved or verified with tools, but full tool-assisted execution is no longer available or no longer justified.

Do not infer capability from vendor name, branding, or expectation. Infer capability only from observable in-session behavior.

## Common Workflow

Follow the same high-level workflow in all modes:

1. Understand the task.
2. Identify what context is missing.
3. Decide whether the missing context truly blocks a good answer.
4. If needed and possible, acquire only the minimum necessary context.
5. Produce a clear answer, plan, or recommendation.
6. Report assumptions and evidence level.

The skill should optimize for the smallest sufficient context set, not the largest available context set.

## Tool-Assisted Workflow

When tools are available and justified:

1. Search for the most relevant files, symbols, modules, or evidence sources.
2. Read only the highest-value artifacts first.
3. Avoid loading entire repositories or large files unless clearly necessary.
4. Build a compact task-specific context set.
5. If budget pressure remains, summarize lower-priority material.
6. Use code compression only as a late-stage fallback when the task genuinely benefits.

The skill should prefer targeted inspection over broad exploration.

If the repository is sparse, the skill should not over-explore merely because tools exist.

## Prompt-Only Workflow

When operating in true prompt-only mode:

1. Reason only from the material explicitly provided.
2. Do not imply hidden repository access.
3. State the smallest missing information that would most improve the answer.
4. Still provide the best useful answer or next step possible.
5. Distinguish assumptions from observed facts.

Prompt-only mode is a first-class mode. It is not a failure state unless the task truly requires unavailable external evidence.

When operating in degraded mixed mode, use `partial-tools` instead of `prompt-only` if earlier tool results remain valid and relevant.

## Failure / Fallback Policy

If tool use becomes impossible or unreliable:

1. Downgrade immediately when a required tool is absent or forbidden.
2. Retry at most once per failing step when the failure appears cheap and transient.
3. If failure persists, continue in degraded mode.
4. Do not repeatedly probe the same failing path unless conditions clearly changed.
5. Preserve any verified results obtained before failure.
6. Clearly mark the boundary between verified findings and inferred conclusions.

Allowed runtime modes are:

- `unknown`
- `tool-assisted`
- `prompt-only`
- `partial-tools`

Use `partial-tools` when some relevant tools worked but others failed or were unavailable.

## Output Format

Return results using this structure:

Use the exact section headings below.

All seven sections are required on every run. If a section is not applicable, explicitly say `none`, `not needed`, or `not verified` rather than omitting the section.

### Understanding

State what the task is asking for.

### Mode Used

Output exactly one of the following literal values, with no extra words or explanation:

- `tool-assisted`
- `prompt-only`
- `partial-tools`

### Missing Context

State what information is absent, uncertain, or still unverified.

### Plan / Answer

Provide the answer, proposed approach, or next-step plan.

### Assumptions

List what was inferred rather than verified.

### Evidence Level

Output exactly one of the following literal values, with no extra words or explanation:

- tool-verified
- partially verified
- prompt-only reasoning

### Next Best Action

State the highest-value next step to improve confidence or continue progress.

The output shape should remain stable across modes even when evidence quality changes.

## Hard Prohibitions

Never:

1. fabricate files, modules, symbols, repository structure, or tool outputs,
2. claim a tool succeeded when it did not,
3. imply hidden inspection of files or repositories,
4. assume tool capability based on host branding,
5. over-explore when a small context set is sufficient,
6. use code compression as the default first move,
7. hide uncertainty when context is incomplete,
8. block unnecessarily when prompt-only reasoning can still provide value.

## Explicit Host Assumptions

This skill assumes:

1. the host may provide zero, some, or many tools,
2. tool exposure may be partial and uneven,
3. user instruction or policy may forbid tool use even when tools exist,
4. the only guaranteed input is the user task,
5. host-specific tool names, schemas, and invocation syntax are outside this file,
6. output formatting may later be adapted by a thin host wrapper.

This file is the source-of-truth instruction body, not a host adapter.

## Adapter Notes

When adapting this skill to a specific host:

1. keep the core behavior unchanged,
2. map host-specific tool names onto the capability rule,
3. keep adapters thin,
4. do not bury the core logic inside host-only metadata,
5. preserve the output contract,
6. and preserve the no-fabrication guarantee.

If the host supports structured tool manifests, they may be used to improve mode selection. If not, this skill should still function through capability observation and prompt-only fallback.
"""


def repo_root() -> Path:
    return Path(__file__).resolve().parent


def load_skill_body(root: Path | None = None) -> str:
    candidate_roots = []
    if root is not None:
        candidate_roots.append(root)
    else:
        try:
            candidate_roots.append(repo_root())
        except Exception:
            pass
    for base in candidate_roots:
        skill_path = base / "SKILL.md"
        if skill_path.exists():
            return skill_path.read_text(encoding="utf-8").rstrip() + "\n"
    return EMBEDDED_SKILL_BODY.rstrip() + "\n"


def render_skill(target: str, body: str) -> str:
    frontmatter = [
        "---",
        f"name: {SKILL_NAME}",
        f"description: {SKILL_DESCRIPTION}",
        f"license: {SKILL_LICENSE}",
        "---",
        "",
    ]
    if target == "opencode":
        frontmatter.insert(4, "compatibility: opencode")
    return "\n".join(frontmatter) + body


def codex_agents_snippet() -> str:
    return (
        "# Optional Codex AGENTS.md snippet\n\n"
        "Use the `context-optimization` skill when a task involves sparse repositories, "
        "uncertain tool availability, context-budget discipline, or a need to prefer targeted "
        "reading over broad exploration.\n\n"
        "Do not load broad repository context by default. Prefer selective retrieval, then summary, "
        "and only treat compression as a late-stage fallback.\n"
    )


def target_dir(target: str, scope: str, home: Path, cwd: Path) -> Path:
    if scope == "user":
        roots = {
            "claude": home / ".claude" / "skills",
            "opencode": home / ".config" / "opencode" / "skills",
            "codex": home / ".agents" / "skills",
        }
    elif scope == "project":
        roots = {
            "claude": cwd / ".claude" / "skills",
            "opencode": cwd / ".opencode" / "skills",
            "codex": cwd / ".agents" / "skills",
        }
    else:
        raise ValueError(f"Unsupported scope: {scope}")
    return roots[target] / SKILL_NAME


def detect_target(scope: str, home: Path, cwd: Path) -> str:
    if scope == "user":
        candidates = {
            "claude": home / ".claude",
            "opencode": home / ".config" / "opencode",
            "codex": home / ".agents",
        }
    else:
        candidates = {
            "claude": cwd / ".claude",
            "opencode": cwd / ".opencode",
            "codex": cwd / ".agents",
        }
    present = [name for name, marker in candidates.items() if marker.exists()]
    if len(present) == 1:
        return present[0]
    if not present:
        raise SystemExit(
            "Could not auto-detect target. Specify --target claude, opencode, or codex."
        )
    joined = ", ".join(sorted(present))
    raise SystemExit(
        f"Auto-detect found multiple targets ({joined}). Specify --target explicitly."
    )


def install_skill(
    *,
    target: str,
    scope: str,
    dry_run: bool,
    force: bool,
    init_always_on: bool,
    home: Path,
    cwd: Path,
    root: Path | None = None,
) -> Path:
    resolved_target = detect_target(scope, home, cwd) if target == "auto" else target
    body = load_skill_body(root)
    content = render_skill(resolved_target, body)
    destination_dir = target_dir(resolved_target, scope, home, cwd)
    destination_file = destination_dir / "SKILL.md"
    principles_file = destination_dir / "principles.md"

    if dry_run:
        print(f"[dry-run] target={resolved_target} scope={scope}")
        print(f"[dry-run] would write {destination_file}")
        print(f"[dry-run] would write {principles_file}")
        if scope == "project":
            agents_path = cwd / "AGENTS.md"
            marker = f"<!-- {AGENTS_MARKER} -->"
            if agents_path.exists() and marker in agents_path.read_text(encoding="utf-8"):
                print(f"[dry-run] AGENTS.md already contains skill instruction, would skip")
            else:
                print(f"[dry-run] would inject skill instruction into {agents_path}")
        if scope == "project" and init_always_on:
            _dry_run_always_on(resolved_target, cwd)
        return destination_file

    destination_dir.mkdir(parents=True, exist_ok=True)
    if destination_file.exists():
        existing = destination_file.read_text(encoding="utf-8")
        if existing == content:
            print(f"Already up to date: {destination_file}")
            return destination_file
        if not force:
            raise SystemExit(
                f"Refusing to overwrite existing file without --force: {destination_file}"
            )

    destination_file.write_text(content, encoding="utf-8")
    principles_file.write_text(PRINCIPLES_CONTENT, encoding="utf-8")
    print(f"Installed {SKILL_NAME} for {resolved_target} at {destination_file}")

    if scope == "project":
        inject_agents_instruction(cwd)
        if init_always_on:
            inject_always_on(resolved_target, cwd)

    return destination_file


def inject_agents_instruction(cwd: Path) -> None:
    agents_path = cwd / "AGENTS.md"
    marker = f"<!-- {AGENTS_MARKER} -->"

    if agents_path.exists():
        existing = agents_path.read_text(encoding="utf-8")
        if marker in existing:
            return
        new_section = f"\n\n{marker}\n{AGENTS_SNIPPET}\n"
        agents_path.write_text(existing.rstrip() + new_section, encoding="utf-8")
    else:
        project_name = cwd.resolve().name
        content = f"""# AGENTS.md — {project_name}

{marker}
{AGENTS_SNIPPET}
"""
        agents_path.write_text(content, encoding="utf-8")

    print(f"Injected skill instruction into {agents_path}")


def inject_always_on(target: str, cwd: Path) -> None:
    if target == "opencode":
        _inject_opencode_always_on(cwd)
    elif target == "claude":
        _inject_claude_always_on(cwd)
    elif target == "codex":
        _inject_codex_always_on(cwd)


def _dry_run_always_on(target: str, cwd: Path) -> None:
    if target == "opencode":
        config_path = cwd / ".opencode" / "oh-my-openagent.jsonc"
        print(f"[dry-run] would create/update {config_path} with prompt_append")
    elif target == "claude":
        claude_path = cwd / "CLAUDE.md"
        print(f"[dry-run] would inject principles into {claude_path}")
    elif target == "codex":
        agents_path = cwd / "AGENTS.md"
        print(f"[dry-run] would inject principles into {agents_path}")


def _inject_opencode_always_on(cwd: Path) -> None:
    config_dir = cwd / ".opencode"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "oh-my-openagent.jsonc"
    principles_path = config_dir / "skills" / SKILL_NAME / "principles.md"

    content = f"""{{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/assets/oh-my-opencode.schema.json",

  "agents": {{
    "sisyphus": {{
      "prompt_append": "file://{principles_path}"
    }}
  }}
}}
"""
    config_path.write_text(content, encoding="utf-8")
    print(f"Created always-on config at {config_path}")


def _inject_claude_always_on(cwd: Path) -> None:
    claude_path = cwd / "CLAUDE.md"
    marker = f"<!-- {ALWAYS_ON_MARKER} -->"
    section = f"\n\n{marker}\n{PRINCIPLES_CONTENT.rstrip()}\n"

    if claude_path.exists():
        existing = claude_path.read_text(encoding="utf-8")
        if marker in existing:
            return
        claude_path.write_text(existing.rstrip() + section, encoding="utf-8")
    else:
        claude_path.write_text(f"# CLAUDE.md\n\n{marker}\n{PRINCIPLES_CONTENT.rstrip()}\n", encoding="utf-8")

    print(f"Injected always-on principles into {claude_path}")


def _inject_codex_always_on(cwd: Path) -> None:
    agents_path = cwd / "AGENTS.md"
    marker = f"<!-- {ALWAYS_ON_MARKER} -->"

    if agents_path.exists():
        existing = agents_path.read_text(encoding="utf-8")
        if marker in existing:
            return
        section = f"\n\n{marker}\n{PRINCIPLES_CONTENT.rstrip()}\n"
        agents_path.write_text(existing.rstrip() + section, encoding="utf-8")
    else:
        content = f"""# AGENTS.md — {cwd.resolve().name}

<!-- {AGENTS_MARKER} -->
{AGENTS_SNIPPET}

{marker}
{PRINCIPLES_CONTENT.rstrip()}
"""
        agents_path.write_text(content, encoding="utf-8")

    print(f"Injected always-on principles into {agents_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install the context-optimization skill for OpenCode, Claude Code, or Codex."
    )
    parser.add_argument(
        "--target",
        default="auto",
        choices=["auto", "claude", "opencode", "codex"],
        help="Target host. Use auto to detect from the chosen scope.",
    )
    parser.add_argument(
        "--scope",
        default="user",
        choices=["user", "project"],
        help="Install globally for the current user or into the current project.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files if content differs.")
    parser.add_argument(
        "--init-always-on",
        action="store_true",
        help="Inject context-optimization principles into the host's always-on prompt file."
    )
    parser.add_argument(
        "--print-codex-agents-snippet",
        action="store_true",
        help="Print an optional AGENTS.md snippet for Codex and exit.",
    )
    parser.add_argument("--home", help=argparse.SUPPRESS)
    parser.add_argument("--cwd", help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.print_codex_agents_snippet:
        print(codex_agents_snippet(), end="")
        return 0

    home = Path(args.home).expanduser().resolve() if args.home else Path.home().resolve()
    cwd = Path(args.cwd).resolve() if args.cwd else Path.cwd().resolve()
    install_skill(
        target=args.target,
        scope=args.scope,
        dry_run=args.dry_run,
        force=args.force,
        init_always_on=args.init_always_on,
        home=home,
        cwd=cwd,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
