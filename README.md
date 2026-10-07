# bedrock-python engineering assets

> The files every bedrock-python library shares, delivered to each of them as a pull request: the documentation site's assets and workflow, community and release settings, and instructions for coding agents.

This is the hub of the bedrock-python organisation, created from [engineering-assets-template](https://github.com/bedrock-python/engineering-assets-template). Its CI runs [touchmark](https://github.com/bedrock-python/touchmark): whenever a pack changes, every library the hub subscribes gets a pull request with the change, and a file a library has made its own stays its own.

*Not running yet: the workflow waits for the hub's GitHub Apps and their keys. [Before the first run](#before-the-first-run) lists what is left.*

```
bedrock-python/engineering-assets          this hub: packs/, hub.yml, targets.yml
        │  one pull request per library on every change to a pack
        ▼
bedrock-python/clientwright, …             the libraries: topic python, subscribed by the hub
```

## Packs

| Pack | Ships | Source |
|---|---|---|
| `zensical-docs` | `docs/assets/javascripts/copy-page.js`, `docs/assets/stylesheets/copy-page.css`, `overrides/main.html`, `scripts/emit_markdown.py`, `.github/workflows/docs.yml` | [python-library-template](https://github.com/bedrock-python/python-library-template), byte for byte |
| `bedrock-community` | `CODE_OF_CONDUCT.md`, `.editorconfig`, `.github/dependabot.yml`, `.github/workflows/release-please.yml` | python-library-template, byte for byte |
| `agents` | `AGENTS.md`, the project profile `.agents/project.md` to fill in, review prompts | the template's starter pack |
| `claude` | Claude Code instructions, settings, skills and a reviewer agent | the template's starter pack |
| `python-library` | guidelines for public APIs, versioning and deprecation | the template's starter pack |

The first two packs are the files python-library-template gives every new library, taken from its `template/` directory at commit `a1a1e7d` (`CODE_OF_CONDUCT.md` from the repository root, which is the rendered `CODE_OF_CONDUCT.md.jinja`). Their blob ids are the ones the libraries already have, so for every library that never changed them, touchmark recognises them as shipped and connects them with an empty diff. Keep python-library-template and these packs in step: a change goes to the pack here, and the same bytes to the template, so new libraries start in sync.

`targets.yml` selects the libraries created from python-library-template, the organisation's repositories with the topic `python` but mr-review, the blog and the template itself, and gives each all five packs. The libraries share one owner with the hub, so the hub subscribes them itself (`opt_in: assumed`) instead of waiting for an `.engineering-assets.yml` in each; a library chooses packs or ignores files by adding that file, and opts out with `enabled: false` in it. The subscription rolls out in two steps ([Before the first run](#before-the-first-run)): deadline-budget first, then every library.

A new library is a target once it has the topic `python` and both of the hub's GitHub Apps are installed on it: the Apps are installed on selected repositories only, since the writer must not reach this hub.

## What a sync would do

[expected.md](expected.md) says, per library and file, what `touchmark plan` should report today: the first two packs change nothing, four libraries keep files of their own (`local`), and every library would get one pull request with the starter packs. It also suggests, per `local` file, whether to adopt it, ignore it or fold its change into the pack.

Check it in one command, with a read-only GitHub token (a fine-grained token with the default *Public repositories* access is enough, since every target is public):

```sh
export TOUCHMARK_GH_READ_TOKEN=...      # never committed, never printed
scripts/plan-bedrock.sh --status
```

The script builds touchmark from `../touchmark` (or uses `$TOUCHMARK_BIN`), runs `touchmark check`, then `touchmark plan --assume-opt-in --all --format json`, and compares the report with expected.md (`scripts/check_plan.py`). `--status` also clones every library anonymously and compares the state of every file; `--status-only` does just that, without a token. Exit 0 means the plan matches.

## How this hub was made

The way a new organisation would:

1. **From the template.** The first commit is the template's files at its first published commit, as if created with *Use this template*: GitHub starts such a repository with one commit.
2. **Made ours** in the second commit, so `git diff HEAD~1 HEAD` (or the commit on GitHub) shows everything an organisation changes:
   - `hub.yml`: `id: bedrock-python` (sync branch `touchmark/bedrock-python`); one GitHub provider `gh` with the writer App's bot as a placeholder; security settings kept at `write_isolation: platform` and `private_targets_in_public_hub: skip`; `sensitive_paths` for the documentation site's script, HTML and JavaScript; metadata of the packs we use.
   - `targets.yml`: the repositories of `bedrock-python` with the topic `python`, minus the three that are not libraries (mr-review, an application with its own agent setup; the blog; python-library-template itself), which on 2026-10-07 were the 13 libraries; deadline-budget subscribed as the first step of the rollout.
   - `packs/zensical-docs` and `packs/bedrock-community` added; the starter packs `python-service` and `gitlab` removed, since our libraries are neither services nor on GitLab.
   - CI for other platforms removed (`.gitlab-ci.yml`, `.gitlab/`, `.gitea/`, `renovate.json`), as the template's README allows: this hub lives on GitHub. `.github/CODEOWNERS` names the organisation's maintainer.
   - The expectation: `expected.md`, `scripts/plan-bedrock.sh` and `scripts/check_plan.py`.

`touchmark check` passes on the result, and so does the template's `scripts/validate.sh` (check, then actionlint on the workflows).

The repository is public: the organisation is on GitHub Free, where environment secrets exist only in public repositories, and without them the write key cannot be limited to `master`. A ruleset protects `master`: changes only through pull requests with an approving review and a review from Code Owners, no force pushes, no deletion. GitHub doesn't let anyone approve their own pull request, so organisation admins may merge a pull request without them. GitHub Actions stay off until the first run (below), so that neither a push nor the daily schedule starts a workflow without its keys.

touchmark is pinned to v0.1.0: the Action in `.github/workflows/engineering-assets.yml` by the commit of its tag, `# v0.1.0` after it. The Action at that commit runs the image of v0.1.0 by digest once it has verified the image's build provenance, so there is no image digest to pin here. Dependabot proposes the next release.

## Before the first run

In order:

1. **Run the check** with a read token: `TOUCHMARK_GH_READ_TOKEN=... scripts/plan-bedrock.sh --status` exits 0. If a library changed one of these files since 2026-10-02, recompute expected.md first.
2. **Create the GitHub Apps** in bedrock-python and install each on the 13 libraries only (*Only select repositories*), never on this hub:
   - `bedrock-python-assets-read`: Metadata, Contents and Pull requests read-only;
   - `bedrock-python-assets-write`: Metadata read-only; Contents, Pull requests and Workflows read and write.

   If GitHub gives the writer a different name, set `writer` in `hub.yml` to its bot login (`<slug>[bot]`).
3. **Store the keys** in this repository:
   - reader: the variable `TOUCHMARK_READ_APP_ID` and the secret `TOUCHMARK_READ_APP_KEY`;
   - writer: an environment `touchmark-distribute` with Deployment branches set to *Selected branches and tags*, rule `master`, holding the variable `TOUCHMARK_WRITE_APP_ID` and the secret `TOUCHMARK_WRITE_APP_KEY`, and nowhere else. Not *Protected branches only*: with no branch rules, every branch qualifies.
4. **Decide where `python-library`'s guidelines go** before any library gets them: in the libraries' `docs/`, where the documentation site would publish them, or out of `docs/` through a change to the pack (expected.md).
5. **Turn GitHub Actions on** (Settings → Actions → General), add the workflow's `check` job as a required status check of `master`'s ruleset, and start the workflow (Actions → engineering-assets → Run workflow). Its first run opens one sync pull request, in deadline-budget, the library `targets.yml` subscribes for the first step of the rollout. Read it and merge it.
6. **Decide the `local` files** of expected.md: adopt (`touchmark apply --adopt <path>` in the library, through a pull request there), ignore (`ignore` in an `.engineering-assets.yml` the library adds), or fold the change into the pack here.
7. **Subscribe every library**: in `targets.yml`, uncomment `opt_in: assumed` under `defaults` and drop the deadline-budget entry, through a pull request here. Its merge opens a sync pull request in each of the other twelve libraries, which says the hub subscribed it and how to opt out.

After that, the hub runs itself: `distribute` on every merge to `master` and daily, `doctor` weekly. A new library joins once it has the topic `python` and both Apps are installed on it; a new Python repository that is not a library goes under `exclude` in `targets.yml`. In a public repository GitHub disables scheduled workflows after 60 days without activity; re-enable the workflow if the daily run stops.

## License

The hub's own files and the starter packs are MIT-0, like the template ([LICENSE](LICENSE)). The files of `zensical-docs` and `bedrock-community` are the organisation's own, copied from python-library-template, which has no license file; `CODE_OF_CONDUCT.md` is adapted from the Contributor Covenant and keeps its attribution.
