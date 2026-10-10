# What You Need (WYN)

**You can make the tools you need.**

A portable agent skill for Claude Code, Codex, and other agents that support
[Agent Skills](https://agentskills.io/specification).

WYN reminds agents they can write software, download a local binary, build from
source, connect existing tools, or drive another AI session to get the job done.
It also tells them to keep the AI budget under control.

## Why

> “I need sudo to install xyz.”

You need a capability. A system install is one way to get it. A local build,
an unpacked executable, or a small script may be enough.

The same principle applies to AI workers. An agent can start a real Claude Code
or Codex process, read its terminal, answer questions, and direct the next step.
WYN favors these explicit processes over built-in subagents.

## How

| Need | WYN's approach |
| --- | --- |
| A missing tool | Find, download, build, compose, or write what the task needs. |
| A bounded AI assignment | Use `claude -p` or `codex exec`. |
| An ongoing AI conversation | Run Claude Code or Codex in tmux; observe, prompt, verify, and continue. |
| Affordable execution | Use an economical doing model; move up one tier for hard work. |
| Reliable verification | Use a stronger model for a bounded review of the consolidated result. |
| Difficult reasoning | Tune reasoning effort separately from model tier. |
| Clear progress | Report `WYN:` plus the action and relevant paths. |

The intended model split is Luna/Haiku doing, an intermediate GPT model/Sonnet
when needed, and Sol/Opus checking. These are user-suggested roles, not fixed
provider IDs. The agent checks availability, effort settings, and usage limits.
Worker counts, attempts, and review rounds stay bounded.

Example progress report:

```text
WYN: Creating tools/convert.py to process input/ and write converted files to output/.
```

Full instructions are in [SKILL.md](skills/wyn/SKILL.md).
[Worker examples](skills/wyn/references/cli-workers.md) cover both CLIs and tmux.

## Install

### Ask your agent

Tell Claude Code or Codex:

```text
Read https://github.com/fcecin/wyn and install WYN globally for this agent.
Follow skills/wyn/references/install.md. Keep the skill in a persistent local directory.
```

The agent can inspect or clone the repository, select its host, run the installer,
and verify the result. The skill carries its own installation instructions and
installer. If you want both agents installed, say “for Claude Code and Codex.”

### Install from a terminal

Requires Git, Bash, and Python 3.8 or later. The installer uses no Python packages
outside the standard library and needs no sudo.

```sh
git clone https://github.com/fcecin/wyn.git ~/wyn
~/wyn/install.sh --claude
```

For Codex, or both agents:

```sh
~/wyn/install.sh --codex
~/wyn/install.sh --all
```

Choose the command for your setup. With no host option, the installer targets
Claude Code, matching [BOINK's](https://github.com/fcecin/claude-boink) convention.

| Host | Global skill link | Activation file |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/wyn` | `~/.claude/CLAUDE.md` |
| Codex | `~/.agents/skills/wyn` | `~/.codex/AGENTS.md` |

The activation block is a short pointer and reminder. The full skill stays in
`skills/wyn/SKILL.md` and loads when needed. Keep the checkout in place: the
global entries link to it. Start a new session if WYN is not listed yet.

```text
install.sh [install|status|uninstall] [--claude|--codex|--all] [--no-instructions]
```

Like BOINK, the installer is idempotent, backs up changed instruction files, and
maintains a block between `<!-- wyn:begin -->` and `<!-- wyn:end -->`. Reinstalling
updates that block in place. Uninstall removes the owned skill link and WYN
block, keeping the checkout, backups, and unrelated configuration. Conflicting
skill paths and malformed managed blocks are reported without overwriting them.

Use `--no-instructions` for discovery links only. `--no-claudemd` is an alias.
`CLAUDE_CONFIG_DIR` and `CODEX_HOME` override configuration roots; Codex's skill
directory remains `~/.agents/skills` unless `--codex-skills-dir` is supplied.
Run `./install.sh --help` for explicit directory overrides.

### Update, inspect, or remove

From your checkout, choose the host you installed:

```sh
git pull --ff-only
./install.sh install --all
./install.sh status --all
```

To remove the global links and activation blocks:

```sh
./install.sh uninstall --all
```

Use `--claude` or `--codex` instead of `--all` to manage one host. Repeat any custom
directory options used at installation.

## Portable by design

The skill bundle is `skills/wyn/`. Its installer and references travel with it,
so an agent can install from a copied bundle too:

```sh
python3 /path/to/wyn/scripts/install.py install --codex
```

The repository also includes `.claude/skills/wyn` and `.agents/skills/wyn`
symlinks for project discovery. Both point to the same canonical folder.
Other Agent Skills hosts can use that folder through their own discovery
conventions. On systems without symlink support, copy the bundle to the host's
skill directory and follow its installation guidance.

The instructions need no fixed runtime. Python is used by the optional installer;
tmux and agent CLIs are needed only for workflows that use them. WYN operates
within the user's task, environment permissions, and budget.

## Develop

Edit [skills/wyn/SKILL.md](skills/wyn/SKILL.md). Supporting files:

```text
install.sh                         Repository installer entrypoint
skills/wyn/
  SKILL.md                         Shared instructions
  scripts/install.py               Standalone installer
  references/
    install.md                     Agent installation workflow
    cli-workers.md                 Claude Code, Codex, and tmux examples
    claude-md-block.md             Claude activation template
    codex-md-block.md              Codex activation template
tests/test_install.py              Installer lifecycle checks
```

Run the installer checks in isolated temporary directories:

```sh
python3 -m unittest discover -s tests -v
```

These checks cover installation and configuration handling. Agent behavior,
model quality, and account-specific CLI access still need real use to evaluate.

## Acknowledgments

Installation follows the linked-skill and managed-instruction-block pattern from
[fcecin/claude-boink](https://github.com/fcecin/claude-boink).

## License

[MIT](LICENSE)
