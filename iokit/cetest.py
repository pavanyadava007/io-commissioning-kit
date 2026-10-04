"""Cause-and-effect test: exercise every cause and check every effect against the matrix."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

from . import interlock
from .records import SIM_NOTE


def load_spec(path: str | Path) -> dict:
    return yaml.safe_load(Path(path).read_text())


def run_cetest(spec: dict, scan=interlock.scan) -> dict:
    effects = spec["effects"]
    reqs = dict.fromkeys(spec["requests"], True)
    checks: list[dict] = []

    def run(inputs, state, cause, step, tripped):
        out = scan(inputs, reqs, state)
        for eid, e in effects.items():
            expected = (not e["healthy"]) if eid in tripped else e["healthy"]
            checks.append({"cause": cause, "step": step, "effect": eid, "signal": e["name"],
                           "expected": expected, "found": out[e["name"]],
                           "ok": out[e["name"]] == expected})
        if step == "trip":
            checks.append({"cause": cause, "step": step, "effect": "alarm", "signal": "alarms",
                           "expected": "non-empty", "found": out["alarms"],
                           "ok": bool(out["alarms"])})

    run(dict(spec["healthy"]), interlock.State(), "-", "baseline", set())
    for cid, c in spec["causes"].items():
        state, trip = interlock.State(), set(c["effects"])
        run(dict(spec["healthy"]) | c["trip"], state, cid, "trip", trip)
        run(dict(spec["healthy"]), state, cid, "cleared, no reset (latched)", trip)
        run(dict(spec["healthy"]) | {"HS-604": True}, state, cid, "reset", set())
        if "boundary" in c:
            run(dict(spec["healthy"]) | c["boundary"], interlock.State(), cid, "boundary", set())
    cells = {(k["cause"], k["effect"]) for k in checks if k["step"] == "trip" and k["effect"] != "alarm"}
    covered = {k["effect"] for k in checks if k["step"] == "trip" and k["effect"] in effects
               and k["ok"] and k["expected"] != effects[k["effect"]]["healthy"]}
    failed = [k for k in checks if not k["ok"]]
    return {
        "title": "Cause-and-effect test record",
        "note": SIM_NOTE + " Logic test harness only, not a safety function.",
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tester": "simulated run",
        "summary": {"causes": len(spec["causes"]), "effects": len(effects),
                    "matrix_cells_checked": len(cells), "effects_covered": len(covered),
                    "checks": len(checks), "passed": len(checks) - len(failed),
                    "failed": len(failed)},
        "failed": failed,
        "checks": checks,
        "sign_off": {"tested_by": "", "witnessed_by": "", "date": ""},
    }


def record_md(rec: dict, spec: dict) -> str:
    s = rec["summary"]
    eids = list(spec["effects"])
    out = [f"# {rec['title']}", "", f"**{rec['note']}**", "",
           f"- Timestamp (UTC): {rec['timestamp_utc']}, tester: {rec['tester']}",
           f"- {s['causes']} causes x {s['effects']} effects = {s['matrix_cells_checked']} matrix "
           f"cells checked; {s['checks']} checks, {s['passed']} passed, {s['failed']} failed", "",
           "## Matrix (X = cause trips effect; result of the trip step)", "",
           "| Cause | Description | " + " | ".join(spec["effects"][e]["name"] for e in eids)
           + " | Result |", "|---|---|" + "---|" * (len(eids) + 1)]
    for cid, c in spec["causes"].items():
        mine = [k for k in rec["checks"] if k["cause"] == cid]
        ok = all(k["ok"] for k in mine)
        marks = ["X" if e in c["effects"] else "" for e in eids]
        out.append(f"| {cid} | {c['description']} | " + " | ".join(marks)
                   + f" | {'PASS' if ok else 'FAIL'} |")
    out += ["", "Steps per cause: trip, cause cleared without reset (trip must stay latched), "
            "reset, and a boundary value just inside the limit where given.", ""]
    if rec["failed"]:
        out += ["## Failed checks", ""] + [
            f"- {k['cause']} / {k['step']} / {k['signal']}: expected {k['expected']}, "
            f"found {k['found']}" for k in rec["failed"]] + [""]
    out += ["## Sign-off", "", "| Tested by | Witnessed by | Date |", "|---|---|---|",
            "|  |  |  |", ""]
    return "\n".join(out)


def write(rec: dict, spec: dict, out_dir: str | Path) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "ce_test_record.json").write_text(json.dumps(rec, indent=2) + "\n")
    (out / "ce_test_record.md").write_text(record_md(rec, spec))
