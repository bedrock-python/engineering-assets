# What plan should say

touchmark's check against a real fleet: `touchmark plan --assume-opt-in --all` on the 13 bedrock-python libraries, and `touchmark status` in a clone of each, match the expectation written down here. `scripts/plan-bedrock.sh` runs both and compares them with the two tables below.

## Where it stands

The rollout finished on 2026-10-07 (README, "Rollout"), and every library had the hub's files. On 2026-10-11 the starter packs went deeper: the review prompt reviews a large change in slices and asks every addition for its reason, a new prompt `.agents/prompts/pure-refactor.md` checks that a change keeps behaviour, `AGENTS.md` gained working principles, and the `python-library` guidelines gained concrete rules. So every library gets one sync pull request: nine files updated and one created. What differs otherwise, differs on purpose:

- every library filled in `.agents/project.md`, which is therefore its own (`local`);
- mattermind keeps its own `.github/workflows/docs.yml`, since its docs dependencies are an extra, and pg-partsmith its own `.github/dependabot.yml`, which adds the `docker` ecosystem. Their `.engineering-assets.yml` lists those files under `ignore`.

Once those pull requests are merged, a plan changes nothing anywhere again: write the expectation again then.

The expectation holds while:

- only mattermind and pg-partsmith have an `.engineering-assets.yml`, and it only ignores those files. `targets.yml` subscribes every target (`defaults.opt_in: assumed`), so `--assume-opt-in` changes nothing;
- the organisation's repositories with the topic `python`, minus the `exclude` patterns of `targets.yml`, are these 13. A new one shows up as an unexpected target;
- touchmark has no open sync pull request in any target;
- the packs and the libraries' copies stay as they are. A change to a pack makes the copies `outdated` and the plan `opened`; a library that changes a copy makes it `local`. Either way, write the expectation again.

The default branches it was checked at, on 2026-10-11:

| Repository | Commit |
|---|---|
| aiokafka-foundation-kit | `3ba88e56975e9d607aa8ce7f05ce0d7566a0108a` |
| alembic-gauntlet | `50eb84e11c667105713d5632f690e24d67b6b2d4` |
| clientwright | `7cda21512ab41266e741006329c845adf7db10f8` |
| deadline-budget | `37e0656b7bb9329df53e8b2bd03979d4a8cf47ba` |
| grpc-client-kit | `db6452920a1a2b3a8550a64fab174b5bc963cd49` |
| grpc-server-kit | `90fce7b4759eae094caf8ba2b8f0f2aef5ac914d` |
| idempotency-kit | `af413605ddd8b72361330ef5459045cf6eaabfd8` |
| mattermind | `04344c77790073691d53e77d704665270d6701ef` |
| omni-box | `c36f99f395f3fe85856d5d22305f1177df83a201` |
| pg-partsmith | `55c483a01cef9f20e530b7a43f300e190cd833ed` |
| redis-client-kit | `823a116ac0b5be68599760f7c43df055f1332b5f` |
| servicewright | `c84440df7596fce04519f3ccc7237e58c7e00aae` |
| sqlalchemy-foundation-kit | `87e97aa6ea45ae4a681491df4d31eddcfeb56eb6` |

## Expectation

Packs of every target: `zensical-docs, bedrock-community, agents, claude, python-library`

That is `defaults.packs` of `targets.yml`, with `agents` placed before the packs that require it. No target adds packs: the two opt-in files only ignore paths.

| Repository | Outcome | Create | Update | Delete |
|---|---|---:|---:|---:|
| `bedrock-python/aiokafka-foundation-kit` | opened | 1 | 9 | 0 |
| `bedrock-python/alembic-gauntlet` | opened | 1 | 9 | 0 |
| `bedrock-python/clientwright` | opened | 1 | 9 | 0 |
| `bedrock-python/deadline-budget` | opened | 1 | 9 | 0 |
| `bedrock-python/grpc-client-kit` | opened | 1 | 9 | 0 |
| `bedrock-python/grpc-server-kit` | opened | 1 | 9 | 0 |
| `bedrock-python/idempotency-kit` | opened | 1 | 9 | 0 |
| `bedrock-python/mattermind` | opened | 1 | 9 | 0 |
| `bedrock-python/omni-box` | opened | 1 | 9 | 0 |
| `bedrock-python/pg-partsmith` | opened | 1 | 9 | 0 |
| `bedrock-python/redis-client-kit` | opened | 1 | 9 | 0 |
| `bedrock-python/servicewright` | opened | 1 | 9 | 0 |
| `bedrock-python/sqlalchemy-foundation-kit` | opened | 1 | 9 | 0 |

| Path | Pack | State | Exceptions | Sensitive |
|---|---|---|---|---|
| `.github/workflows/docs.yml` | zensical-docs | current | ignored: mattermind | yes |
| `docs/assets/javascripts/copy-page.js` | zensical-docs | current | - | yes |
| `docs/assets/stylesheets/copy-page.css` | zensical-docs | current | - | no |
| `overrides/main.html` | zensical-docs | current | - | yes |
| `scripts/emit_markdown.py` | zensical-docs | current | - | yes |
| `.editorconfig` | bedrock-community | current | - | no |
| `.github/dependabot.yml` | bedrock-community | current | ignored: pg-partsmith | yes |
| `.github/workflows/release-please.yml` | bedrock-community | current | - | yes |
| `CODE_OF_CONDUCT.md` | bedrock-community | current | - | no |
| `.agents/project.md` | agents | local | - | no |
| `.agents/prompts/pure-refactor.md` | agents | missing | - | no |
| `.agents/prompts/refactor-check.md` | agents | outdated | - | no |
| `.agents/prompts/review.md` | agents | outdated | - | no |
| `AGENTS.md` | agents | outdated | - | no |
| `.claude/agents/reviewer.md` | claude | outdated | - | yes |
| `.claude/settings.json` | claude | current | - | yes |
| `.claude/skills/commit/SKILL.md` | claude | current | - | yes |
| `.claude/skills/new-branch/SKILL.md` | claude | current | - | yes |
| `.claude/skills/pr/SKILL.md` | claude | outdated | - | yes |
| `.claude/skills/review-change/SKILL.md` | claude | outdated | - | yes |
| `.claude/skills/spec/SKILL.md` | claude | current | - | yes |
| `CLAUDE.md` | claude | outdated | - | no |
| `.agents/guidelines/public-api.md` | python-library | current | - | no |
| `.agents/guidelines/python.md` | python-library | outdated | - | no |
| `.agents/guidelines/testing.md` | python-library | outdated | - | no |

Sensitive files are those the pull request description lists under ⚠: touchmark's built-in list (workflows, `dependabot.yml`, `.claude/settings*.json`, `.claude/agents/**`, `.claude/skills/**`, ...) and `sensitive_paths` of `hub.yml`. Skills are on the list because a skill's `allowed-tools` lets Claude Code use those tools without asking.

## How the rollout got here

The first expectation was computed on 2026-10-02, independently of touchmark: the blob id of every file the packs ship against the blob id of the same path in every library (`GET /repos/bedrock-python/<repo>/git/trees/HEAD?recursive=1`). It found that `zensical-docs` and `bedrock-community` matched what the libraries already had, that four libraries had files of their own, and that the starter packs were new everywhere. On 2026-10-07, with the reader App's key, `scripts/plan-bedrock.sh --status` matched it, and the rollout settled the rest:

- clientwright's and pg-partsmith's improvements to `docs.yml` went into `zensical-docs` (#5, and python-library-template#9), and both took the hub's version back (clientwright#53, pg-partsmith#99);
- grpc-client-kit took back its three copies that differed only in CRLF line endings and an older checkout action (grpc-client-kit#42);
- mattermind's `docs.yml` and pg-partsmith's `dependabot.yml` stay their own (mattermind#41, pg-partsmith#99);
- the starter packs reached deadline-budget first (deadline-budget#29), then the other twelve, and every library filled in its profile.

The per-file analysis of 2026-10-02 is in this file's history (`git log -p -- expected.md`).

## What the report cannot show

plan's JSON report counts the files each target would create, update and delete, and lists the changed paths across targets. It does not name the files it leaves alone, so a file that is `local` where `current` was expected (or the other way round) would not show. `scripts/plan-bedrock.sh --status` covers that: it clones every target anonymously with `core.autocrlf=false` and compares the state `touchmark status` gives each file with the file table.

`touchmark status` judges a file unchanged since its commit by its committed blob, as plan does: a copy committed with CRLF line endings is `local` in both, on a Windows checkout with `core.autocrlf=true` too. That is how grpc-client-kit's copies differed until it took them back. The script clones with `core.autocrlf=false` all the same, so that the files on disk are the committed bytes whatever the machine's settings.

## Format

`scripts/check_plan.py` reads three things from this file, so keep their shape when you edit it:

- the line that starts with `Packs of every target:`, with the packs in a code span, comma-separated, in layering order;
- the table whose header is `| Repository | Outcome | Create | Update | Delete |`: one row per target, the repository in a code span;
- the table whose header is `| Path | Pack | State | Exceptions | Sensitive |`: one row per file the packs ship. State is the state in every target but those under Exceptions, written `state: repo, repo; state: repo` with the repository's name without the organisation, or `-`. Sensitive is `yes` or `no`.

The checker refuses a file table that contradicts the outcomes table.
