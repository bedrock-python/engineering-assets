#!/usr/bin/env bash
# Check in one command that `touchmark plan --assume-opt-in --all` on the
# 13 bedrock-python libraries matches expected.md.
#
#   TOUCHMARK_GH_READ_TOKEN=... scripts/plan-bedrock.sh [--status] [--keep]
#   scripts/plan-bedrock.sh --status-only
#
# plan reads the targets through the GitHub API, which needs a read
# credential: TOUCHMARK_GH_READ_TOKEN (a fine-grained token with the default
# "Public repositories" access is enough, since every target is public), or
# TOUCHMARK_GH_READ_APP_ID and TOUCHMARK_GH_READ_APP_KEY of the reader App.
# The script never reads, prints or stores the credential: touchmark takes
# it from the environment and masks it in its output.
#
# --status also clones every target anonymously over git (no API calls),
# runs `touchmark status --assume-opt-in` in each clone (a library without an
# .engineering-assets.yml counts as subscribed, as targets.yml makes it; one
# with the file is read as it is), and compares the state of every file: plan's
# report only counts the files it would change, status names the files it
# leaves (current, local). --status-only does only that and needs no token.
#
# Environment:
#   TOUCHMARK_BIN     a touchmark binary to use;
#   TOUCHMARK_SRC     else, a touchmark source tree to build it from
#                     (default: ../touchmark next to this hub, if present);
#                     else `touchmark` on PATH;
#   TOUCHMARK_HUB_FP  the hub's fingerprint, github.com/<repository id>
#                     (gh api repos/bedrock-python/engineering-assets --jq .id
#                     once the repository exists). Default github.com/9999999999,
#                     an id no repository has yet: plan then takes no pull
#                     request for its own, which is right while touchmark has
#                     opened none, as expected.md assumes anyway.
#
# Exit codes: 0 match, 1 a difference, 2 a usage or setup error.
set -euo pipefail

usage() { sed -n '2,/^set -euo/p' "$0" | sed '$d; s/^# \{0,1\}//'; }
die() { echo "plan-bedrock: $*" >&2; exit 2; }

run_plan=1 run_status=0 keep=0
for arg in "$@"; do
  case "$arg" in
    --status) run_status=1 ;;
    --status-only) run_status=1 run_plan=0 ;;
    --keep) keep=1 ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
done

hub=$(cd "$(dirname "$0")/.." && pwd)
work=$(mktemp -d "${TMPDIR:-/tmp}/plan-bedrock.XXXXXX")
if [ "$keep" = 1 ]; then
  echo "plan-bedrock: keeping $work"
else
  trap 'rm -rf "$work"' EXIT
fi

# A Python 3 that runs (on Windows, python3 may be a stub that does not).
py=
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(sys.version_info < (3, 9))' >/dev/null 2>&1; then
    py=$c
    break
  fi
done
[ -n "$py" ] || die "needs Python 3.9 or newer as python3 or python"

# touchmark: TOUCHMARK_BIN, else built from TOUCHMARK_SRC, else on PATH.
src=${TOUCHMARK_SRC:-$hub/../touchmark}
if [ -n "${TOUCHMARK_BIN:-}" ]; then
  tm=$TOUCHMARK_BIN
elif [ -f "$src/go.mod" ] && [ -d "$src/cmd/touchmark" ]; then
  command -v go >/dev/null 2>&1 || die "go is needed to build touchmark from $src (or set TOUCHMARK_BIN)"
  tm="$work/touchmark$(go env GOEXE)"
  echo "plan-bedrock: building touchmark from $src"
  (cd "$src" && go build -o "$tm" ./cmd/touchmark) || die "go build failed in $src"
elif command -v touchmark >/dev/null 2>&1; then
  tm=$(command -v touchmark)
else
  die "no touchmark: set TOUCHMARK_BIN or TOUCHMARK_SRC, or put touchmark on PATH"
fi
echo "plan-bedrock: $("$tm" version)"

if [ -n "$(git -C "$hub" status --porcelain)" ]; then
  echo "plan-bedrock: warning: the hub has uncommitted changes; touchmark reads its last commit" >&2
fi
"$tm" check --hub "$hub" >"$work/check.txt" 2>&1 || { cat "$work/check.txt" >&2; die "touchmark check failed"; }

args=()
if [ "$run_plan" = 1 ]; then
  # A read credential under the provider's names, or the short ones that a
  # hub with one provider also takes (the template's workflow uses those).
  have_read=
  for p in TOUCHMARK_GH_ TOUCHMARK_; do
    tok=${p}READ_TOKEN id=${p}READ_APP_ID key=${p}READ_APP_KEY
    if [ -n "${!tok:-}" ] || { [ -n "${!id:-}" ] && [ -n "${!key:-}" ]; }; then
      have_read=1
    fi
  done
  [ -n "$have_read" ] || die "set TOUCHMARK_GH_READ_TOKEN (or TOUCHMARK_GH_READ_APP_ID and TOUCHMARK_GH_READ_APP_KEY) for plan, or run with --status-only"
  # plan only reads; a write credential in this environment is a mistake.
  for name in $(compgen -e); do
    case "$name" in
      *WRITE_TOKEN|*WRITE_APP_ID|*WRITE_APP_KEY|*SIGNING_KEY) die "$name is set: plan needs only the read credential" ;;
    esac
  done
  fp=${TOUCHMARK_HUB_FP:-github.com/9999999999}
  echo "plan-bedrock: touchmark plan --assume-opt-in --all (hub fingerprint $fp)"
  set +e
  "$tm" plan --hub "$hub" --hub-fp "$fp" --assume-opt-in --all --format json >"$work/plan.json" 2>"$work/plan.err"
  code=$?
  set -e
  # 0: planned; 1: a target or provider failed, which the comparison
  # reports; 2: a configuration or usage error, with no report.
  if [ "$code" -ge 2 ]; then
    cat "$work/plan.err" >&2
    die "touchmark plan exited with $code"
  fi
  args+=(--plan "$work/plan.json")
fi

if [ "$run_status" = 1 ]; then
  mkdir -p "$work/status" "$work/clones"
  # The repositories of the outcomes table: rows that start with | `bedrock-python/...` |.
  # shellcheck disable=SC2016 # the backticks are Markdown, not a command
  repos=$(sed -n 's/^| `\(bedrock-python\/[A-Za-z0-9._-]*\)` |.*/\1/p' "$hub/expected.md")
  [ -n "$repos" ] || die "no repositories in expected.md"
  for repo in $repos; do
    name=${repo#*/}
    dir="$work/clones/$name"
    # core.autocrlf=false: the files are checked out as committed, whatever
    # the machine's settings. status judges an unchanged file by its
    # committed blob anyway, as plan does.
    git -c core.longpaths=true clone --quiet --depth 1 --config core.autocrlf=false \
      --config core.longpaths=true "https://github.com/$repo.git" "$dir" || die "cannot clone $repo"
    "$tm" status --hub "$hub" --dir "$dir" --repo "gh:$repo" --assume-opt-in --format json >"$work/status/$name.json" \
      || die "touchmark status failed for $repo"
  done
  args+=(--status "$work/status")
fi

"$py" "$hub/scripts/check_plan.py" --expected "$hub/expected.md" "${args[@]}"
