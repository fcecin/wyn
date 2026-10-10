"""Exercise installer effects using temporary directories, never live config."""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/wyn"
INSTALLER = SKILL / "scripts/install.py"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="wyn-installer-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.claude = self.root / "Claude config with spaces"
        self.codex = self.root / "Codex config"
        self.skills = self.root / "Agent skills"

    def run_installer(self, *arguments, expected=0, installer=INSTALLER):
        result = subprocess.run(
            [sys.executable, str(installer), *arguments,
             "--claude-config-dir", str(self.claude),
             "--codex-config-dir", str(self.codex),
             "--codex-skills-dir", str(self.skills)],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_both_hosts_install_update_status_uninstall(self):
        originals = {}
        for directory, name in ((self.claude, "CLAUDE.md"), (self.codex, "AGENTS.md")):
            directory.mkdir()
            path = directory / name
            original = b"# Existing rules\r\nPreserve me.\r\n"
            path.write_bytes(original)
            path.chmod(0o640)
            originals[path] = original

        self.run_installer("install", "--all")
        for link in (self.claude / "skills/wyn", self.skills / "wyn"):
            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), SKILL)
            self.assertTrue((link / "references/cli-workers.md").is_file())
        for path, original in originals.items():
            self.assertTrue(path.read_bytes().startswith(original))
            self.assertEqual(path.stat().st_mode & 0o777, 0o640)
            backups = list(path.parent.glob(path.name + ".bak.wyn.*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), original)

        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file() and not p.is_symlink()}
        self.run_installer("install", "--all")
        status = self.run_installer("status", "--all")
        self.assertEqual(status.stdout.count("current:"), 2)
        after = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file() and not p.is_symlink()}
        self.assertEqual(before, after)

        path = self.claude / "CLAUDE.md"
        stale = path.read_bytes().replace(b"# What You Need (WYN)", b"# Old WYN")
        path.write_bytes(stale + b"\n# Rules below the block\n")
        self.run_installer("install", "--claude")
        self.assertEqual(path.read_text().count("<!-- wyn:begin -->"), 1)
        self.assertTrue(path.read_bytes().endswith(b"\n# Rules below the block\n"))
        self.assertIn(stale + b"\n# Rules below the block\n",
                      [p.read_bytes() for p in self.claude.glob("CLAUDE.md.bak.wyn.*")])

        self.run_installer("uninstall", "--all")
        self.run_installer("uninstall", "--all")
        self.assertFalse((self.claude / "skills/wyn").is_symlink())
        self.assertFalse((self.skills / "wyn").is_symlink())
        self.assertEqual(path.read_bytes(), originals[path] + b"\n# Rules below the block\n")
        self.assertEqual((self.codex / "AGENTS.md").read_bytes(), originals[self.codex / "AGENTS.md"])
        self.assertTrue((SKILL / "SKILL.md").is_file())

    def test_status_and_uninstall_absent_have_no_side_effects(self):
        self.run_installer("status", "--all")
        self.run_installer("uninstall", "--all")
        self.assertEqual(list(self.root.iterdir()), [])

    def test_conflict_preflight_preserves_both_hosts(self):
        foreign = self.skills / "wyn"
        foreign.mkdir(parents=True)
        (foreign / "mine").write_text("keep")
        self.run_installer("install", "--all", expected=1)
        self.assertFalse(self.claude.exists())
        self.assertEqual((foreign / "mine").read_text(), "keep")
        self.run_installer("uninstall", "--codex", expected=1)
        self.assertTrue(foreign.is_dir())

    def test_dangling_foreign_link_is_not_replaced(self):
        link = self.claude / "skills/wyn"
        link.parent.mkdir(parents=True)
        link.symlink_to(self.root / "missing")
        self.run_installer("install", expected=1)
        self.assertEqual(os.readlink(link), str(self.root / "missing"))

    def test_bad_markers_do_not_create_skill_link(self):
        self.claude.mkdir()
        config = self.claude / "CLAUDE.md"
        for text in ("<!-- wyn:begin -->\n", "<!-- wyn:end -->\n",
                     "<!-- wyn:end -->\n<!-- wyn:begin -->\n",
                     "<!-- wyn:begin -->\n<!-- wyn:end -->\n" * 2):
            with self.subTest(text=text):
                config.write_text(text)
                self.run_installer("install", expected=1)
                self.assertEqual(config.read_text(), text)
                self.assertFalse((self.claude / "skills/wyn").exists())

    def test_no_instructions_and_default_host(self):
        self.run_installer("install", "--no-claudemd")
        self.assertTrue((self.claude / "skills/wyn").is_symlink())
        self.assertFalse((self.claude / "CLAUDE.md").exists())
        self.assertFalse(self.codex.exists())
        self.assertFalse(self.skills.exists())
        self.run_installer("uninstall", "--no-instructions")
        self.assertFalse((self.claude / "skills/wyn").is_symlink())

    def test_config_symlink_is_preserved(self):
        self.claude.mkdir()
        target = self.root / "shared-rules.md"
        target.write_text("# Shared rules\n")
        config = self.claude / "CLAUDE.md"
        config.symlink_to(target)
        self.run_installer("install")
        self.assertTrue(config.is_symlink())
        self.assertIn("<!-- wyn:begin -->", target.read_text())
        self.run_installer("uninstall")
        self.assertTrue(config.is_symlink())
        self.assertEqual(target.read_text(), "# Shared rules\n")

    def test_standalone_bundle_installs_codex(self):
        bundle = self.root / "standalone" / "wyn"
        shutil.copytree(SKILL, bundle, ignore=shutil.ignore_patterns("__pycache__"))
        self.run_installer("install", "--codex", installer=bundle / "scripts/install.py")
        self.assertEqual((self.skills / "wyn").resolve(), bundle)
        self.assertIn(str(self.skills / "wyn/SKILL.md"), (self.codex / "AGENTS.md").read_text())
        self.assertFalse(self.claude.exists())


if __name__ == "__main__":
    unittest.main()
