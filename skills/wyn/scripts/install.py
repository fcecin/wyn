#!/usr/bin/env python3
"""Install WYN as a linked user skill without replacing unrelated configuration."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import tempfile


SKILL = Path(__file__).resolve().parents[1]
BEGIN = "<!-- wyn:begin -->"
END = "<!-- wyn:end -->"


def block_span(text):
    """Find exactly one complete managed block, or no block."""
    starts, ends = [], []
    offset = 0
    for line in text.splitlines(keepends=True):
        if line.strip() == BEGIN:
            starts.append(offset)
        if line.strip() == END:
            ends.append(offset + len(line))
        offset += len(line)
    if not starts and not ends:
        return None
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        raise ValueError("WYN markers are incomplete, duplicated, or out of order; inspect the file")
    return starts[0], ends[0]


def link_state(link):
    if link.is_symlink() and link.resolve() == SKILL:
        return "linked"
    if link.exists() or link.is_symlink():
        return "conflict"
    return "absent"


def rewrite(path, content):
    """Back up before changing an existing file; preserve a config symlink."""
    target = path.resolve(strict=True) if path.is_symlink() else path
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = target.with_name(target.name + ".bak.wyn." + stamp)
        shutil.copy2(target, backup)
        print(f"backup   {backup}")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".wyn-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content.encode("utf-8"))
        if target.exists():
            shutil.copystat(target, temporary)
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def expanded(value):
    return Path(value).expanduser().absolute()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", choices=("install", "status", "uninstall"), default="install")
    targets = parser.add_mutually_exclusive_group()
    targets.add_argument("--claude", action="store_true", help="Claude Code only (default)")
    targets.add_argument("--codex", action="store_true", help="Codex only")
    targets.add_argument("--all", action="store_true", help="Claude Code and Codex")
    parser.add_argument("--no-instructions", "--no-claudemd", action="store_true",
                        help="manage skill links only; leave CLAUDE.md and AGENTS.md untouched")
    parser.add_argument("--claude-config-dir", default=os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude"))
    parser.add_argument("--codex-config-dir", default=os.environ.get("CODEX_HOME", "~/.codex"))
    parser.add_argument("--codex-skills-dir", default="~/.agents/skills",
                        help="Codex discovery directory (default: ~/.agents/skills)")
    args = parser.parse_args(argv)

    if not (SKILL / "SKILL.md").is_file():
        raise ValueError(f"Missing skill entrypoint: {SKILL / 'SKILL.md'}")

    selected = []
    if args.all or not args.codex:
        config = expanded(args.claude_config_dir)
        selected.append(("claude", config / "skills/wyn", config / "CLAUDE.md"))
    if args.all or args.codex:
        selected.append(("codex", expanded(args.codex_skills_dir) / "wyn",
                         expanded(args.codex_config_dir) / "AGENTS.md"))

    # Inspect every target before changing any of them.
    plans = []
    for host, link, instructions in selected:
        state = link_state(link)
        if state == "conflict" and args.command != "status":
            raise ValueError(f"Refusing to replace or remove {link}: it is not a link to {SKILL}")
        old, new, block_state = None, None, "skipped"
        if not args.no_instructions:
            if instructions.is_symlink() and not instructions.exists():
                raise ValueError(f"Dangling configuration symlink: {instructions}")
            old = instructions.read_bytes().decode("utf-8") if instructions.exists() else ""
            try:
                span = block_span(old)
            except ValueError as error:
                raise ValueError(f"{instructions}: {error}") from error
            template = (SKILL / "references" / f"{host}-md-block.md").read_text()
            body = template.replace("{{skill_path}}", str(link / "SKILL.md")).rstrip()
            block = BEGIN + "\n" + body + "\n" + END + "\n"
            block_state = "absent" if span is None else (
                "current" if old[span[0]:span[1]] == block else "stale")
            if args.command == "uninstall":
                new = old if span is None else old[:span[0]] + old[span[1]:]
            elif span is None:
                separator = "" if not old or old.endswith("\n") else "\n"
                new = old + separator + block
            else:
                new = old[:span[0]] + block + old[span[1]:]
        plans.append((host, link, instructions, state, old, new, block_state))

    for host, link, instructions, state, old, new, block_state in plans:
        if args.command == "status":
            print(f"{host:8} {state}: {link}")
            print(f"block    {block_state}: {instructions}")
            continue
        if args.command == "install":
            if state == "absent":
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(SKILL, target_is_directory=True)
                print(f"linked   {link} -> {SKILL}")
            else:
                print(f"ok       already linked: {link}")
        elif state == "linked":
            link.unlink()
            print(f"removed  {link}")
        else:
            print(f"ok       no skill link: {link}")
        if not args.no_instructions and new != old:
            rewrite(instructions, new)
            print(f"updated  WYN block: {instructions}")
        else:
            print(f"ok       configuration unchanged: {instructions}")

    if args.command == "install":
        print("done     Start a new agent session if WYN is not yet listed.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"error    {error}", file=sys.stderr)
        sys.exit(1)
