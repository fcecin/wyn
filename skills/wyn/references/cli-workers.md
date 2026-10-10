# Claude Code and Codex workers

Either agent can act as coordinator through its available shell tools. It can launch workers of either kind when the CLI, authentication, and required permissions are available. The worker does not automatically inherit the coordinator's conversation: provide a brief and relevant files.

## Choose the invocation

| Purpose | Claude Code | Codex |
| --- | --- | --- |
| Interactive conversation | `claude` | `codex` |
| Single request | `claude -p 'Read BRIEF.md and complete the assignment.'` | `codex exec 'Read BRIEF.md and complete the assignment.'` |
| Resume a specific saved conversation | `claude --resume SESSION_ID` | `codex resume SESSION_ID` |

Run in the worker's workspace, normally under the owning WYN project in `~/wyn/`, or in an isolated working copy recorded by that project. For a one-shot call, capture stdout, stderr, and the exit status. For concurrent conversations, record explicit session IDs; a "most recent" shortcut can select the wrong worker. Resume only after determining that the intended conversation is no longer active.

These mappings follow the [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference) and [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference). Check local `--help` for version-specific options. In particular, Claude's `-p` means print mode, while Codex's `-p` selects a profile; use `codex exec` for non-interactive work.

## Start an interactive worker

The following Bash examples assume tmux is available and `/absolute/path/to/worker` is an existing workspace containing `BRIEF.md`. Choose one launch command and a unique session name. Record the returned pane ID and keep it with the worker's other state.

Claude Code:

```bash
wyn_pane=$(tmux new-session -d -s wyn-claude-1 -c /absolute/path/to/worker -x 160 -y 48 -P -F '#{pane_id}' claude)
```

Codex:

```bash
wyn_pane=$(tmux new-session -d -s wyn-codex-1 -c /absolute/path/to/worker -x 160 -y 48 -P -F '#{pane_id}' 'codex --no-alt-screen')
```

Codex's `--no-alt-screen` preserves terminal scrollback. Use plain `codex` if the installed version lacks it. Keep interactive stdout connected to the tmux terminal; capture the pane to observe it.

Retain `wyn_pane` explicitly between coordinator shell calls if they do not share variables. If using a separate tmux server/socket, record that too and target it consistently.

## Observe, send, verify, repeat

Read the screen first:

```bash
tmux capture-pane -p -J -S -200 -t "$wyn_pane"
```

Once the worker is ready at its input composer, send a literal prompt:

```bash
tmux send-keys -t "$wyn_pane" -l 'Read BRIEF.md and complete the assignment. Ask here if essential context is missing.'
```

Capture again to confirm delivery before submitting with a separate command:

```bash
tmux send-keys -t "$wyn_pane" Enter
```

Then observe the response and artifacts. Send follow-ups to the same pane to retain the conversation. Readiness, submission, interruption, and permission dialogs depend on the running CLI; determine their state from output rather than assuming a fixed delay or sending repeated Enter keys. A quiet pane is not proof that an assignment is complete.

For longer prompts, write a file and direct the worker to read it. This avoids shell interpolation and multiline paste ambiguities. Send control keys only after checking the target and the intended effect. User approval requirements still apply inside a worker.

The user can inspect the session with `tmux attach -t wyn-claude-1` or `tmux attach -t wyn-codex-1`. Coordinate input when the user is attached. On completion, collect artifacts and close only the worker sessions owned by the task, or preserve their IDs and state if they should continue.

## Adapt to the actual environment

Authentication, models, effort flags, and resource limits belong to the selected CLI and account. Inspect current options before configuring them; do not copy model identifiers or effort syntax between providers. Use existing authorized authentication and scope worker permissions to the assignment.

Apply WYN's budget split to both CLIs: choose an economical doing model and a more capable verification model, then configure each with its supported syntax. Record each worker's model, effort, role, and work allowance with its session target. A tmux session provides persistence, not a spending cap; enforce the bounded assignment and stop or interrupt generation when its allowance is reached.

For a challenging assignment, select a doing model one tier above the baseline while retaining the designated verifier. Resolve the intermediate model against actual availability; do not invent a GPT equivalent for Sonnet. When changing a worker's model, preserve its brief, artifacts, and relevant conversation context so the next attempt builds on completed work.

Select reasoning effort separately for each worker and verifier. Check which effort levels the chosen model supports and how the installed CLI sets them. Confirm that the requested setting took effect rather than assuming identical labels or behavior across providers. Bound any comparison of effort settings within the existing work allowance; do not turn tuning into an open-ended benchmark.

If a launch fails, inspect the actual error and choose a supported launch context or alternative. If tmux is unavailable, use an available persistent PTY facility or obtain tmux locally when practical. If only batch execution is available, retain useful context in briefs and artifacts between calls, and explain that limitation when it matters.
