# What plan should say

touchmark's check against a real fleet: `touchmark plan --assume-opt-in --all` on the 13 bedrock-python libraries, and `touchmark status` in a clone of each, match the expectation written down here. `scripts/plan-bedrock.sh` runs both and compares them with the two tables below.

## Where it stands

The rollout finished on 2026-10-07 (README, "Rollout"); the deeper starter packs of 2026-10-11 (#13) and the template's `ai-review` and `workflow` packs of 2026-11-15 (#17-#19) reached every library: all 13 sync pull requests are merged. Every library has the hub's files, so a plan changes nothing anywhere. What differs, differs on purpose:

- every library filled in `.agents/project.md`, which is therefore its own (`local`);
- mattermind keeps its own `.github/workflows/docs.yml`, since its docs dependencies are an extra, and pg-partsmith its own `.github/dependabot.yml`, which adds the `docker` ecosystem. Their `.engineering-assets.yml` lists those files under `ignore`.

The expectation holds while:

- only mattermind and pg-partsmith have an `.engineering-assets.yml`, and it only ignores those files. `targets.yml` subscribes every target (`defaults.opt_in: assumed`), so `--assume-opt-in` changes nothing;
- the organisation's repositories with the topic `python`, minus the `exclude` patterns of `targets.yml`, are these 13. A new one shows up as an unexpected target;
- touchmark has no open sync pull request in any target;
- the packs and the libraries' copies stay as they are. A change to a pack makes the copies `outdated` and the plan `opened`; a library that changes a copy makes it `local`. Either way, write the expectation again.

The default branches it was checked at, on 2026-11-16:

| Repository | Commit |
|---|---|
| aiokafka-foundation-kit | `546d55c192e4bd34307cddcee1ee3773e57acaf5` |
| alembic-gauntlet | `40d0248ff1f572eec46e1109fbef75d8cd12de79` |
| clientwright | `bf0180c6c86a245a982388c5692bb4b3d99f6306` |
| deadline-budget | `113f7125449cc92e94d9f74bfe0015d4dae42a49` |
| grpc-client-kit | `c753921317e309fb42e352380655ac616aadd070` |
| grpc-server-kit | `f057d6cfffdc6460c22b6cb7a45297885e79a4f7` |
| idempotency-kit | `98d63b79e3c4fe148541489ca7dcf1bddd7840d5` |
| mattermind | `1335af8f2b039c366b8fe2077c5eedf91d2e8c4a` |
| omni-box | `3fa8677ece901ed683a816b44e2b8865a86c3fa4` |
| pg-partsmith | `de42af8cfc4366d16a2413fa6f67752431fdc466` |
| redis-client-kit | `b8532f51668a199f7d7bb0660eba66c9bf373856` |
| servicewright | `3e147a0840d4cde6b7899a140e231ef5ad535e44` |
| sqlalchemy-foundation-kit | `b1b3ede2d01a43f0b60a2d3a7fe21c1e4f10164f` |

## Expectation

Packs of every target: `zensical-docs, bedrock-community, agents, claude, python-library, ai-review, workflow`

That is `defaults.packs` of `targets.yml`, with `agents` placed before the packs that require it. `ai-review` and `workflow` both ship `local/.gitignore`, with the same content; `workflow`, the later, is its pack. No target adds packs: the two opt-in files only ignore paths.

| Repository | Outcome | Create | Update | Delete |
|---|---|---:|---:|---:|
| `bedrock-python/aiokafka-foundation-kit` | unchanged | 0 | 0 | 0 |
| `bedrock-python/alembic-gauntlet` | unchanged | 0 | 0 | 0 |
| `bedrock-python/clientwright` | unchanged | 0 | 0 | 0 |
| `bedrock-python/deadline-budget` | unchanged | 0 | 0 | 0 |
| `bedrock-python/grpc-client-kit` | unchanged | 0 | 0 | 0 |
| `bedrock-python/grpc-server-kit` | unchanged | 0 | 0 | 0 |
| `bedrock-python/idempotency-kit` | unchanged | 0 | 0 | 0 |
| `bedrock-python/mattermind` | unchanged | 0 | 0 | 0 |
| `bedrock-python/omni-box` | unchanged | 0 | 0 | 0 |
| `bedrock-python/pg-partsmith` | unchanged | 0 | 0 | 0 |
| `bedrock-python/redis-client-kit` | unchanged | 0 | 0 | 0 |
| `bedrock-python/servicewright` | unchanged | 0 | 0 | 0 |
| `bedrock-python/sqlalchemy-foundation-kit` | unchanged | 0 | 0 | 0 |

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
| `.agents/prompts/pure-refactor.md` | agents | current | - | no |
| `.agents/prompts/refactor-check.md` | agents | current | - | no |
| `.agents/prompts/review.md` | agents | current | - | no |
| `AGENTS.md` | agents | current | - | no |
| `.claude/agents/reviewer.md` | claude | current | - | yes |
| `.claude/settings.json` | claude | current | - | yes |
| `.claude/skills/commit/SKILL.md` | claude | current | - | yes |
| `.claude/skills/new-branch/SKILL.md` | claude | current | - | yes |
| `.claude/skills/pr/SKILL.md` | claude | current | - | yes |
| `.claude/skills/review-change/SKILL.md` | claude | current | - | yes |
| `.claude/skills/spec/SKILL.md` | claude | current | - | yes |
| `CLAUDE.md` | claude | current | - | no |
| `.agents/guidelines/public-api.md` | python-library | current | - | no |
| `.agents/guidelines/python.md` | python-library | current | - | no |
| `.agents/guidelines/testing.md` | python-library | current | - | no |
| `.agents/review/README.md` | ai-review | current | - | no |
| `.agents/review/check.py` | ai-review | current | - | yes |
| `.agents/review/directions/compatibility.md` | ai-review | current | - | no |
| `.agents/review/directions/correctness.md` | ai-review | current | - | no |
| `.agents/review/directions/design.md` | ai-review | current | - | no |
| `.agents/review/directions/performance.md` | ai-review | current | - | no |
| `.agents/review/directions/security.md` | ai-review | current | - | no |
| `.agents/review/directions/tests.md` | ai-review | current | - | no |
| `.agents/review/pure-refactor.md` | ai-review | current | - | no |
| `.agents/review/review.md` | ai-review | current | - | no |
| `.agents/skills/review-change/SKILL.md` | ai-review | current | - | yes |
| `.agents/skills/commit/SKILL.md` | workflow | current | - | yes |
| `.agents/skills/implement/SKILL.md` | workflow | current | - | yes |
| `.agents/skills/new-branch/SKILL.md` | workflow | current | - | yes |
| `.agents/skills/pr/SKILL.md` | workflow | current | - | yes |
| `.agents/skills/spec/SKILL.md` | workflow | current | - | yes |
| `.claude/skills/implement/SKILL.md` | workflow | current | - | yes |
| `local/.gitignore` | workflow | current | - | no |

Sensitive files are those the pull request description lists under ⚠: touchmark's built-in list (workflows, `dependabot.yml`, `.claude/settings*.json`, `.claude/agents/**`, `.claude/skills/**`, `.agents/skills/**`, ...) and `sensitive_paths` of `hub.yml`, which adds `.agents/review/check.py`. Skills are on the list because a skill's `allowed-tools` lets Claude Code use those tools without asking.

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
