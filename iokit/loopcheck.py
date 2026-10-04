"""Loop-check runner: inject at the field side, read back over OPC UA, classify faults."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from statistics import mean

from .iolist import IOList, Point
from .opcua import RackClient, RackServer
from .rack import OPEN_RAW, FieldRack

STEPS = (0.0, 0.25, 0.5, 0.75, 1.0)
TOL_PCT = 0.5   # analog tolerance, % of span
SAMPLES = 3     # readings per analog step (kit mode)

CAUSE_TEXT = {
    "swap": "swapped with {partner_channel} ({partner})",
    "open": "open circuit",
    "scaling": "scaling mismatch between field device and controller channel",
    "noise": "noisy signal (unstable reading)",
    "stuck": "stuck / frozen value",
    "inverted": "inverted contact (NO wired as NC or vice versa)",
    "polarity": "output polarity reversed",
    "unknown": "out of tolerance, cause not classified",
    "fail": "failed single-point check (naive mode does not classify)",
}


@dataclass
class PointResult:
    tag: str
    channel: str
    signal: str
    passed: bool
    cause: str | None = None
    partner: str | None = None
    partner_channel: str | None = None
    evidence: str = ""
    max_err_pct: float | None = None
    steps: list[dict] = field(default_factory=list)

    @property
    def cause_text(self) -> str:
        if self.passed:
            return "-"
        return CAUSE_TEXT[self.cause].format(partner=self.partner, partner_channel=self.partner_channel)


class Bench:
    """Server + client + field rack, i.e. everything a commissioning engineer touches."""

    def __init__(self, iol: IOList, server: RackServer, client: RackClient):
        self.iol, self.server, self.client = iol, server, client
        self.points = iol.by_tag()

    @property
    def rack(self) -> FieldRack:
        return self.server.rack

    async def read(self) -> dict[str, tuple]:
        await self.server.scan()
        return await self.client.read_inputs()


def _r(x: float) -> float:
    return float(f"{x:.6g}")


async def check_analog(b: Bench, p: Point) -> PointResult:
    s_lo, s_hi = p.signal_range
    span = s_hi - s_lo
    peers = [q for q in b.iol.of_type(p.signal) if q.tag != p.tag]
    matches = dict.fromkeys((q.tag for q in peers), 0)
    steps, spread = [], 0.0
    for f in STEPS:
        s = p.frac_to_signal(f)
        b.rack.inject(p.tag, s)
        reads = [await b.read() for _ in range(SAMPLES)]
        raws = [r[p.tag][0] for r in reads]
        raw, eng = mean(raws), mean(r[p.tag][1] for r in reads)
        spread = max(spread, (max(raws) - min(raws)) / span * 100)
        err = (p.eng_frac(eng) - f) * 100
        for q in peers:
            if abs(mean(r[q.tag][0] for r in reads) - s) / span * 100 <= TOL_PCT:
                matches[q.tag] += 1
        steps.append({"pct": int(f * 100), "inject": _r(s), "expected": _r(p.eng_at(f)),
                      "found": _r(eng), "raw": _r(raw), "status": reads[-1][p.tag][2],
                      "err_pct": _r(err), "signal_ok": abs(p.signal_to_frac(raw) - f) * 100 <= TOL_PCT,
                      "ok": abs(err) <= TOL_PCT})
    b.rack.release(p.tag)
    res = PointResult(p.tag, p.channel, p.signal, False, steps=steps,
                      max_err_pct=_r(max(abs(s["err_pct"]) for s in steps)))
    partners = [t for t, n in matches.items() if n >= len(STEPS) - 1]
    raws = [s["raw"] for s in steps]
    if all(s["ok"] for s in steps) and spread <= TOL_PCT:
        res.passed = True
    elif partners:
        res.cause, res.partner = "swap", partners[0]
        res.partner_channel = b.points[partners[0]].channel
        res.evidence = (f"injection at {p.tag} field terminals moved channel {res.partner_channel} "
                        f"({partners[0]}); {p.channel} stayed near {raws[0]:.4g} "
                        f"{_unit(p)}")
    elif spread > TOL_PCT:
        res.cause, res.evidence = "noise", f"reading spread up to {spread:.2f} % of span within one step"
    elif all(s["status"] != "OK" for s in steps) or all(r == OPEN_RAW[p.signal] for r in raws):
        res.cause = "open"
        res.evidence = f"raw {raws[0]:.4g} {_unit(p)}, status {steps[0]['status']} at every step"
    elif all(s["signal_ok"] for s in steps):
        res.cause = "scaling"
        res.evidence = (f"raw signal correct at every step, but 0 % reads {steps[0]['found']:.4g} and "
                        f"100 % reads {steps[-1]['found']:.4g} {p.units} (I/O list: "
                        f"{p.lo:.4g} .. {p.hi:.4g})")
    elif max(raws) - min(raws) <= TOL_PCT / 100 * span:
        res.cause, res.evidence = "stuck", f"raw frozen at {raws[0]:.4g} {_unit(p)} for all steps"
    else:
        res.cause, res.evidence = "unknown", f"max error {res.max_err_pct:.2f} % of span"
    return res


def _unit(p: Point) -> str:
    return {"AI_4_20mA": "mA", "AI_0_10V": "V", "AI_RTD": "ohm"}[p.signal]


async def check_di(b: Bench, p: Point) -> PointResult:
    peers = [q.tag for q in b.iol.of_type("DI") if q.tag != p.tag]
    got, tracking = {}, set(peers)
    for state in (True, False):
        b.rack.inject(p.tag, state)
        r = await b.read()
        got[state] = r[p.tag][0]
        tracking = {q for q in tracking if r[q][0] == state}
    b.rack.release(p.tag)
    steps = [{"action": "close contact", "expected": True, "found": got[True]},
             {"action": "open contact", "expected": False, "found": got[False]}]
    return _classify_digital(b, p, got, sorted(tracking), steps, "inverted")


async def check_do(b: Bench, p: Point) -> PointResult:
    others = [q.tag for q in b.iol.of_type("DO") if q.tag != p.tag]
    got, tracking, steps = {}, set(others), []
    for cmd in (False, True, False):
        await b.client.write_command(p.tag, cmd)
        await b.server.scan()
        got[cmd] = b.rack.field_output(p.tag)
        tracking = {q for q in tracking if b.rack.field_output(q) == cmd}
        steps.append({"action": f"command {'TRUE' if cmd else 'FALSE'}", "expected": cmd,
                      "found": got[cmd]})
    return _classify_digital(b, p, got, sorted(tracking), steps, "polarity")


def _classify_digital(b, p, got, tracking, steps, inverse_cause) -> PointResult:
    res = PointResult(p.tag, p.channel, p.signal, False, steps=steps)
    if got[True] is True and got[False] is False:
        res.passed = True
    elif tracking:
        res.cause, res.partner = "swap", tracking[0]
        res.partner_channel = b.points[tracking[0]].channel
        res.evidence = f"toggling {p.tag} switched {res.partner} ({res.partner_channel}) instead"
    elif got[True] is False and got[False] is True:
        res.cause, res.evidence = inverse_cause, "state follows the stimulus inverted"
    else:
        res.cause = "stuck" if got[True] else "open"
        res.evidence = f"constant {'TRUE' if got[True] else 'FALSE'} in both states"
    return res


async def naive_point(b: Bench, p: Point) -> PointResult:
    """Baseline: one mid-scale reading per analog point, one state per digital point."""
    res = PointResult(p.tag, p.channel, p.signal, False)
    if p.is_analog:
        b.rack.inject(p.tag, p.frac_to_signal(0.5))
        r = await b.read()
        b.rack.release(p.tag)
        err = (p.eng_frac(r[p.tag][1]) - 0.5) * 100
        res.passed, res.max_err_pct = abs(err) <= TOL_PCT, _r(abs(err))
        res.steps = [{"pct": 50, "expected": _r(p.eng_at(0.5)), "found": _r(r[p.tag][1])}]
    elif p.signal == "DI":
        b.rack.inject(p.tag, True)
        r = await b.read()
        b.rack.release(p.tag)
        res.passed = r[p.tag][0] is True
    else:
        await b.client.write_command(p.tag, True)
        await b.server.scan()
        res.passed = b.rack.field_output(p.tag) is True
        await b.client.write_command(p.tag, False)
        await b.server.scan()
    if not res.passed:
        res.cause = "fail"
    return res


async def run_checks(b: Bench, mode: str = "kit") -> list[PointResult]:
    out = []
    for p in b.iol.points:
        if mode == "naive":
            out.append(await naive_point(b, p))
        elif p.is_analog:
            out.append(await check_analog(b, p))
        elif p.signal == "DI":
            out.append(await check_di(b, p))
        else:
            out.append(await check_do(b, p))
    return out


async def loopcheck(iol: IOList, rack: FieldRack, mode: str = "kit") -> list[PointResult]:
    async with RackServer(iol, rack) as srv, RackClient(srv.url, iol) as cli:
        return await run_checks(Bench(iol, srv, cli), mode)


def results_to_dicts(results: list[PointResult]) -> list[dict]:
    return [asdict(r) | {"cause_text": r.cause_text} for r in results]
