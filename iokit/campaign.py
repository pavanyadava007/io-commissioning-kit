"""Seeded fault-injection campaign: full loop check (kit) vs a naive single-point check."""

from __future__ import annotations

import platform
import random
import sys
from collections import defaultdict
from time import perf_counter

from .iolist import IOList
from .loopcheck import TOL_PCT, Bench, run_checks
from .opcua import RackClient, RackServer
from .rack import APPLIES_TO, FAULT_CLASSES, Fault, FieldRack, random_fault


def make_scenario(iol: IOList, rng: random.Random, max_faults: int) -> list[Fault]:
    faults, used = [], set()
    for _ in range(rng.randint(0, max_faults)):
        kind = rng.choice(FAULT_CLASSES)
        cands = [p for p in iol.points if p.signal in APPLIES_TO[kind] and p.tag not in used]
        if kind == "swap":
            cands = [p for p in cands
                     if any(q.signal == p.signal and q.tag not in used | {p.tag} for q in iol.points)]
        if not cands:
            continue
        p = rng.choice(cands)
        partner = None
        if kind == "swap":
            partner = rng.choice([q for q in iol.points
                                  if q.signal == p.signal and q.tag not in used | {p.tag}])
        f = random_fault(kind, p, rng, partner)
        used |= {f.tag, f.partner} - {None}
        faults.append(f)
    return faults


def variant(f: Fault) -> str:
    if f.kind == "scaling":
        return "scaling/rtd-curve" if "alpha" in f.params else f"scaling/{f.params['mode']}"
    return f.kind


def score(faults: list[Fault], results, n_points: int) -> dict:
    by_tag = {r.tag: r for r in results}
    flagged = {r.tag for r in results if not r.passed}
    faulty = set()
    per_fault = []
    for f in faults:
        tags = [t for t in (f.tag, f.partner) if t]
        faulty |= set(tags)
        ok = all(by_tag[t].cause == f.kind for t in tags)
        if f.kind == "swap":
            ok = ok and by_tag[f.tag].partner == f.partner and by_tag[f.partner].partner == f.tag
        per_fault.append({"fault": f.describe(), "class": f.kind, "variant": variant(f),
                          "detected": bool(flagged & set(tags)), "classified": ok})
    return {"faults": per_fault, "false_alarms": sorted(flagged - faulty),
            "healthy_points": n_points - len(faulty)}


async def run_campaign(iol: IOList, n: int = 200, seed: int = 1, max_faults: int = 3,
                       log=None) -> dict:
    rng = random.Random(seed)
    scenarios = [make_scenario(iol, rng, max_faults) for _ in range(n)]
    rows, wall = [], {"kit": 0.0, "naive": 0.0}
    t_all = perf_counter()
    async with RackServer(iol, FieldRack(iol)) as srv, RackClient(srv.url, iol) as cli:
        bench = Bench(iol, srv, cli)
        for i, faults in enumerate(scenarios):
            row = {"scenario": i, "faults": [f.describe() for f in faults]}
            for mode in ("kit", "naive"):
                srv.rack = FieldRack(iol, faults, seed=seed * 100_000 + i)
                t0 = perf_counter()
                results = await run_checks(bench, mode)
                wall[mode] += perf_counter() - t0
                row[mode] = score(faults, results, len(iol.points))
            rows.append(row)
            if log and (i + 1) % 25 == 0:
                log(f"  {i + 1}/{n} scenarios")
    return summarize(rows, wall, perf_counter() - t_all, n, seed, max_faults, len(iol.points))


def _pct(a: int, b: int) -> float | None:
    return round(100.0 * a / b, 1) if b else None


def summarize(rows, wall, total_s, n, seed, max_faults, n_points) -> dict:
    def table(key):
        agg = defaultdict(lambda: {"n": 0, "kit_detected": 0, "kit_classified": 0, "naive_detected": 0})
        for row in rows:
            for fk, fn in zip(row["kit"]["faults"], row["naive"]["faults"], strict=True):
                a = agg[fk[key]]
                a["n"] += 1
                a["kit_detected"] += fk["detected"]
                a["kit_classified"] += fk["classified"]
                a["naive_detected"] += fn["detected"]
        return {k: v | {"kit_detected_pct": _pct(v["kit_detected"], v["n"]),
                        "kit_classified_pct": _pct(v["kit_classified"], v["n"]),
                        "naive_detected_pct": _pct(v["naive_detected"], v["n"])}
                for k, v in sorted(agg.items())}

    per_class = table("class")
    tot = {k: sum(v[k] for v in per_class.values())
           for k in ("n", "kit_detected", "kit_classified", "naive_detected")}
    fa = {m: sum(len(r[m]["false_alarms"]) for r in rows) for m in ("kit", "naive")}
    healthy = sum(r["kit"]["healthy_points"] for r in rows)
    return {
        "note": "SIMULATED rack and simulated wiring faults. Numbers come from scripts/run_campaign.py.",
        "config": {"scenarios": n, "seed": seed, "max_faults_per_scenario": max_faults,
                   "io_points": n_points, "tolerance_pct_of_span": TOL_PCT,
                   "fault_classes": list(FAULT_CLASSES)},
        "environment": {"python": sys.version.split()[0], "platform": platform.platform(),
                        "processor": platform.processor() or platform.machine()},
        "overall": tot | {
            "kit_detected_pct": _pct(tot["kit_detected"], tot["n"]),
            "kit_classified_pct": _pct(tot["kit_classified"], tot["n"]),
            "naive_detected_pct": _pct(tot["naive_detected"], tot["n"]),
            "scenarios_without_faults": sum(1 for r in rows if not r["faults"]),
            "healthy_point_checks": healthy,
            "kit_false_alarms": fa["kit"], "naive_false_alarms": fa["naive"],
            "kit_false_alarm_pct": _pct(fa["kit"], healthy),
            "naive_false_alarm_pct": _pct(fa["naive"], healthy),
        },
        "per_class": per_class,
        "per_variant": table("variant"),
        "timing_s": {"total": round(total_s, 1), "kit": round(wall["kit"], 1),
                     "naive": round(wall["naive"], 1),
                     "kit_per_scenario": round(wall["kit"] / n, 3),
                     "naive_per_scenario": round(wall["naive"] / n, 3)},
        "scenarios": rows,
    }
