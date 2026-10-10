# WYN projects, index, and publication

Read this when creating or maintaining durable WYN tooling, preparing a publication offer, or updating a published project.

## One tooling home

Use `~/wyn/` by default, or an existing tooling root selected by the user. Inspect its README before choosing a new project name. Keep projects in separate directories and repositories; the tooling home itself is a local index, not one large repository to push to GitHub.

```text
~/wyn/
  README.md                    Local tooling index
  file-converter/
    README.md                  Purpose, setup, use, checks, and language choice
    ...                        Source and relevant tests
    PUBLISHING.md              Present once publishing is planned or authorized
  another-tool/
    README.md
    ...
```

If WYN itself is cloned into this layout, use `~/wyn/wyn/` for its repository. Reserve `~/wyn/README.md` for the machine's index. Older installations may have cloned WYN directly into `~/wyn`; detect that before writing an index and preserve the existing repository README. Choose an agreed alternative root or a non-disruptive migration instead of overwriting it.

Keep existing working checkouts intact when relocation would break references. Add a project symlink under the tooling home or index the actual location, and record which path is canonical. A link is not a second checkout. Keep data, build outputs, and scratch work separate from reusable source where practical.

## Keep the index useful

The root README should explain its layout and how to use the available tooling. A compact table can provide discovery:

| Project | Purpose | Location | Language/runtime | Readiness | Publication |
| --- | --- | --- | --- | --- | --- |
| file-converter | Convert the team's interchange format | `file-converter/` | Record the actual runtime | Experimental / tested / mature | Local only, or repository URL and sync state |

Link each project README. Record non-obvious shared prerequisites and conventions once at the root, and put detailed setup, commands, checks, limitations, and the reason for a consequential language choice in the project. Maintain entries when projects change. Use evidence for readiness claims; "tested" should point to what was checked.

For published projects, include the repository URL, canonical local checkout, publication state, and last verified synchronization information in the local index. Mark pending local changes honestly. A locally recorded last-published commit is useful; do not require a commit to contain its own hash.

The index describes this machine and may include private paths and project information. Publish only the chosen project, not the whole tooling home or its index.

## Prepare a concrete offer

A sharing candidate should have a useful capability, representative checks that pass, a usable entrypoint, and enough documentation for someone else to run it. Avoid presenting a one-off fragment or an untested prototype as a mature project.

Check for `gh` and run `gh auth status` without displaying credentials. Inspect relevant repository state and remotes. If GitHub access is unavailable, retain a local candidate and report what is missing; do not create credentials or change accounts implicitly.

Before offering publication, prepare the project's README, relevant checks, and file selection. Inspect the actual files to exclude credentials, task-private data, local logs, build caches, and unrelated work. Address required attribution and licensing. State the proposed owner/name, visibility, and what the repository will contain. Mention routine maintenance pushes in the proposed scope so future synchronization can reuse the user's authorization.

If the user already authorized this project's publication and scope, proceed without asking again. Otherwise, offer the concrete result and wait for the user's decision before creating or publishing a remote repository.

## Publish and record

After authorization, use `gh` to create or select the intended repository, push the prepared commits, and verify its identity, visibility, branch, and published revision. Preserve an existing remote; do not overwrite it simply to match a command example. A link existing on GitHub is not proof that the latest local work was pushed.

Add a visible publication section to the project's README. Keep the project-local maintenance record in `PUBLISHING.md` or an equivalent existing document. Include:

- Publication state and GitHub repository URL.
- Remote and maintained branch, or the existing pull-request/release workflow.
- Validation and documentation steps required before updates.
- The user's publication and routine maintenance authorization, including limits on visibility, release creation, and other external actions.
- How to verify synchronization and record pending work in the local index.

Update the tooling-home README with the same repository and state. Keep machine-specific synchronization observations in that local index when putting them inside a commit would make them self-referential or immediately stale.

## Maintain published work

For changes to a published tool, read its publication record before editing. Check the branch, remotes, working tree, and relevant remote changes. Preserve other work. Modify the code and docs, run the relevant checks, inspect the diff, and commit the intended change.

Push or open a pull request according to the recorded workflow and existing authorization. Resolve ordinary synchronization issues without overwriting other contributors' work. Do not force-push to make divergence disappear. Verify that GitHub has the expected commit or pull request; distinguish a pushed branch from a merged default branch or a released package.

Update the local index with the observed state and any follow-up. If access, failing checks, conflicts, or required authorization prevents synchronization, record what is pending and report it. Continue on the next authorized maintenance task; do not install timers or continuous model polling to satisfy the maintenance obligation.
