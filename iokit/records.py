"""Commissioning record and issue log writers (JSON + Markdown)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .iolist import IOList
from .loopcheck import TOL_PCT, PointResult, results_to_dicts
from .rack import Fault

SIM_NOTE = ("SIMULATED RUN - simulated instrumentation rack and simulated wiring faults. "
            "No real hardware or plant data.")
ACTIONS = {
    "swap": "Check core termination at the junction box and cabinet terminals for both "
            "loops; correct the crossed cores, then repeat the loop check for both points.",
    "open": "Check continuity of field cable and trunk cores, terminal screws and fuses.",
    "scaling": "Compare transmitter range / sensor type with the controller channel "
               "configuration and correct one of them (update the I/O list if the device changed).",
    "noise": "Check shield termination (one end), cable routing near power cables and grounding.",
    "stuck": "Check whether the channel or device is frozen (forced value, failed card, shorted "
             "contact).",
    "inverted": "Check whether the device contact is NO or NC against the I/O list and rewire "
                "or change the configured logic.",
    "polarity": "Check output wiring and the configured output logic (normally energised vs "
                "normally de-energised).",
    "unknown": "Repeat the check and investigate manually.",
    "fail": "Run the full loop check on this point to find the cause.",
}


def build_record(iol: IOList, results: list[PointResult], mode: str, seed: int,
                 faults: list[Fault], wall_s: float) -> dict:
    failed = [r for r in results if not r.passed]
    return {
        "title": "Loop-check commissioning record",
        "note": SIM_NOTE,
        "rack": iol.meta.get("title", ""),
        "io_list_revision": iol.meta.get("revision", ""),
        "io_list_sha256": iol.sha256,
        "mode": mode,
        "seed": seed,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tester": "simulated run",
        "tolerance_pct_of_span": TOL_PCT,
        "wall_time_s": round(wall_s, 2),
        "summary": {"points": len(results), "passed": len(results) - len(failed),
                    "failed": len(failed)},
        "sign_off": {"tested_by": "", "witnessed_by": "", "date": ""},
        "results": results_to_dicts(results),
        "injected_faults_simulation_only": [f.describe() for f in faults],
    }


def issues(iol: IOList, results: list[PointResult]) -> list[dict]:
    pts = iol.by_tag()
    out = []
    for n, r in enumerate((r for r in results if not r.passed), start=1):
        d = pts[r.tag].data
        out.append({
            "id": f"ISSUE-{n:03d}",
            "title": f"{r.tag} ({r.channel}) - {r.cause_text}",
            "labels": ["commissioning", "wiring" if r.cause != "scaling" else "configuration",
                       d["subsystem"]],
            "suspected_cause": r.cause,
            "evidence": r.evidence,
            "location": (f"cable {d['field']['cable']} via {d['junction_box']['id']} "
                         f"{' '.join(d['junction_box']['terminals'])}, trunk {d['trunk']['cable']} "
                         f"cores {'/'.join(str(c) for c in d['trunk']['cores'])}, cabinet "
                         f"{' '.join(d['cabinet_terminals'])}"),
            "action": ACTIONS[r.cause],
            "status": "open",
        })
    return out


def _yn(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def record_md(rec: dict) -> str:
    s = rec["summary"]
    out = [f"# {rec['title']}", "", f"**{rec['note']}**", "",
           f"- Rack: {rec['rack']}", f"- I/O list revision {rec['io_list_revision']}, "
           f"sha256 `{rec['io_list_sha256']}`", f"- Mode: {rec['mode']}, seed {rec['seed']}",
           f"- Timestamp (UTC): {rec['timestamp_utc']}", f"- Tester: {rec['tester']}",
           f"- Tolerance: +/- {rec['tolerance_pct_of_span']} % of span",
           f"- Result: {s['passed']}/{s['points']} passed, {s['failed']} failed "
           f"(wall time {rec['wall_time_s']} s)", "",
           "| Tag | Channel | Signal | As found | Max error % | Result | Suspected cause |",
           "|---|---|---|---|---|---|---|"]
    for r in rec["results"]:
        if r["signal"] in ("DI", "DO"):
            found = " / ".join(f"{st['action']}: {'T' if st['found'] else 'F'}" for st in r["steps"])
        else:
            found = " / ".join(f"{st['pct']}%: {st['found']:.4g}" for st in r["steps"])
        err = "-" if r["max_err_pct"] is None else f"{r['max_err_pct']:.2f}"
        out.append(f"| {r['tag']} | {r['channel']} | {r['signal']} | {found} | {err} | "
                   f"{_yn(r['passed'])} | {r['cause_text']} |")
    out += ["", "## Sign-off", "", "| Tested by | Witnessed by | Date |", "|---|---|---|",
            "|  |  |  |", ""]
    if rec["injected_faults_simulation_only"]:
        out += ["## Injected faults (simulation only, hidden from the checker)", ""]
        out += [f"- {f}" for f in rec["injected_faults_simulation_only"]] + [""]
    return "\n".join(out)


def issues_md(items: list[dict]) -> str:
    out = ["# Issue log", "", f"**{SIM_NOTE}**", "",
           f"{len(items)} open issue(s). Each entry can be pasted into an issue tracker.", ""]
    for i in items:
        out += [f"## {i['id']}: {i['title']}", "",
                f"- Labels: {', '.join(i['labels'])}",
                f"- Suspected cause: {i['suspected_cause']}",
                f"- Evidence: {i['evidence']}",
                f"- Location: {i['location']}",
                f"- Suggested action: {i['action']}",
                f"- Status: {i['status']}", ""]
    return "\n".join(out)


def write_run(out_dir: str | Path, rec: dict, items: list[dict]) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "commissioning_record.json").write_text(json.dumps(rec, indent=2) + "\n")
    (out / "commissioning_record.md").write_text(record_md(rec))
    (out / "issue_log.json").write_text(json.dumps(items, indent=2) + "\n")
    (out / "issue_log.md").write_text(issues_md(items))
