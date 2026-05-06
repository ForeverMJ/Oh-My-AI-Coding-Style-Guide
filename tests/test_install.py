from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

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
            path = install.install_skill(
                target="opencode",
                scope="user",
                dry_run=False,
                force=False,
                home=home,
                cwd=cwd,
                root=root,
            )
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
            path = install.install_skill(
                target="claude",
                scope="project",
                dry_run=False,
                force=False,
                home=home,
                cwd=cwd,
                root=root,
            )
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
            path = install.install_skill(
                target="codex",
                scope="user",
                dry_run=False,
                force=False,
                home=home,
                cwd=cwd,
                root=root,
            )
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
            path = install.install_skill(
                target="claude",
                scope="user",
                dry_run=True,
                force=False,
                home=home,
                cwd=cwd,
                root=root,
            )
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
            path = install.install_skill(
                target="auto",
                scope="project",
                dry_run=False,
                force=False,
                home=home,
                cwd=cwd,
                root=root,
            )
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
            first = install.install_skill(
                target="claude",
                scope="user",
                dry_run=False,
                force=False,
                home=home,
                cwd=cwd,
                root=root,
            )
            second = install.install_skill(
                target="claude",
                scope="user",
                dry_run=False,
                force=False,
                home=home,
                cwd=cwd,
                root=root,
            )
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
                install.install_skill(
                    target="claude",
                    scope="user",
                    dry_run=False,
                    force=False,
                    home=home,
                    cwd=cwd,
                    root=root,
                )

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


if __name__ == "__main__":
    unittest.main()
