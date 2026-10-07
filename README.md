# bedrock-python engineering assets

> The files every bedrock-python library shares, delivered to each of them as a pull request: the documentation site's assets and workflow, community and release settings, and instructions for coding agents.

This is the hub of the bedrock-python organisation, created from [engineering-assets-template](https://github.com/bedrock-python/engineering-assets-template). Its CI runs [touchmark](https://github.com/bedrock-python/touchmark): whenever a pack changes, every library the hub subscribes gets a pull request with the change, and a file a library has made its own stays its own.

*Running since 2026-10-07: every library is subscribed and has the hub's files. [Rollout](#rollout) says how it went.*

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

The first two packs are the files python-library-template gives every new library, taken from its `template/` directory at commit `a1a1e7d` (`CODE_OF_CONDUCT.md` from the repository root, which is the rendered `CODE_OF_CONDUCT.md.jinja`). Their blob ids are the ones the libraries already have, so for every library that never changed them, touchmark recognises them as shipped and connects them with an empty diff. Keep python-library-template and these packs in step: a change goes to the pack here, and the same bytes to the template, so new libraries start in sync. The first such change, on 2026-10-07: `docs.yml` takes clientwright's `workflow_dispatch`, `concurrency: pages` and `--no-dev --group docs` on `uv run`, and pg-partsmith's `uv sync --locked`.

`targets.yml` selects the libraries created from python-library-template, the organisation's repositories with the topic `python` but mr-review, the blog and the template itself, and gives each all five packs. The libraries share one owner with the hub, so the hub subscribes them itself (`opt_in: assumed`) instead of waiting for an `.engineering-assets.yml` in each; a library chooses packs or ignores files by adding that file, and opts out with `enabled: false` in it. The subscription rolled out in two steps ([Rollout](#rollout)): deadline-budget first, then every library.

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

The repository is public: the organisation is on GitHub Free, where environment secrets exist only in public repositories, and without them the write key cannot be limited to `master`. A ruleset protects `master`: changes only through pull requests with an approving review and a review from Code Owners, no force pushes, no deletion. GitHub doesn't let anyone approve their own pull request, so organisation admins may merge a pull request without them. GitHub Actions were off until the first run ([Rollout](#rollout)); the workflow's `check` job is a required status check, and its default token is read-only.

touchmark is pinned to v0.1.0: the Action in `.github/workflows/engineering-assets.yml` by the commit of its tag, `# v0.1.0` after it. The Action at that commit runs the image of v0.1.0 by digest once it has verified the image's build provenance, so there is no image digest to pin here. Dependabot proposes the next release.

**The GitHub Apps.** Both are installed on the 13 libraries only (*Only select repositories*), never on this hub, with no webhook:
- `bedrock-python-assets-read`: Metadata, Contents and Pull requests read-only;
- `bedrock-python-assets-write`: Metadata read-only; Contents, Pull requests and Workflows read and write. Its bot, `bedrock-python-assets-write[bot]`, is `writer` in `hub.yml`.

The reader's keys are the repository variable `TOUCHMARK_READ_APP_ID` and secret `TOUCHMARK_READ_APP_KEY`. The writer's are the variable `TOUCHMARK_WRITE_APP_ID` and the secret `TOUCHMARK_WRITE_APP_KEY` of the environment `touchmark-distribute`, whose deployment branches are *Selected branches and tags* with the one rule `master` (not *Protected branches only*: with no branch rules, every branch qualifies), and nowhere else. With the reader's key, `scripts/plan-bedrock.sh --status` matched expected.md on 2026-10-07.

`python-library` ships its guidelines to `.agents/guidelines/`, as the template's starter packs do, not to `docs/`, which the libraries publish as their documentation sites.

## Rollout

1. **The first library**, 2026-10-07. GitHub Actions on, and Run workflow: the hub opened one sync pull request, in deadline-budget (bedrock-python/deadline-budget#29, 15 files), the one library `targets.yml` subscribed then. A review of it changed the starter packs before the merge: the guidelines moved to `.agents/guidelines/`, and `AGENTS.md` says what agents do while `.agents/project.md` is blank. deadline-budget then filled in its profile (bedrock-python/deadline-budget#31), which is its own from then on.
2. **Every library**, 2026-10-07: `defaults.opt_in: assumed` in `targets.yml`. Its merge opens a sync pull request in each of the other twelve libraries, which says the hub subscribed it and how to opt out.
3. **The libraries' own files**, 2026-10-07. clientwright's and pg-partsmith's improvements to `docs.yml` went into `zensical-docs` (#5) and both took the hub's version back; grpc-client-kit took back three copies that differed only in line endings; mattermind keeps its own `docs.yml` and pg-partsmith its own `dependabot.yml`, through `ignore` in their `.engineering-assets.yml`. Every library filled in its `.agents/project.md`. expected.md describes the result.

After that, the hub runs itself: `distribute` on every merge to `master` and daily, `doctor` weekly. A new library joins once it has the topic `python` and both Apps are installed on it; a new Python repository that is not a library goes under `exclude` in `targets.yml`. In a public repository GitHub disables scheduled workflows after 60 days without activity; re-enable the workflow if the daily run stops.

## License

The hub's own files and the starter packs are MIT-0, like the template ([LICENSE](LICENSE)). The files of `zensical-docs` and `bedrock-community` are the organisation's own, copied from python-library-template, which has no license file; `CODE_OF_CONDUCT.md` is adapted from the Contributor Covenant and keeps its attribution.
