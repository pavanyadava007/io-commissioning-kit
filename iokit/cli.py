"""Command line entry point: iokit lint | docs | loopcheck | cetest | campaign | serve."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from time import perf_counter

import yaml

from . import cetest, docs, iolist, records
from .lint import lint
from .loopcheck import TOL_PCT, loopcheck
from .rack import Fault, FieldRack

DEFAULT_IO = "config/io_list.yaml"


def load_faults(path: str | None) -> tuple[list[Fault], int]:
    if not path:
        return [], 0
    d = yaml.safe_load(Path(path).read_text())
    faults = [Fault(f["kind"], f["tag"], f.get("partner"), f.get("params", {}))
              for f in d.get("faults", [])]
    return faults, int(d.get("seed", 0))


def cmd_lint(a) -> int:
    findings = lint(iolist.load_raw(a.io))
    for f in findings:
        print(f)
    errors = sum(f.severity == "error" for f in findings)
    print(f"{a.io}: {errors} error(s), {len(findings) - errors} warning(s)")
    return 1 if errors else 0


def cmd_docs(a) -> int:
    for path in docs.generate_all(iolist.load(a.io), a.out, TOL_PCT):
        print(f"wrote {path}")
    return 0


def cmd_loopcheck(a) -> int:
    iol = iolist.load(a.io)
    faults, seed = load_faults(a.faults)
    t0 = perf_counter()
    results = asyncio.run(loopcheck(iol, FieldRack(iol, faults, seed), a.mode))
    rec = records.build_record(iol, results, a.mode, seed, faults, perf_counter() - t0)
    items = records.issues(iol, results)
    records.write_run(a.out, rec, items)
    s = rec["summary"]
    print(f"SIMULATED loop check ({a.mode}): {s['passed']}/{s['points']} passed, "
          f"{s['failed']} issue(s) -> {a.out}")
    for r in results:
        if not r.passed:
            print(f"  FAIL {r.tag:11} {r.channel:9} {r.cause_text}")
    return 0


def cmd_cetest(a) -> int:
    spec = cetest.load_spec(a.spec)
    rec = cetest.run_cetest(spec)
    cetest.write(rec, spec, a.out)
    s = rec["summary"]
    print(f"C&E test: {s['causes']} causes x {s['effects']} effects, {s['checks']} checks, "
          f"{s['passed']} passed, {s['failed']} failed -> {a.out}")
    return 1 if s["failed"] else 0


def cmd_campaign(a) -> int:
    from .campaign import run_campaign

    iol = iolist.load(a.io)
    res = asyncio.run(run_campaign(iol, a.n, a.seed, a.max_faults, log=print))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n")
    o = res["overall"]
    print(f"{o['n']} faults: kit detected {o['kit_detected_pct']} %, classified "
          f"{o['kit_classified_pct']} %; naive detected {o['naive_detected_pct']} % -> {a.out}")
    return 0


def cmd_serve(a) -> int:
    from .opcua import RackServer

    iol = iolist.load(a.io)
    faults, seed = load_faults(a.faults)

    async def main():
        async with RackServer(iol, FieldRack(iol, faults, seed), a.port) as srv:
            print(f"SIMULATED rack on {srv.url} (Ctrl+C to stop)")
            while True:
                await srv.scan()
                await asyncio.sleep(0.1)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="iokit", description=__doc__)
    ap.add_argument("--io", default=DEFAULT_IO, help="I/O list YAML")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("lint", help="validate the I/O list").set_defaults(fn=cmd_lint)
    p = sub.add_parser("docs", help="generate cable schedule, interfaces, procedure")
    p.add_argument("--out", default="docs/generated")
    p.set_defaults(fn=cmd_docs)
    p = sub.add_parser("loopcheck", help="run the loop check against the simulated rack")
    p.add_argument("--faults", help="YAML with wiring faults to plant in the simulation")
    p.add_argument("--mode", choices=("kit", "naive"), default="kit")
    p.add_argument("--out", default="results/run")
    p.set_defaults(fn=cmd_loopcheck)
    p = sub.add_parser("cetest", help="test interlock logic against the C&E matrix")
    p.add_argument("--spec", default="config/cause_effect.yaml")
    p.add_argument("--out", default="results/cetest")
    p.set_defaults(fn=cmd_cetest)
    p = sub.add_parser("campaign", help="seeded fault-injection campaign")
    p.add_argument("--n", type=int, default=200)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--max-faults", type=int, default=3)
    p.add_argument("--out", default="results/campaign.json")
    p.set_defaults(fn=cmd_campaign)
    p = sub.add_parser("serve", help="run the simulated OPC UA rack for manual browsing")
    p.add_argument("--faults")
    p.add_argument("--port", type=int, default=4840)
    p.set_defaults(fn=cmd_serve)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
