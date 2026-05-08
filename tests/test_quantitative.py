#!/usr/bin/env python3
"""Quantitative token test for context-optimization skill.

Compares token usage with and without the skill across 6 tasks
in the opencode repository (52K files).

Usage:
    python3 tests/test_quantitative.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

OPENCODE_REPO = str(Path(__file__).resolve().parent.parent.parent / "opencode")
SKILL_INSTALLER = str(Path(__file__).resolve().parent.parent / "install.py")
AGENTS_MD = os.path.join(OPENCODE_REPO, "AGENTS.md")
TIMEOUT = 180


@dataclass
class Task:
    id: str
    prompt: str
    key_info: list[str]
    quality_desc: str


@dataclass
class Result:
    task_id: str
    variant: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    tool_calls: int = 0
    quality_pass: bool = False
    quality_detail: str = ""
    answer_excerpt: str = ""
    success: bool = False


TASKS = [
    Task(
        id="T1",
        prompt="找到 opencode 仓库中 skill 加载机制的关键实现文件，不要过度探索",
        key_info=["skill.ts", "registry.ts"],
        quality_desc="至少提及 2 个关键文件路径",
    ),
    Task(
        id="T2",
        prompt="快速统计 opencode 仓库中 .test.ts 文件的数量，只用 find 命令",
        key_info=["569"],
        quality_desc="报告数字在 500-650 范围内",
    ),
    Task(
        id="T3",
        prompt="找到 opencode 的 package.json 中的 test 脚本命令是什么",
        key_info=["bun test"],
        quality_desc="提及 bun test",
    ),
    Task(
        id="T4",
        prompt="找到 opencode 的配置加载逻辑，opencode.json 是怎么被读取的，找到关键文件",
        key_info=["config"],
        quality_desc="提及 config 相关目录或文件",
    ),
    Task(
        id="T5",
        prompt="列出 opencode 仓库中所有 MCP 相关的源文件路径",
        key_info=["mcp"],
        quality_desc="列出含 mcp 的文件路径",
    ),
    Task(
        id="T6",
        prompt="分析 opencode 的构建工具链，用了什么构建工具和编译器",
        key_info=["bun", "typescript"],
        quality_desc="提及 bun 和 typescript",
    ),
]


def run_codex(prompt: str) -> dict:
    try:
        proc = subprocess.run(
            ["codex", "exec", "--json", prompt],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            cwd=OPENCODE_REPO,
        )
    except subprocess.TimeoutExpired:
        return {"tokens": None, "answer": "", "tool_calls": 0, "success": False}

    tokens = None
    answers: list[str] = []
    tool_calls = 0

    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        evt = obj.get("type", "")
        if evt == "turn.completed":
            usage = obj.get("usage", {})
            tokens = {
                "input": usage.get("input_tokens", 0),
                "output": usage.get("output_tokens", 0),
            }
        elif evt == "item.completed":
            item = obj.get("item", {})
            if item.get("type") == "agent_message":
                answers.append(item.get("text", ""))
            if item.get("type") == "command_execution":
                tool_calls += 1

    total = (tokens["input"] + tokens["output"]) if tokens else 0
    return {
        "tokens": tokens,
        "answer": "\n".join(answers),
        "tool_calls": tool_calls,
        "total_tokens": total,
        "success": tokens is not None,
    }


def check_quality(answer: str, task: Task) -> tuple[bool, str]:
    answer_lower = answer.lower()
    matches = [info for info in task.key_info if info.lower() in answer_lower]
    passed = len(matches) >= max(1, len(task.key_info) // 2)
    detail = f"matched {len(matches)}/{len(task.key_info)}: {matches}"
    return passed, detail


def backup_agents() -> str:
    with open(AGENTS_MD, encoding="utf-8") as f:
        return f.read()


def restore_agents(content: str) -> None:
    with open(AGENTS_MD, "w", encoding="utf-8") as f:
        f.write(content)


def remove_always_on(original: str) -> str:
    marker = "<!-- context-optimization:always-on -->"
    if marker in original:
        idx = original.index(marker)
        return original[:idx].rstrip() + "\n"
    return original


def run_suite(variant: str, tasks: list[Task]) -> list[Result]:
    results: list[Result] = []
    for task in tasks:
        print(f"  [{variant}] {task.id}: {task.prompt[:50]}...", flush=True)
        raw = run_codex(task.prompt)
        quality_pass, quality_detail = check_quality(raw["answer"], task)
        r = Result(
            task_id=task.id,
            variant=variant,
            input_tokens=raw["tokens"]["input"] if raw["tokens"] else 0,
            output_tokens=raw["tokens"]["output"] if raw["tokens"] else 0,
            total_tokens=raw.get("total_tokens", 0),
            tool_calls=raw.get("tool_calls", 0),
            quality_pass=quality_pass,
            quality_detail=quality_detail,
            answer_excerpt=raw["answer"][:200],
            success=raw["success"],
        )
        status = "✓" if quality_pass else "✗"
        print(f"    tokens={r.total_tokens:>8,}  tools={r.tool_calls}  quality={status}", flush=True)
        results.append(r)
    return results


def main() -> int:
    print("=== Quantitative Token Test ===\n", flush=True)
    print(f"Repo: {OPENCODE_REPO}", flush=True)
    print(f"Tasks: {len(TASKS)}\n", flush=True)

    if not os.path.isdir(OPENCODE_REPO):
        print(f"ERROR: opencode repo not found at {OPENCODE_REPO}")
        return 1

    original = backup_agents()

    print("Phase 1: Baseline (no skill)", flush=True)
    restore_agents(remove_always_on(original))
    baseline = run_suite("baseline", TASKS)

    print("\nPhase 2: With skill (always-on)", flush=True)
    restore_agents(original)
    subprocess.run(
        ["python3", SKILL_INSTALLER, "--target", "codex", "--scope", "project", "--init-always-on"],
        cwd=OPENCODE_REPO,
        capture_output=True,
    )
    skilled = run_suite("with_skill", TASKS)

    print("\n=== Results ===\n", flush=True)
    header = f"{'Task':<5} {'Baseline':>10} {'Skill':>10} {'Reduction':>10} {'Tools(B/S)':>12} {'Quality':>8}"
    print(header, flush=True)
    print("-" * len(header), flush=True)

    total_b = total_s = 0
    quality_ok = 0
    reductions = 0
    rows: list[str] = []

    for b, s in zip(baseline, skilled):
        if not b.success:
            print(f"{b.task_id:<5} {'TIMEOUT':>10} {s.total_tokens:>10,} {'---':>10} {'---':>12} {'✗':>8}", flush=True)
            rows.append(f"{b.task_id},baseline,TIMEOUT,,,,")
            rows.append(f"{s.task_id},skill,{s.input_tokens},{s.output_tokens},{s.total_tokens},{s.quality_pass},")
            continue
        if not s.success:
            print(f"{b.task_id:<5} {b.total_tokens:>10,} {'TIMEOUT':>10} {'---':>10} {'---':>12} {'✗':>8}", flush=True)
            rows.append(f"{b.task_id},baseline,{b.input_tokens},{b.output_tokens},{b.total_tokens},{b.quality_pass},")
            rows.append(f"{s.task_id},skill,TIMEOUT,,,,")
            continue

        reduction = (b.total_tokens - s.total_tokens) / b.total_tokens * 100 if b.total_tokens > 0 else 0
        total_b += b.total_tokens
        total_s += s.total_tokens
        if s.quality_pass:
            quality_ok += 1
        if reduction > 0:
            reductions += 1

        qmark = "✓" if s.quality_pass else "✗"
        tools = f"{b.tool_calls}/{s.tool_calls}"
        print(f"{b.task_id:<5} {b.total_tokens:>10,} {s.total_tokens:>10,} {reduction:>9.1f}% {tools:>12} {qmark:>8}", flush=True)
        rows.append(f"{b.task_id},baseline,{b.input_tokens},{b.output_tokens},{b.total_tokens},{b.quality_pass},")
        rows.append(f"{s.task_id},skill,{s.input_tokens},{s.output_tokens},{s.total_tokens},{s.quality_pass},")

    print("-" * len(header), flush=True)
    avg_red = (total_b - total_s) / total_b * 100 if total_b > 0 else 0
    print(f"{'Total':<5} {total_b:>10,} {total_s:>10,} {avg_red:>9.1f}% {'':>12} {'':>8}", flush=True)

    print("\n=== Acceptance Criteria ===\n", flush=True)
    criteria = [
        ("Avg token reduction ≥ 15%", avg_red >= 15),
        ("Quality preserved ≥ 5/6 tasks", quality_ok >= 5),
        ("No task token increase > 50%", all(
            (s.total_tokens - b.total_tokens) / b.total_tokens * 100 < 50
            for b, s in zip(baseline, skilled)
            if b.success and s.success and b.total_tokens > 0
        )),
        ("≥ 4/6 tasks show token reduction", reductions >= 4),
    ]

    all_pass = True
    for name, passed in criteria:
        tag = "✓ PASS" if passed else "✗ FAIL"
        if not passed:
            all_pass = False
        print(f"  {tag}  {name}", flush=True)

    print(f"\n{'='*50}", flush=True)
    print(f"Overall: {'ACCEPTED' if all_pass else 'NEEDS REVIEW'}", flush=True)

    csv_path = Path(__file__).resolve().parent / "quantitative_results.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("task_id,variant,input_tokens,output_tokens,total_tokens,quality_pass\n")
        for row in rows:
            f.write(row + "\n")
    print(f"\nResults saved to {csv_path}", flush=True)

    print("\nPhase 3: Cleanup", flush=True)
    restore_agents(original)
    print("AGENTS.md restored.", flush=True)

    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
