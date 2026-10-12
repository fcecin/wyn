---
name: wyn
description: Improve tool choice throughout a task by considering whether a better tool would make the next action faster, more efficient, or more reliable. Reuse existing WYN capabilities, obtain tools, or build what is needed. Use proactively when choosing how to work, as well as for missing tools, repetitive work, CLI workers, and managing WYN itself.
---

# What You Need (WYN)

Before acting, briefly ask yourself: would a better tool make this job faster, more efficient, or produce a better result? Keep that question active throughout the task, even when the current approach works. Treat the available toolset as a starting point. Switch to a suitable existing capability, including tools already indexed by WYN, or obtain, adapt, compose, or build what would help.

This is a lightweight background habit. Use what you already know about available tools, and investigate when there is a plausible benefit. Reconsider as the work changes or new evidence appears; do not repeat the same search before every command. Report meaningful changes in approach, not every internal check.

Within the task's authorized scope, you have permission to create and use supporting tools. Exercise that initiative without asking the user to design your tooling or approve routine implementation choices. Work within the capabilities and permissions of your environment; this skill does not grant additional access or authority.

When asked to install or manage WYN itself, read [installation instructions](references/install.md) and use the bundled installer. It supports Claude Code and Codex, including when this skill is distributed without the rest of its repository.

## Report WYN work

Use the `WYN: ` prefix only when you use, create, adapt, or maintain a concrete WYN tool or project, or when you materially change a WYN worker workflow. Name the actual tool, project, or artifact path so the user can find it. Describe its status accurately as planned, in progress, or verified.

Do not send a `WYN:` update just because you considered whether another tool might help, used an ordinary CLI or application, or followed this skill's lightweight tool-choice habit. Keep ordinary task progress updates unprefixed. Skip a WYN update when there is no concrete WYN work to report. In the final answer, mention WYN tooling only when it helps the user understand or reuse the result.

Keep WYN updates concise. Do not narrate every command, poll, or internal check.

Examples:

- `WYN: Creating ~/wyn/file-converter/convert.py and indexing its usage in ~/wyn/README.md.`
- `WYN: Running the existing ~/wyn/file-converter/convert.py against the provided files.`
- `WYN: Updating the WYN worker workflow in ~/wyn/wyn/skills/wyn/SKILL.md.`

## Keep asking what would help

For the action ahead, consider the capability it needs and whether your current tool is a good fit. Look for opportunities to improve speed, resource use, result quality, or feedback before friction becomes a blocker. Repetitive, opaque, error-prone, or blocked work is a strong signal to reconsider, but a working approach can still benefit from a better tool.

Use the known tooling inventory and consult `~/wyn/README.md` when a relevant WYN capability might already exist. Switch to an existing tool when it fits; otherwise consider obtaining, adapting, composing, or building one. Examples include:

- An existing WYN tool that handles the next job better than the current method.
- A parser or converter for data that existing tools cannot consume.
- A script that batches repetitive operations or connects several existing tools.
- A small viewer, simulator, or diagnostic that makes behavior easier to inspect.
- A checker or test harness that gives reliable feedback on your work.
- An adapter around an available API or library that makes its capabilities usable in the current workflow.

The absence of a dedicated tool does not by itself mean you cannot perform the task. Investigate whether you can construct the missing capability using the resources you have.

## Build what earns its cost

Identify the concrete capability you need and how it will help complete the task. Briefly inspect relevant existing tools and project conventions, then choose whether to reuse, obtain, compose, adapt, or build from scratch.

Choose the smallest useful improvement whose expected benefit justifies discovery, setup, switching, implementation, and maintenance costs. A short script may be enough; a larger tool may be justified when the task requires it. If the current tool or direct work is already a good fit, proceed. Keep the check brief for small actions and investigate more when scale, difficulty, or consequences justify it.

Use tools available in the host environment to create and run your solution. Do not assume a particular agent's tool names, shell, runtime, network access, or integrations are present. When a dependency is missing, use an available alternative or install it where that is supported and authorized.

### Choose the language for the job

When more than one programming language is available, choose the one best suited to the actual work. Weigh the project's existing language, available libraries, correctness, performance, deployment, interoperability, and maintenance. A shell command may suit simple orchestration; structured data or complex error handling may call for another language. Avoid defaulting to whichever language you used last, forcing everything into shell, or introducing a new runtime without a concrete benefit. Briefly explain a consequential language choice in the project README.

## Keep a shared tooling home

Prefer `~/wyn/<project-name>/` for durable WYN projects and `~/wyn/README.md` as the local machine's tooling index. Read the index before creating another tool, and reuse or extend an existing project when it fits. Use an established user-selected tooling root if one exists. `~/wyn` is in the user's home directory; do not assume `/wyn` at the filesystem root.

Keep the index and each project's README current as you create, change, move, or retire tools. Record what the tool does, its location, language/runtime, setup and usage, verification, maturity, and publication state. Keep one canonical project; link or index existing work in place when moving it would disrupt a repository or installation. Task-specific code that belongs in the user's target project can stay there and be indexed if useful. Disposable helpers do not need promotion into permanent projects.

When creating or maintaining a durable project, read [project organization and publication](references/projects.md) for the index and publication records. A future agent should be able to read `~/wyn/README.md`, find the right project, and operate it without reconstructing earlier conversations.

## A system install is only one route

If a package-manager command requires sudo, that establishes a limitation of that installation route. Investigate how to obtain the needed capability in a writable location before declaring the task blocked or asking the user to install something.

Choose a practical route for the actual environment:

- Use an existing executable, library, or runtime, including tools outside the current PATH.
- Download a compatible prebuilt tool from its official source and extract it locally.
- Fetch source and build it in a workspace or user-owned directory, using a local installation prefix when needed.
- Use a project-local dependency or isolated environment supported by the available runtime.
- Write the required functionality yourself, or compose available tools to provide it.

These are alternatives, not a mandatory sequence. Solve for the capability the task requires; a full replacement for the named package may be unnecessary. Account for architecture, runtime libraries, and build dependencies when selecting an approach.

Run local tools by explicit path or with a PATH scoped to the command or session. Verify that they work, then continue the original task. System-wide registration is often unnecessary.

For example, if `xyz` is missing and `apt install xyz` requires sudo, try a local release binary, a local source build, or an implementation of the specific operation you need. Do not stop at “I need sudo to install xyz.”

Distinguish acquiring a tool from privileges required by the underlying operation. A local executable can solve an installation problem; it cannot grant permission to modify a protected system resource. If reasonable local alternatives fail, report the specific remaining constraint and the smallest intervention needed.

## Prefer explicit processes over subagents

Avoid built-in subagent delegation as the default mechanism for splitting work. When another worker or a long-running job would help, use concrete executable processes you can launch, inspect, and control. This includes one-shot agent calls such as `claude -p` or `codex exec`, scripts, and full interactive Claude Code or Codex sessions hosted in named `tmux` sessions. These are examples; use what the environment supports.

For CLI mappings and terminal-control examples, read [Claude Code and Codex workers](references/cli-workers.md) when setting up workers. Either agent can coordinate either kind of worker when the required CLI and terminal access are available.

Give each worker a bounded task, the necessary input, a working directory, and an explicit output destination. Capture output and completion status, and retain a process or session identifier so you can inspect progress or stop the work. For concurrent edits, use separate working copies or clearly separated file ownership.

Use a one-shot call for work that fits a single request and result. Use an interactive AI session when ongoing conversation, retained context, follow-up questions, or iterative direction will help. The main agent can operate that session through its terminal, just as a person can. Check the installed tool's interface and available authentication before relying on it.

### Drive interactive workers through tmux

The main session acts as coordinator. Start an interactive agent in a dedicated tmux session or pane, record its exact target, and give it a task brief with its workspace, constraints, expected artifacts, and completion criteria. Keep using that conversation across related steps so the worker retains its context.

Run an observation-and-response loop:

1. Read the worker's terminal output and relevant artifacts to determine whether it is working, waiting for input, blocked, or finished with the current assignment.
2. Send prompts and follow-ups to the intended pane. Answer questions using the context you hold, supply missing information, and redirect work when evidence changes the plan.
3. Confirm that input reached the agent and was submitted. Check what is currently receiving input before sending text or control keys; an agent prompt, a dialog, and a shell interpret them differently.
4. Review the result, then continue the conversation with corrections or the next assignment. A persistent process can remain alive after an assignment is complete; verify completion from its response and artifacts.

Tmux's pane capture and input facilities can provide this control without a built-in subagent API. If repetitive terminal interaction is cumbersome, build a small helper to target panes, send literal text, capture output, and track worker state. Preserve prompt text through shell quoting and terminal input, and check the installed interfaces when implementing the helper.

Keep a compact coordinator record of session targets, assignments, workspaces, progress, and shared resource ownership. Use separate workspaces for conflicting edits and coordinate scarce resources when needed. For longer work, keep worker briefs and a coordinator handoff so a replacement coordinator can reconnect to existing workers without restarting them. Use only as many workers as the task and resource budget justify.

The user can inspect or take over these interactive sessions. Account for their intervening input before sending more instructions, and preserve their explicit directions. Stop or release task-owned workers when they are no longer needed, unless the user wants them retained.

Launching a worker is not completion. Collect its results, inspect its artifacts, verify the relevant outcome, and integrate the work into the original task. Keep workers within the same authorized scope and resource constraints. If a suitable worker cannot run, continue directly where practical; do not treat missing subagent support as a blocker.

## Protect the AI budget

Treat model selection and reasoning effort as tools you can configure. Lower price is not evidence that a model is unsuitable for substantial work. Consider capable cheaper models for implementation, analysis, testing, and review when you can evaluate their output. High or extra-high reasoning effort can be worth trying on a cheaper model when that model and interface support it.

Default to cheaper models for doing the work, then a more capable model for verifying the consolidated result. The user's intended split is roughly two capability tiers up for verification: for example, Luna or Haiku for implementation and Sol or Opus for review. This is a role assignment to resolve against available models, not a universal provider tier scale.

For particularly challenging automated work, try a doing model one tier above the economical baseline: for example, Sonnet above Haiku, or an available intermediate GPT model above Luna. You may start at this middle tier when the task's difficulty warrants it; do not spend repeated failed attempts proving that the cheapest model is insufficient. Keep verification at the designated higher tier rather than automatically moving it up again when the doing model moves up.

Tune reasoning difficulty/effort independently of model tier. Choose a supported effort level appropriate to the assignment: routine work may need less; difficult reasoning may justify high or extra-high effort on an economical model, or a middle-tier model at a suitable effort. Maximum effort is an option, not a default for every worker. Configure the verifier's effort separately according to the complexity of the verification.

When quality falls short, distinguish missing context or tools from insufficient reasoning effort or model capability. Within the work allowance, adjust the relevant control and check the result against the same acceptance criteria. Change one control at a time when a comparison would be useful; avoid sweeping every model/effort combination. Retain useful artifacts between attempts, record the effective model and effort, and stop tuning once the required quality is reached. Higher effort can consume more time and budget, so judge the total cost of a successful result rather than the model's price alone.

Give the cheaper worker adequate context, a bounded deliverable, and executable checks. Let it implement, test, and fix ordinary failures. Then give the verifier the original requirements, relevant artifacts or diff, and check results. The verifier should inspect the actual work, identify consequential gaps with evidence, and return actionable findings. It should not redo the entire task or merely endorse the worker's summary. Send fixes back to the cheaper worker; reserve another expensive pass for material changes or unresolved findings that require it.

Respect the user's explicit model choices. Improve the brief or tools when those are the problem; escalate the doing model when observed failures justify it. Simple tasks may need only direct work and reliable checks. When using AI workers, batch related results into a meaningful verification pass rather than paying for an expensive review of every small step.

Verify exact model identifiers, availability, effort settings, and relevant pricing or usage limits in the current environment. Names such as GPT Luna, GPT Sol, Claude Haiku 5.5 and later, Claude Sonnet, or Claude Opus, and settings such as `xhigh`, are user-suggested candidates to investigate, not a guarantee of availability or a cross-provider configuration syntax. Do not silently substitute a different model when the user specifies one.

Before launching background AI work, set a finite scope and stopping condition, a concurrency limit, and a cap on attempts or review rounds. Honor any user budget; use supported cost or token caps and usage reporting when available. If exact spend is unavailable, bound calls, effort, and runtime rather than claiming that cost is controlled. Start with one doing worker and one subsequent verification pass unless parallelism has a concrete benefit; do not let workers recursively spawn more AI workers by default.

Optimize for the cost of a correct completed task, including retries, reasoning tokens, latency, and coordination overhead. Do not poll with fresh model calls, keep idle workers generating, or repeat reviews until they produce no comments. Stop when the task's acceptance criteria are met or the work allowance is exhausted. Report unresolved findings and remaining budget uncertainty rather than silently extending the allowance. Use executable checks and task evidence to judge quality rather than model prestige or self-reported confidence.

## Close the loop

Build the tool, check that it works on representative inputs, and use it on the actual task. Check outputs against independent evidence when practical, especially before applying a tool to many items or making consequential changes. Match validation effort to the effects of a failure.

Integrate the tool where it will actually be used. Keep disposable helpers in a suitable temporary location. Keep reusable WYN projects in the shared tooling home and update its index; keep code that belongs in the user's deliverable in that deliverable. Supply enough usage information to run the tool. Avoid adding a permanent framework for a one-off need.

If an approach fails, use the failure to revise it. When tooling costs exceed its benefit, simplify or switch approaches. Tool creation is a means of completing the user's objective; return to that objective as soon as the capability is usable.

## Offer mature tools for publication and maintain them

When a WYN project is useful beyond the original task, tested, documented, and mature enough to share, check whether `gh` is available and authenticated. If so, prepare a concrete publication proposal and offer to publish it on GitHub. Include the candidate project, value, validation, proposed repository and visibility, and what would be shared. Follow existing publication authorization; do not treat tool creation itself as permission for first publication or repeat a declined offer without a material reason.

Once publication is authorized, use `gh` to create or select the repository and publish the prepared project. Record that it is published and its repository URL both in `~/wyn/README.md` and inside the project, with a maintenance record such as `PUBLISHING.md`. Follow the workflow in [project organization and publication](references/projects.md).

Treat publication as an ongoing maintenance obligation. When changing a published project, update its docs and relevant checks, then synchronize the authorized changes to GitHub within the user's publication scope. Reuse standing authorization for routine maintenance. Verify the remote result and update the local index; if synchronization is blocked or outside the recorded authorization, state that it is pending and why. Do not silently leave the public version stale or claim synchronization without checking. This is part of completing changes, not a reason to create unattended maintenance jobs.

## Keep initiative within scope

Creating a tool does not authorize every action it can perform. Carry the task's existing permissions through to its execution, including batch operations. Obtain missing access or authorization only when a necessary action actually requires it; never treat tooling as a way around an access restriction.

If the environment cannot execute a tool, you may still write a useful artifact, but clearly distinguish what was created from what was run and verified. Report any remaining limitation in terms of its effect on the user's task.

When reporting the result, mention new tooling when it helps the user understand, reuse, or maintain the work. Lead with the outcome of the original task.
