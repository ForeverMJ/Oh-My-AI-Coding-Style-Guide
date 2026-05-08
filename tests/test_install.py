from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from typing import cast

import install


class InstallTests(unittest.TestCase):
    def test_render_skill_has_frontmatter(self) -> None:
        body = "# Demo\n"
        content = install.render_skill("claude", body)
        self.assertIn("name: context-optimization", content)
        self.assertIn("description:", content)
        self.assertIn("# Demo", content)

    def test_render_skill_opencode_adds_compatibility(self) -> None:
        content = install.render_skill("opencode", "# Demo\n")
        self.assertIn("compatibility: opencode", content)

    def test_user_scope_opencode_install_creates_expected_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "cwd"
            home.mkdir()
            cwd.mkdir()
            root = Path(tmp) / "repo"
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            path = install.install_skill(target="opencode", scope="user", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            self.assertTrue(path.exists())
            self.assertIn("compatibility: opencode", path.read_text(encoding="utf-8"))

    def test_project_scope_claude_install_creates_expected_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            path = install.install_skill(target="claude", scope="project", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            self.assertTrue(path.exists())
            self.assertTrue(str(path).endswith(".claude/skills/context-optimization/SKILL.md"))

    def test_user_scope_codex_install_creates_expected_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "cwd"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            path = install.install_skill(target="codex", scope="user", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            self.assertTrue(path.exists())
            self.assertTrue(str(path).endswith(".agents/skills/context-optimization/SKILL.md"))

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "cwd"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            path = install.install_skill(target="claude", scope="user", dry_run=True, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            self.assertFalse(path.exists())

    def test_auto_detects_project_opencode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            root = Path(tmp) / "repo"
            home.mkdir()
            (cwd / ".opencode").mkdir(parents=True)
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            path = install.install_skill(target="auto", scope="project", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            self.assertTrue(path.exists())
            self.assertTrue(str(path).endswith(".opencode/skills/context-optimization/SKILL.md"))

    def test_reinstall_same_content_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "cwd"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            first = install.install_skill(target="claude", scope="user", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            second = install.install_skill(target="claude", scope="user", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            self.assertEqual(first, second)
            self.assertTrue(second.exists())

    def test_refuses_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "cwd"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            destination = home / ".claude" / "skills" / "context-optimization" / "SKILL.md"
            destination.parent.mkdir(parents=True)
            destination.write_text("different\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                install.install_skill(target="claude", scope="user", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)

    def test_pipe_install_flow_works_with_embedded_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            home.mkdir()
            cwd.mkdir()
            script = Path(__file__).resolve().parent.parent / "install.py"
            result = subprocess.run(
                [
                    sys.executable,
                    "-",
                    "--target",
                    "claude",
                    "--scope",
                    "user",
                    "--home",
                    str(home),
                    "--cwd",
                    str(cwd),
                ],
                input=script.read_text(encoding="utf-8"),
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertIn("Installed context-optimization for claude", result.stdout)
            installed = home / ".claude" / "skills" / "context-optimization" / "SKILL.md"
            self.assertTrue(installed.exists())
            self.assertIn("# Context Optimization Skill", installed.read_text(encoding="utf-8"))

    def test_project_scope_creates_agents_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            install.install_skill(target="claude", scope="project", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            agents_path = cwd / "AGENTS.md"
            self.assertTrue(agents_path.exists())
            content = agents_path.read_text(encoding="utf-8")
            self.assertIn(install.AGENTS_MARKER, content)
            self.assertIn("context-optimization", content)

    def test_project_scope_appends_to_existing_agents_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            (cwd / "AGENTS.md").write_text("# Existing content\n", encoding="utf-8")
            install.install_skill(target="claude", scope="project", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            content = (cwd / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("# Existing content", content)
            self.assertIn(install.AGENTS_MARKER, content)

    def test_project_scope_agents_md_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            install.install_skill(target="claude", scope="project", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            content_first = (cwd / "AGENTS.md").read_text(encoding="utf-8")
            install.install_skill(target="claude", scope="project", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            content_second = (cwd / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(content_first, content_second)

    def test_user_scope_does_not_inject_agents_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "cwd"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            install.install_skill(target="claude", scope="user", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            agents_path = cwd / "AGENTS.md"
            self.assertFalse(agents_path.exists())

    def test_dry_run_shows_agents_md_injection_message(self) -> None:
        from io import StringIO
        real_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp) / "home"
                cwd = Path(tmp) / "project"
                root = Path(tmp) / "repo"
                home.mkdir()
                cwd.mkdir()
                root.mkdir()
                (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
                install.install_skill(target="claude", scope="project", dry_run=True, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
                output = cast(StringIO, sys.stdout).getvalue()
                self.assertIn("would inject skill instruction", output)
        finally:
            sys.stdout = real_stdout

    def test_dry_run_user_scope_does_not_show_agents_message(self) -> None:
        from io import StringIO
        real_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp) / "home"
                cwd = Path(tmp) / "cwd"
                root = Path(tmp) / "repo"
                home.mkdir()
                cwd.mkdir()
                root.mkdir()
                (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
                install.install_skill(target="claude", scope="user", dry_run=True, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
                output = cast(StringIO, sys.stdout).getvalue()
                self.assertNotIn("would inject skill instruction", output)
        finally:
            sys.stdout = real_stdout

    def test_install_writes_principles_alongside_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            install.install_skill(target="claude", scope="project", dry_run=False, force=False, init_always_on=False, home=home, cwd=cwd, root=root)
            principles = cwd / ".claude" / "skills" / "context-optimization" / "principles.md"
            self.assertTrue(principles.exists())
            self.assertIn("Retrieval First", principles.read_text(encoding="utf-8"))

    def test_opencode_always_on_creates_omo_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            install.install_skill(target="opencode", scope="project", dry_run=False, force=False, init_always_on=True, home=home, cwd=cwd, root=root)
            config = cwd / ".opencode" / "oh-my-openagent.jsonc"
            self.assertTrue(config.exists())
            content = config.read_text(encoding="utf-8")
            self.assertIn("prompt_append", content)
            self.assertIn("principles.md", content)

    def test_claude_always_on_injects_into_claude_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            install.install_skill(target="claude", scope="project", dry_run=False, force=False, init_always_on=True, home=home, cwd=cwd, root=root)
            claude_md = cwd / "CLAUDE.md"
            self.assertTrue(claude_md.exists())
            content = claude_md.read_text(encoding="utf-8")
            self.assertIn(install.ALWAYS_ON_MARKER, content)
            self.assertIn("Retrieval First", content)

    def test_codex_always_on_injects_into_agents_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            install.install_skill(target="codex", scope="project", dry_run=False, force=False, init_always_on=True, home=home, cwd=cwd, root=root)
            agents_md = cwd / "AGENTS.md"
            self.assertTrue(agents_md.exists())
            content = agents_md.read_text(encoding="utf-8")
            self.assertIn(install.ALWAYS_ON_MARKER, content)
            self.assertIn(install.AGENTS_MARKER, content)
            self.assertIn("Retrieval First", content)

    def test_always_on_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "project"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            install.install_skill(target="claude", scope="project", dry_run=False, force=False, init_always_on=True, home=home, cwd=cwd, root=root)
            content_first = (cwd / "CLAUDE.md").read_text(encoding="utf-8")
            install.install_skill(target="claude", scope="project", dry_run=False, force=False, init_always_on=True, home=home, cwd=cwd, root=root)
            content_second = (cwd / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertEqual(content_first, content_second)

    def test_user_scope_does_not_inject_always_on(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            cwd = Path(tmp) / "cwd"
            root = Path(tmp) / "repo"
            home.mkdir()
            cwd.mkdir()
            root.mkdir()
            (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
            install.install_skill(target="claude", scope="user", dry_run=False, force=False, init_always_on=True, home=home, cwd=cwd, root=root)
            claude_md = cwd / "CLAUDE.md"
            self.assertFalse(claude_md.exists())

    def test_dry_run_shows_always_on_for_opencode(self) -> None:
        from io import StringIO
        real_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp) / "home"
                cwd = Path(tmp) / "project"
                root = Path(tmp) / "repo"
                home.mkdir()
                cwd.mkdir()
                root.mkdir()
                (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
                install.install_skill(target="opencode", scope="project", dry_run=True, force=False, init_always_on=True, home=home, cwd=cwd, root=root)
                output = cast(StringIO, sys.stdout).getvalue()
                self.assertIn("prompt_append", output)
        finally:
            sys.stdout = real_stdout

    def test_dry_run_shows_always_on_for_claude(self) -> None:
        from io import StringIO
        real_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp) / "home"
                cwd = Path(tmp) / "project"
                root = Path(tmp) / "repo"
                home.mkdir()
                cwd.mkdir()
                root.mkdir()
                (root / "SKILL.md").write_text("# Context Optimization Skill\n", encoding="utf-8")
                install.install_skill(target="claude", scope="project", dry_run=True, force=False, init_always_on=True, home=home, cwd=cwd, root=root)
                output = cast(StringIO, sys.stdout).getvalue()
                self.assertIn("CLAUDE.md", output)
        finally:
            sys.stdout = real_stdout


if __name__ == "__main__":
    unittest.main()
