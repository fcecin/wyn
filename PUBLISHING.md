# Publication and maintenance

This WYN project is **published** at [fcecin/wyn](https://github.com/fcecin/wyn).
The repository is public and uses the [MIT license](LICENSE).

## Repository

- Git remote: `origin`, pointing to `fcecin/wyn` on GitHub.
- Maintained branch: `main`.
- Workflow: validate the intended changes, commit, and push to `origin/main`.
- Use the existing Git signing configuration. Preserve unrelated local work.

## Authorization

The owner requested creation and publication of this repository and ongoing
maintenance of published WYN projects. Routine updates to this skill, its
installer, tests, and documentation may be synchronized to the existing public
repository within that scope. Reuse this authorization without asking again
for each maintenance push.

Changing visibility, deleting the repository, publishing another project, or
creating a release requires the corresponding user instruction. Use the existing
authorized GitHub account and check that the remote still identifies this project.

## Before and after an update

1. Read the project README and this file. Inspect the working tree, branch,
   remotes, and relevant remote changes.
2. Keep the README, skill, and supporting references consistent. For installer
   or activation-template changes, run `python3 -m unittest discover -s tests -v`
   and `bash -n install.sh`. For documentation changes, check local links and
   skill metadata. Run `git diff --check` for all changes.
3. Inspect and commit only the intended changes, then push to `origin/main`.
   Preserve others' work when resolving divergence; do not force-push.
4. Verify that GitHub's `main` has the expected commit. Update the machine's
   WYN index with the repository URL, canonical checkout, validation, and last
   verified synchronization state. Keep this machine-specific record local.
5. If activation templates changed, refresh the installed hosts with the local
   installer and check its status. Skill-content changes are picked up through
   the existing links.

If checks, access, conflicts, or authorization prevent publication, record the
pending work in the local index and report it. Do not describe the project as
synchronized until the remote revision has been checked. Continuous background
maintenance is not required.
