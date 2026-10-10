# Install WYN for future sessions

Use this workflow when the user requests installation, updating an installation, checking its status, or uninstalling it. Ordinary invocation of WYN does not itself request persistent configuration changes.

The installer travels with the skill at `scripts/install.py`. It uses Python 3.8 or later and the standard library. A full repository checkout also provides the `install.sh` wrapper. Resolve paths relative to the skill you actually loaded, not the task's current directory.

## Install

From the skill directory, choose the requested host:

```sh
python3 scripts/install.py install --claude
python3 scripts/install.py install --codex
python3 scripts/install.py install --all
```

Choose one command. With no host flag, the installer targets Claude Code. It creates a global skill symlink and a short activation block in the host's instruction file. Keep the source skill in a durable location because the symlink points to it. If WYN is currently in a temporary download directory, move or copy the complete skill to a stable user-owned location before installing it.

If the files are not available locally, clone `https://github.com/fcecin/wyn.git` into `~/wyn/wyn/` or an appropriate location under the user's existing tooling home, inspect the installer, and run its `install.sh` wrapper. Reserve `~/wyn/README.md` for the machine's tooling index. Reuse an existing checkout when appropriate. Do not overwrite another checkout or execute a remote shell script through a pipe.

| Host | Skill link | Activation file |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/wyn` | `~/.claude/CLAUDE.md` |
| Codex | `~/.agents/skills/wyn` | `~/.codex/AGENTS.md` |

`CLAUDE_CONFIG_DIR` and `CODEX_HOME` select the corresponding configuration roots. The Codex skill directory stays at `~/.agents/skills` unless `--codex-skills-dir` is provided. Explicit `--claude-config-dir` and `--codex-config-dir` options also exist. Use `--no-instructions` to install only the discovery link; `--no-claudemd` is an alias.

The installer refuses to replace an unrelated file, directory, or skill link. It checks managed markers before writing, backs up changed existing instruction files, and preserves content outside its WYN block. Resolve a conflict from evidence; do not delete another installation merely to make this installer succeed.

## Verify or remove

Use the same host and custom directory options as installation:

```sh
python3 scripts/install.py status --claude
python3 scripts/install.py uninstall --claude
```

Verify that the skill link resolves, referenced files exist, and the activation block is current when enabled. Rerunning installation refreshes its managed block without duplicating it. Uninstall removes only this installation's link and WYN block; it keeps the source skill and backups. With `--no-instructions`, it leaves instruction files untouched.

Follow [project organization](projects.md) to register the durable installation in the tooling-home README, including the repository URL when known and the actual canonical checkout. The agent maintains that index; the installer manages only skill links and activation blocks.

Report the installed link, source directory, and activation file. A new session may be needed for discovery. Installation checks do not prove runtime behavior inside an agent.
