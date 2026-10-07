#!/usr/bin/env python3
"""Compare touchmark reports of this hub with expected.md.

    check_plan.py [--expected FILE] [--plan PLAN.json] [--status DIR]

--plan takes the JSON report of `touchmark plan --assume-opt-in --all
--format json` and checks, per target, the outcome, the packs and the number
of files created, updated and deleted, and across targets the changed paths
with their counts and sensitive flags.

--status takes a directory of `touchmark status --format json` reports, one
per target, named <repository name>.json, and checks the state of every file.

expected.md holds the expectation in two tables (its "Format" section says
how). Both checks derive what they compare from the same file table: a file
in state missing is created, one in state outdated is updated, one in state
retired is deleted, and any other state changes nothing.

Exit codes: 0 everything matches, 1 a difference, 2 a usage error or an input
that cannot be read. Standard library only; Python 3.9 or newer.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROVIDER = "gh"
COUNTS = ("create", "update", "delete")
# The change a file in each state makes: (key of report "changes", action of report "paths").
CHANGES = {"missing": ("create", "add"), "outdated": ("update", "update"), "retired": ("delete", "delete")}
STATES = {"missing", "current", "outdated", "local", "ignored", "retired", "retired-local", "unsafe", "orphaned"}
OUTCOMES_HEADER = ["Repository", "Outcome", "Create", "Update", "Delete"]
FILES_HEADER = ["Path", "Pack", "State", "Exceptions", "Sensitive"]
NONE = ("", "-", "—")


class InputError(Exception):
    """An input that cannot be read or parsed (exit 2)."""


def cells(line: str) -> list[str] | None:
    """Split a Markdown table row into its stripped cells; None for any other line."""
    line = line.strip()
    if not (line.startswith("|") and line.endswith("|")):
        return None
    return [c.strip() for c in line[1:-1].split("|")]


def unquote(text: str) -> str:
    """Remove one pair of backticks around a cell."""
    if len(text) >= 2 and text[0] == "`" and text[-1] == "`":
        return text[1:-1]
    return text


def table(lines: list[str], header: list[str], name: str) -> list[tuple[int, list[str]]]:
    """Return the numbered rows of the one table whose header row is header."""
    rows: list[tuple[int, list[str]]] = []
    found, inside = 0, False
    for n, line in enumerate(lines, 1):
        row = cells(line)
        if row is None:
            inside = False
        elif row == header:
            found += 1
            inside = True
        elif inside and not all(set(c) <= set("-: ") for c in row):
            if len(row) != len(header):
                raise InputError(f"expected.md:{n}: the {name} table needs {len(header)} cells, got {len(row)}")
            rows.append((n, row))
    if found != 1:
        raise InputError(f"expected.md: want one {name} table with the header | {' | '.join(header)} |, found {found}")
    return rows


def count(text: str, where: str) -> int:
    if not re.fullmatch(r"[0-9]+", text):
        raise InputError(f"{where}: {text!r} is not a count")
    return int(text)


def parse_expected(path: Path) -> tuple[list[str], dict, dict]:
    """Read expected.md into the packs, the outcomes by repository and the files by path."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as e:
        raise InputError(f"{path}: {e}") from e
    packs = None
    for line in lines:
        m = re.match(r"^Packs of every target: `([^`]*)`", line)
        if m:
            packs = [p.strip() for p in m.group(1).split(",") if p.strip()]
    if not packs:
        raise InputError("expected.md: no line 'Packs of every target: `a, b`'")
    outcomes: dict[str, dict] = {}
    for n, row in table(lines, OUTCOMES_HEADER, "outcomes"):
        repo, where = unquote(row[0]), f"expected.md:{n}"
        if repo in outcomes:
            raise InputError(f"{where}: {repo} twice")
        outcomes[repo] = {"outcome": row[1]} | {k: count(v, where) for k, v in zip(COUNTS, row[2:])}
    names = {repo.rsplit("/", 1)[-1]: repo for repo in outcomes}
    files: dict[str, dict] = {}
    for n, row in table(lines, FILES_HEADER, "files"):
        where = f"expected.md:{n}"
        fpath, pack, state, exceptions, sensitive = unquote(row[0]), row[1], row[2], row[3], row[4]
        if fpath in files:
            raise InputError(f"{where}: {fpath} twice")
        if state not in STATES:
            raise InputError(f"{where}: unknown state {state!r}")
        per = dict.fromkeys(outcomes, state)
        if exceptions not in NONE:
            for part in exceptions.split(";"):
                st, _, who = (s.strip() for s in part.partition(":"))
                if st not in STATES or not who:
                    raise InputError(f"{where}: exceptions read 'state: repo, repo; state: repo', got {part!r}")
                for name in (w.strip() for w in who.split(",")):
                    if name not in names:
                        raise InputError(f"{where}: {name!r} is not a repository of the outcomes table")
                    per[names[name]] = st
        if sensitive not in ("yes", "no"):
            raise InputError(f"{where}: Sensitive is yes or no, got {sensitive!r}")
        files[fpath] = {"pack": pack, "states": per, "sensitive": sensitive == "yes"}
    return packs, outcomes, files


def derived(files: dict, repo: str) -> dict[str, int]:
    """The files repo creates, updates and deletes according to the file table."""
    out = dict.fromkeys(COUNTS, 0)
    for f in files.values():
        if f["states"][repo] in CHANGES:
            out[CHANGES[f["states"][repo]][0]] += 1
    return out


def consistency(outcomes: dict, files: dict) -> list[str]:
    """Contradictions between the outcomes table and the file table."""
    diffs = []
    for repo, want in sorted(outcomes.items()):
        got = derived(files, repo)
        diffs.extend(
            f"expected.md: {repo}: the outcomes table says {k} {want[k]}, the file table gives {got[k]}"
            for k in COUNTS
            if got[k] != want[k]
        )
        changes = sum(got.values())
        if want["outcome"] != ("opened" if changes else "unchanged"):
            diffs.append(f"expected.md: {repo}: outcome {want['outcome']} with {changes} changes")
    return diffs


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise InputError(f"{path}: {e}") from e


def check_plan(report: dict, packs: list[str], outcomes: dict, files: dict) -> list[str]:
    """Differences between a plan report and the expectation."""
    if report.get("schema") != "report/v1" or report.get("command") != "plan":
        raise InputError("the plan report is not a report/v1 of touchmark plan")
    diffs = []
    if not report.get("assume_opt_in"):
        diffs.append("plan: run without --assume-opt-in")
    mode = (report.get("scope") or {}).get("mode", "all")
    if mode != "all":
        diffs.append(f"plan: scope {mode}, want all (--all)")
    for p in report.get("providers", []):
        if p.get("error"):
            diffs.append(f"plan: provider {p.get('id')} unavailable: {p['error']}")
        if not p.get("resolve_complete"):
            diffs.append(f"plan: provider {p.get('id')} did not resolve every target")
        diffs.extend(f"plan: provider {p.get('id')} does not know {m}" for m in p.get("missing") or [])
    seen = set()
    for t in report.get("targets", []):
        repo = t.get("path")
        ref = f"{t.get('provider')}:{repo or '(unnamed)'}"
        if t.get("provider") != PROVIDER or repo not in outcomes:
            diffs.append(f"plan: unexpected target {ref} ({t.get('outcome')})")
            continue
        seen.add(repo)
        want = outcomes[repo]
        if t.get("outcome") != want["outcome"] or t.get("reason"):
            reason = f":{t['reason']}" if t.get("reason") else ""
            notes = "; ".join(t.get("warnings") or [])
            diffs.append(
                f"plan: {ref}: {t.get('outcome')}{reason}, want {want['outcome']}" + (f" ({notes})" if notes else "")
            )
            continue
        if not t.get("opt_in_assumed"):
            diffs.append(f"plan: {ref} has an opt-in file of its own: expected.md assumes none")
        if t.get("packs") != packs:
            diffs.append(f"plan: {ref}: packs {', '.join(t.get('packs') or [])}, want {', '.join(packs)}")
        changes = t.get("changes") or {}
        diffs.extend(
            f"plan: {ref}: {k} {changes.get(k, 0)}, want {want[k]}" for k in COUNTS if changes.get(k, 0) != want[k]
        )
        if changes.get("chmod", 0):
            diffs.append(f"plan: {ref}: chmod {changes['chmod']}, want 0")
    diffs.extend(f"plan: {PROVIDER}:{repo} is not in the report" for repo in sorted(set(outcomes) - seen))
    # The changed paths across targets: compared only when every target was
    # decided as expected, since a target that differs shifts the counts.
    if diffs:
        return diffs
    want_paths: dict[tuple[str, str], tuple[int, bool]] = {}
    for fpath, f in files.items():
        for st in f["states"].values():
            if st in CHANGES:
                key = (CHANGES[st][1], fpath)
                want_paths[key] = (want_paths.get(key, (0, False))[0] + 1, f["sensitive"])
    got_paths = {(p["action"], p["path"]): (p["targets"], bool(p.get("sensitive"))) for p in report.get("paths") or []}
    for key in sorted(set(want_paths) | set(got_paths)):
        want, got = want_paths.get(key), got_paths.get(key)
        what = " ".join(key)
        if want == got:
            continue
        if got is None:
            diffs.append(f"plan: paths: no {what}, want it in {want[0]} targets")
        elif want is None:
            diffs.append(f"plan: paths: unexpected {what} in {got[0]} targets")
        else:
            flag = (" (sensitive)" * got[1], " (sensitive)" * want[1])
            diffs.append(f"plan: paths: {what} in {got[0]} targets{flag[0]}, want {want[0]}{flag[1]}")
    return diffs


def check_status(directory: Path, packs: list[str], outcomes: dict, files: dict) -> list[str]:
    """Differences between status reports and the expected file states."""
    diffs = []
    for repo in sorted(outcomes):
        path = directory / (repo.rsplit("/", 1)[-1] + ".json")
        if not path.exists():
            diffs.append(f"status: {repo}: no report {path}")
            continue
        rep = load_json(path)
        got_packs = (rep.get("selection") or {}).get("packs")
        if got_packs != packs:
            diffs.append(f"status: {repo}: packs {', '.join(got_packs or [])}, want {', '.join(packs)}")
        got = {e["path"]: e["state"] for e in rep.get("entries") or []}
        for fpath in sorted(set(files) | set(got)):
            want = files[fpath]["states"][repo] if fpath in files else None
            if got.get(fpath) != want:
                diffs.append(
                    f"status: {repo}: {fpath} is {got.get(fpath) or 'not reported'}, want {want or 'not reported'}"
                )
    return diffs


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--expected", type=Path, default=Path(__file__).resolve().parent.parent / "expected.md")
    ap.add_argument("--plan", type=Path, help="JSON report of touchmark plan --assume-opt-in --all --format json")
    ap.add_argument("--status", type=Path, help="directory of touchmark status --format json reports, <name>.json each")
    args = ap.parse_args(argv)
    if not args.plan and not args.status:
        ap.error("give --plan, --status or both")
    try:
        packs, outcomes, files = parse_expected(args.expected)
        # A file table that contradicts the outcomes table is a mistake in
        # expected.md: nothing else is compared until it is fixed.
        diffs = consistency(outcomes, files)
        if not diffs:
            if args.plan:
                report = load_json(args.plan)
                diffs += check_plan(report, packs, outcomes, files)
                # The run's own warnings, for context: an unknown writer
                # before the App exists, an unchecked hub head outside CI.
                for w in report.get("warnings") or []:
                    print(f"note: plan warns: {w}")
            if args.status:
                diffs += check_status(args.status, packs, outcomes, files)
    except InputError as e:
        print(f"check_plan: {e}", file=sys.stderr)
        return 2
    checked = " and ".join(name for name, on in (("plan", args.plan), ("status", args.status)) if on)
    for d in diffs:
        print(d)
    if diffs:
        print(f"{len(diffs)} difference(s) from expected.md ({checked})")
        return 1
    print(f"{checked} match expected.md: {len(outcomes)} targets, {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
