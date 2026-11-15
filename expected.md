# What plan should say

touchmark's check against a real fleet: `touchmark plan --assume-opt-in --all` on the 13 bedrock-python libraries, and `touchmark status` in a clone of each, match the expectation written down here. `scripts/plan-bedrock.sh` runs both and compares them with the two tables below.

## Where it stands

The rollout finished on 2026-10-07 (README, "Rollout"), and the deeper starter packs of 2026-10-11 (#13) reached every library the same day. This change takes the template's `ai-review` and `workflow` packs into every library and updates `agents` and `claude` from the template, so the plan opens one sync pull request in each library: the 18 new files of the two packs, and 8 files of `agents` and `claude` updated. What differs otherwise, differs on purpose, as before:

- every library filled in `.agents/project.md`, which is therefore its own (`local`), so the template's new lines in the profile skeleton reach none of them;
- mattermind keeps its own `.github/workflows/docs.yml`, since its docs dependencies are an extra, and pg-partsmith its own `.github/dependabot.yml`, which adds the `docker` ecosystem. Their `.engineering-assets.yml` lists those files under `ignore`.

Once the 13 sync pull requests are merged, the expectation goes back to "nothing changes anywhere": the outcomes `unchanged` with no counts, and the states below `current`.

The expectation holds while:

- only mattermind and pg-partsmith have an `.engineering-assets.yml`, and it only ignores those files. `targets.yml` subscribes every target (`defaults.opt_in: assumed`), so `--assume-opt-in` changes nothing;
- the organisation's repositories with the topic `python`, minus the `exclude` patterns of `targets.yml`, are these 13. A new one shows up as an unexpected target;
- touchmark has no open sync pull request in any target, before the merge of this change;
- the packs and the libraries' copies stay as they are. A change to a pack makes the copies `outdated` and the plan `opened`; a library that changes a copy makes it `local`. Either way, write the expectation again.

The default branches it was checked at, on 2026-11-15:

| Repository | Commit |
|---|---|
| aiokafka-foundation-kit | `62d5e126485fe9f7a5eccc26aa66fe8d0ffa7f48` |
| alembic-gauntlet | `de2170d0609228deb11f2e056e1cbb35a11f1119` |
| clientwright | `8d5835e59545614bca7849ce1b68426e52e12c61` |
| deadline-budget | `158de0215a25192a9f6e070bb812cc1bb4e7635d` |
| grpc-client-kit | `6b333b9551c6db622cfd839ca21acde4d241f19f` |
| grpc-server-kit | `f9f9c609867f42cef528f14864b0b55657a7876e` |
| idempotency-kit | `1bf9a264acd21d96cd2284b7683bf458c012a41a` |
| mattermind | `771c92abb025dfb623163cc2918209d64d735a7f` |
| omni-box | `6b0f9728a5697ce8e8b07091c7e8ef8b2e90fef8` |
| pg-partsmith | `eb29d57456f1fe74a68dd9a26e663a4d1b20c7e5` |
| redis-client-kit | `ccf50c262492a50a44ff6a4e93c7ee4a879d5994` |
| servicewright | `805c4d090b61b1d2ed995f3d6d423a979d2cdf82` |
| sqlalchemy-foundation-kit | `ce9b15cbde116facfb9e9435009c04f06a0413b7` |

## Expectation

Packs of every target: `zensical-docs, bedrock-community, agents, claude, python-library, ai-review, workflow`

That is `defaults.packs` of `targets.yml`, with `agents` placed before the packs that require it. `ai-review` and `workflow` both ship `local/.gitignore`, with the same content; `workflow`, the later, is its pack. No target adds packs: the two opt-in files only ignore paths.

| Repository | Outcome | Create | Update | Delete |
|---|---|---:|---:|---:|
| `bedrock-python/aiokafka-foundation-kit` | opened | 18 | 8 | 0 |
| `bedrock-python/alembic-gauntlet` | opened | 18 | 8 | 0 |
| `bedrock-python/clientwright` | opened | 18 | 8 | 0 |
| `bedrock-python/deadline-budget` | opened | 18 | 8 | 0 |
| `bedrock-python/grpc-client-kit` | opened | 18 | 8 | 0 |
| `bedrock-python/grpc-server-kit` | opened | 18 | 8 | 0 |
| `bedrock-python/idempotency-kit` | opened | 18 | 8 | 0 |
| `bedrock-python/mattermind` | opened | 18 | 8 | 0 |
| `bedrock-python/omni-box` | opened | 18 | 8 | 0 |
| `bedrock-python/pg-partsmith` | opened | 18 | 8 | 0 |
| `bedrock-python/redis-client-kit` | opened | 18 | 8 | 0 |
| `bedrock-python/servicewright` | opened | 18 | 8 | 0 |
| `bedrock-python/sqlalchemy-foundation-kit` | opened | 18 | 8 | 0 |

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
| `AGENTS.md` | agents | outdated | - | no |
| `.claude/agents/reviewer.md` | claude | outdated | - | yes |
| `.claude/settings.json` | claude | current | - | yes |
| `.claude/skills/commit/SKILL.md` | claude | outdated | - | yes |
| `.claude/skills/new-branch/SKILL.md` | claude | outdated | - | yes |
| `.claude/skills/pr/SKILL.md` | claude | outdated | - | yes |
| `.claude/skills/review-change/SKILL.md` | claude | outdated | - | yes |
| `.claude/skills/spec/SKILL.md` | claude | outdated | - | yes |
| `CLAUDE.md` | claude | outdated | - | no |
| `.agents/guidelines/public-api.md` | python-library | current | - | no |
| `.agents/guidelines/python.md` | python-library | current | - | no |
| `.agents/guidelines/testing.md` | python-library | current | - | no |
| `.agents/review/README.md` | ai-review | missing | - | no |
| `.agents/review/check.py` | ai-review | missing | - | yes |
| `.agents/review/directions/compatibility.md` | ai-review | missing | - | no |
| `.agents/review/directions/correctness.md` | ai-review | missing | - | no |
| `.agents/review/directions/design.md` | ai-review | missing | - | no |
| `.agents/review/directions/performance.md` | ai-review | missing | - | no |
| `.agents/review/directions/security.md` | ai-review | missing | - | no |
| `.agents/review/directions/tests.md` | ai-review | missing | - | no |
| `.agents/review/pure-refactor.md` | ai-review | missing | - | no |
| `.agents/review/review.md` | ai-review | missing | - | no |
| `.agents/skills/review-change/SKILL.md` | ai-review | missing | - | yes |
| `.agents/skills/commit/SKILL.md` | workflow | missing | - | yes |
| `.agents/skills/implement/SKILL.md` | workflow | missing | - | yes |
| `.agents/skills/new-branch/SKILL.md` | workflow | missing | - | yes |
| `.agents/skills/pr/SKILL.md` | workflow | missing | - | yes |
| `.agents/skills/spec/SKILL.md` | workflow | missing | - | yes |
| `.claude/skills/implement/SKILL.md` | workflow | missing | - | yes |
| `local/.gitignore` | workflow | missing | - | no |

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
