# What plan should say

touchmark's check against a real fleet: `touchmark plan --assume-opt-in --all` on the 13 bedrock-python libraries matches the expectation written down before the run. This file is that expectation. `scripts/plan-bedrock.sh` runs the plan and compares its JSON report with the two tables below.

## How it was computed

Independently of touchmark, on 2026-10-02:

1. The blob id of every file the packs ship, from this hub's last commit (`git ls-tree -r HEAD packs/`).
2. The blob id of every file of every target at its default branch, from `GET /repos/bedrock-python/<repo>/git/trees/HEAD?recursive=1`, the same comparison as a first count of the drift on 2026-09-23. Its counts still hold: `copy-page.js`, `copy-page.css`, `overrides/main.html`, `emit_markdown.py` and `CODE_OF_CONDUCT.md` have one version across the 13 libraries; `.editorconfig`, `dependabot.yml` and `release-please.yml` two (12 of 13 agree); the pull request template and `feature_request.yml` four (10 of 13 agree); `docs.yml` five and `.gitignore` seven.
3. Per file: no blob at the path is `missing`; the hub's blob is `current`; an older blob of the same path in the hub's history is `outdated` (none yet: the hub is new); any other blob is `local`. A target creates every `missing` file, updates every `outdated` one and leaves the rest. A target with something to create or update would get a pull request (`opened`), one without stays `unchanged`.

The expectation holds while:

- no target has an `.engineering-assets.yml` of its own (none has one today). `targets.yml` subscribes deadline-budget, and `--assume-opt-in` plans the other twelve as if they had an empty one;
- the organisation's repositories with the topic `python`, minus the `exclude` patterns of `targets.yml`, are these 13. A new one shows up as an unexpected target;
- touchmark has opened no sync pull request in any target;
- the targets' copies of these files and the packs stay as they are. Any commit that changes one of them changes the expectation: compute it again.

The default branches it was computed at:

| Repository | Commit |
|---|---|
| aiokafka-foundation-kit | `ac6d350d1f47243a5873756e38f9069ccbc897c4` |
| alembic-gauntlet | `422de2f7623947e6b5f81a76a9e3aeb7a3c39d31` |
| clientwright | `90bc12656b67185f86bcdb4fda1e0af39d94f7f0` |
| deadline-budget | `19a66ccf028fffef1f7ea7871f2e14b793f8a76b` |
| grpc-client-kit | `2164662e66d50849b38fe53dd43c29f60c7784aa` |
| grpc-server-kit | `cc159ec2b2abe8a53e45289a96c17f55c8551b4d` |
| idempotency-kit | `158865d54cc9b8bacd1c3023806092d083682115` |
| mattermind | `3f0b0a39b4287f6c59011cfee2856d5a7663e472` |
| omni-box | `57ab51c7f9e366c53828c6524043914e2070120d` |
| pg-partsmith | `976a4173c7d9ab32e79f9bd613f2e2e42bfe376a` |
| redis-client-kit | `eae35d5a66af2fd09c11019b59799d0d6272a284` |
| servicewright | `dba6f5219ddf0b89bedb000b3ca3c9589122afe9` |
| sqlalchemy-foundation-kit | `95c51a712177fba8cb8e1c83087b987a0a7aab7f` |

## Expectation

Packs of every target: `zensical-docs, bedrock-community, agents, claude, python-library`

That is `defaults.packs` of `targets.yml`, with `agents` placed before the packs that require it. No target adds packs, since none has an opt-in file.

| Repository | Outcome | Create | Update | Delete |
|---|---|---:|---:|---:|
| `bedrock-python/aiokafka-foundation-kit` | opened | 15 | 0 | 0 |
| `bedrock-python/alembic-gauntlet` | opened | 15 | 0 | 0 |
| `bedrock-python/clientwright` | opened | 15 | 0 | 0 |
| `bedrock-python/deadline-budget` | opened | 15 | 0 | 0 |
| `bedrock-python/grpc-client-kit` | opened | 15 | 0 | 0 |
| `bedrock-python/grpc-server-kit` | opened | 15 | 0 | 0 |
| `bedrock-python/idempotency-kit` | opened | 15 | 0 | 0 |
| `bedrock-python/mattermind` | opened | 15 | 0 | 0 |
| `bedrock-python/omni-box` | opened | 15 | 0 | 0 |
| `bedrock-python/pg-partsmith` | opened | 15 | 0 | 0 |
| `bedrock-python/redis-client-kit` | opened | 15 | 0 | 0 |
| `bedrock-python/servicewright` | opened | 15 | 0 | 0 |
| `bedrock-python/sqlalchemy-foundation-kit` | opened | 15 | 0 | 0 |

| Path | Pack | State | Exceptions | Sensitive |
|---|---|---|---|---|
| `.github/workflows/docs.yml` | zensical-docs | current | local: clientwright, grpc-client-kit, mattermind, pg-partsmith | yes |
| `docs/assets/javascripts/copy-page.js` | zensical-docs | current | - | yes |
| `docs/assets/stylesheets/copy-page.css` | zensical-docs | current | - | no |
| `overrides/main.html` | zensical-docs | current | - | yes |
| `scripts/emit_markdown.py` | zensical-docs | current | - | yes |
| `.editorconfig` | bedrock-community | current | local: grpc-client-kit | no |
| `.github/dependabot.yml` | bedrock-community | current | local: pg-partsmith | yes |
| `.github/workflows/release-please.yml` | bedrock-community | current | local: grpc-client-kit | yes |
| `CODE_OF_CONDUCT.md` | bedrock-community | current | - | no |
| `.agents/project.md` | agents | missing | - | no |
| `.agents/prompts/refactor-check.md` | agents | missing | - | no |
| `.agents/prompts/review.md` | agents | missing | - | no |
| `AGENTS.md` | agents | missing | - | no |
| `.claude/agents/reviewer.md` | claude | missing | - | yes |
| `.claude/settings.json` | claude | missing | - | yes |
| `.claude/skills/commit/SKILL.md` | claude | missing | - | yes |
| `.claude/skills/new-branch/SKILL.md` | claude | missing | - | yes |
| `.claude/skills/pr/SKILL.md` | claude | missing | - | yes |
| `.claude/skills/review-change/SKILL.md` | claude | missing | - | yes |
| `.claude/skills/spec/SKILL.md` | claude | missing | - | yes |
| `CLAUDE.md` | claude | missing | - | no |
| `.agents/guidelines/public-api.md` | python-library | missing | - | no |
| `.agents/guidelines/python.md` | python-library | missing | - | no |
| `.agents/guidelines/testing.md` | python-library | missing | - | no |

Sensitive files are those the pull request description lists under ⚠: touchmark's built-in list (workflows, `dependabot.yml`, `.claude/settings*.json`, `.claude/agents/**`, `.claude/skills/**`, ...) and `sensitive_paths` of `hub.yml`. Skills are on the list because a skill's `allowed-tools` lets Claude Code use those tools without asking.

## What it means

**zensical-docs and bedrock-community connect with an empty diff.** Every library already has `copy-page.js`, `copy-page.css`, `overrides/main.html`, `scripts/emit_markdown.py` and `CODE_OF_CONDUCT.md` exactly as the packs ship them. Nine libraries have all nine files as shipped.

**Four libraries have files of their own** (`local`). touchmark leaves a `local` file alone and says so in the pull request: it is not a reason to block the target, and these targets get their pull request for the other packs as usual. For each, the library's maintainers decide between taking the file back under the hub (`touchmark apply --adopt <path>` in the library, through a pull request there), keeping it (`ignore` in the library's `.engineering-assets.yml`), or folding the change into the pack:

| Repository | File | How it differs from the pack | Suggested |
|---|---|---|---|
| clientwright | `.github/workflows/docs.yml` | adds `workflow_dispatch`, a `concurrency: pages` group, and `--no-dev --group docs` on `uv run` | fold into `zensical-docs`: every library gains from it, and clientwright becomes `current` |
| grpc-client-kit | `.github/workflows/docs.yml` | `actions/checkout@v6` instead of `@v7`, and CRLF line endings | `--adopt` |
| grpc-client-kit | `.editorconfig` | CRLF line endings only | `--adopt` |
| grpc-client-kit | `.github/workflows/release-please.yml` | CRLF line endings only | `--adopt` |
| mattermind | `.github/workflows/docs.yml` | adds `workflow_dispatch`; installs the docs dependencies as an extra (`--extra docs`), not a dependency group | `ignore`, unless mattermind moves its docs dependencies to a group |
| pg-partsmith | `.github/workflows/docs.yml` | `uv sync --locked` | fold `--locked` into `zensical-docs`, or `ignore` |
| pg-partsmith | `.github/dependabot.yml` | adds the `docker` ecosystem for its image, labels instead of `day: monday` | `ignore`: the image is pg-partsmith's own |

grpc-client-kit also keeps its pull request template and `feature_request.yml` with CRLF line endings; no pack ships them.

**The starter packs are new everywhere.** No library has `AGENTS.md`, `CLAUDE.md`, or anything under `.agents/` or `.claude/`, so every target would get one pull request that creates the files of `agents`, `claude` and `python-library`.

Two things to know about that pull request:

- `python-library` ships its guidelines to `.agents/guidelines/`, not to `docs/`: `docs/` is the libraries' zensical `docs_dir`, and the guidelines would have been published on every documentation site as pages no menu links to. The template's starter packs made the same move.
- `.claude/settings.json`, `.claude/agents/reviewer.md` and the five skills under `.claude/skills/` are sensitive: the pull request lists them under ⚠.

## What the report cannot show

plan's JSON report counts the files each target would create, update and delete, and lists the changed paths across targets. It does not name the files it leaves alone, so a file that is `local` where `current` was expected (or the other way round) would not show. `scripts/plan-bedrock.sh --status` covers that: it clones every target anonymously with `core.autocrlf=false` and compares the state `touchmark status` gives each file with the file table.

`touchmark status` judges a file unchanged since its commit by its committed blob, as plan does, so grpc-client-kit's `.editorconfig` and `release-please.yml`, which differ from the pack only in line endings, are `local` in both, on a Windows checkout with `core.autocrlf=true` too. The script clones with `core.autocrlf=false` all the same, so that the files on disk are the committed bytes whatever the machine's settings.

## Runs so far

All on 2026-10-02, with touchmark `c79e14e`:

- **Without a token**, `touchmark plan` exits 2 before any request: `provider gh: no read credential: set TOUCHMARK_GH_READ_TOKEN, or TOUCHMARK_GH_READ_APP_ID and TOUCHMARK_GH_READ_APP_KEY`. A local plan always needs a read credential; touchmark reads anonymously only the providers that a hub pull request adds or changes.
- **Anonymously**, with GitHub Actions variables set by hand so that touchmark took the run for a hub pull request whose default branch it cannot tell, which plans every provider without credentials. GitHub allows an address without a token 60 API requests an hour, and the run stopped there (exit 0, the rest `deferred:rate-limit`):
  - with only `zensical-docs` and `bedrock-community` assigned, nine targets were planned in full, all `unchanged` as expected: aiokafka-foundation-kit, alembic-gauntlet, clientwright, deadline-budget, grpc-client-kit, grpc-server-kit, idempotency-kit, mattermind and omni-box. pg-partsmith and redis-client-kit stopped at "list pull requests", servicewright and sqlalchemy-foundation-kit at "open the target's repository": about six requests per unchanged target;
  - with this hub as committed, a target with changes costs more. aiokafka-foundation-kit was planned in full: `opened`, 15 files to create, as expected. alembic-gauntlet, clientwright and grpc-client-kit stopped at "read the rules of the target's branches", deadline-budget, grpc-server-kit, idempotency-kit and mattermind at "read the sync branches", each after counting its 15 files to create, as expected; omni-box, pg-partsmith, redis-client-kit, servicewright and sqlalchemy-foundation-kit waited for the limit before their snapshot.

  Both runs warn that the writer's bot login is unknown to GitHub: the App does not exist yet.
- **`scripts/plan-bedrock.sh --status-only`** on Windows and in a Linux container: every file of the 13 targets is in the state the file table gives.
- **With the reader App's key**, on 2026-10-07: `TOUCHMARK_GH_READ_APP_ID=... TOUCHMARK_GH_READ_APP_KEY=... TOUCHMARK_HUB_FP=github.com/1408350934 scripts/plan-bedrock.sh --status`, in a `golang:1.27` container for its git 2.47 (`plan` needs git 2.45 or newer): plan and status match expected.md, 13 targets and 24 files. The only warning says that a local run cannot read the tip of the hub's default branch.

## Format

`scripts/check_plan.py` reads three things from this file, so keep their shape when you edit it:

- the line that starts with `Packs of every target:`, with the packs in a code span, comma-separated, in layering order;
- the table whose header is `| Repository | Outcome | Create | Update | Delete |`: one row per target, the repository in a code span;
- the table whose header is `| Path | Pack | State | Exceptions | Sensitive |`: one row per file the packs ship. State is the state in every target but those under Exceptions, written `state: repo, repo; state: repo` with the repository's name without the organisation, or `-`. Sensitive is `yes` or `no`.

The checker refuses a file table that contradicts the outcomes table.
