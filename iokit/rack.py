"""SIMULATED field wiring + controller input/output cards, with injectable wiring faults.

Field side: every point has a field device whose signal travels over its cable to a
controller channel. A loop calibrator can replace the device signal (`inject`). Faults change
how the signal reaches the channel. Nothing here talks to real hardware.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

from .iolist import RTD_ALPHA, RTD_R0, IOList, Point, frac_to_eng, rtd_temp

FAULT_CLASSES = ("swap", "open", "scaling", "inverted", "stuck", "polarity", "noise")
APPLIES_TO = {
    "swap": ("AI_4_20mA", "AI_0_10V", "AI_RTD", "DI", "DO"),
    "open": ("AI_4_20mA", "AI_0_10V", "AI_RTD", "DI", "DO"),
    "scaling": ("AI_4_20mA", "AI_0_10V", "AI_RTD"),
    "inverted": ("DI",),
    "stuck": ("AI_4_20mA", "AI_0_10V", "AI_RTD", "DI", "DO"),
    "polarity": ("DO",),
    "noise": ("AI_4_20mA", "AI_0_10V", "AI_RTD"),
}
OPEN_RAW = {"AI_4_20mA": 0.0, "AI_0_10V": 0.0, "AI_RTD": 10000.0}
BASE_NOISE = 0.0005  # healthy channel noise, fraction of signal span (1 sigma)
FAULT_NOISE = 0.01   # noise fault, fraction of signal span (1 sigma)


@dataclass(frozen=True)
class Fault:
    kind: str
    tag: str
    partner: str | None = None
    params: dict = field(default_factory=dict)

    def describe(self) -> str:
        return f"{self.kind} {self.tag}" + (f"<->{self.partner}" if self.partner else "")


@dataclass
class ChannelConfig:
    """Controller-side scaling for one analog channel."""

    lo: float = 0.0
    hi: float = 1.0
    scaling: str = "linear"
    r0: float = RTD_R0
    alpha: float = RTD_ALPHA


class FieldRack:
    def __init__(self, iol: IOList, faults: tuple[Fault, ...] | list[Fault] = (), seed: int = 0):
        self.points: dict[str, Point] = iol.by_tag()
        self.rng = random.Random(seed)
        self.stimulus: dict[str, object] = {}
        self.commands = {t: False for t, p in self.points.items() if p.signal == "DO"}
        self.config = {t: ChannelConfig(p.lo, p.hi, p.scaling)
                       for t, p in self.points.items() if p.is_analog}
        self.route = {t: t for t in self.points}  # field device tag -> channel (point tag)
        self.faults = list(faults)
        self.by_point: dict[str, Fault] = {}
        for f in self.faults:
            self._apply(f)
        self.source = {ch: dev for dev, ch in self.route.items()}  # channel -> field device

    def _apply(self, f: Fault) -> None:
        for t in (f.tag, f.partner):
            if t is not None:
                if t in self.by_point:
                    raise ValueError(f"point {t} already has a fault")
                self.by_point[t] = f
        if f.kind == "swap":
            self.route[f.tag], self.route[f.partner] = f.partner, f.tag
        elif f.kind == "scaling":
            cfg = self.config[f.tag]
            if "alpha" in f.params:
                cfg.alpha = f.params["alpha"]
            else:
                cfg.lo, cfg.hi = f.params["lo"], f.params["hi"]

    # ---- field side -------------------------------------------------------------------
    def inject(self, tag: str, value) -> None:
        self.stimulus[tag] = value

    def release(self, tag: str) -> None:
        self.stimulus.pop(tag, None)

    def field_signal(self, device: str):
        return self.stimulus.get(device, self.points[device].rest_value)

    def field_output(self, device: str) -> bool:
        """What a multimeter at the field device of a DO reads (energised or not)."""
        f = self.by_point.get(device)
        if f is not None and f.kind == "open":
            return False
        if f is not None and f.kind == "stuck":
            return True
        state = self.commands[self.route[device]]
        return (not state) if (f is not None and f.kind == "polarity") else state

    # ---- controller side --------------------------------------------------------------
    def read_channel(self, ch: str) -> tuple[object, object, str]:
        """Return (raw, engineering value, status) as the input card reports them."""
        p = self.points[ch]
        f = self.by_point.get(ch)
        kind = f.kind if f is not None and f.kind != "swap" else None
        if p.signal == "DI":
            if kind == "open":
                return False, False, "OK"
            if kind == "stuck":
                return True, True, "OK"
            raw = bool(self.field_signal(self.source[ch]))
            raw = (not raw) if kind == "inverted" else raw
            return raw, raw, "OK"
        s_lo, s_hi = p.signal_range
        if kind == "open":
            raw = OPEN_RAW[p.signal]
        elif kind == "stuck":
            raw = p.frac_to_signal(f.params["frac"])
        else:
            sigma = FAULT_NOISE if kind == "noise" else BASE_NOISE
            raw = float(self.field_signal(self.source[ch])) + self.rng.gauss(0.0, sigma) * (s_hi - s_lo)
        return raw, self._scale(p, raw), self._status(p, raw)

    def _scale(self, p: Point, raw: float) -> float:
        cfg = self.config[p.tag]
        if p.signal == "AI_RTD":
            return rtd_temp(raw, cfg.r0, cfg.alpha)
        return frac_to_eng(cfg.lo, cfg.hi, cfg.scaling, p.signal_to_frac(raw))

    @staticmethod
    def _status(p: Point, raw: float) -> str:
        if p.signal == "AI_4_20mA":
            return "WIRE_BREAK" if raw < 3.6 else ("OVERRANGE" if raw > 21.0 else "OK")
        if p.signal == "AI_0_10V":
            return "OVERRANGE" if raw > 10.5 else ("UNDERRANGE" if raw < -0.5 else "OK")
        return "OVERRANGE" if raw > 400.0 else ("UNDERRANGE" if raw < 18.0 else "OK")


def random_fault(kind: str, p: Point, rng: random.Random, partner: Point | None = None) -> Fault:
    """Draw fault parameters for one point (used by the campaign)."""
    if kind == "swap":
        return Fault("swap", p.tag, partner.tag)
    if kind == "stuck":
        return Fault("stuck", p.tag, params={"frac": round(rng.uniform(0.0, 1.0), 4)} if p.is_analog else {})
    if kind == "scaling":
        if p.signal == "AI_RTD":
            return Fault("scaling", p.tag, params={"alpha": 0.003926})  # wrong RTD curve
        return Fault("scaling", p.tag, params=wrong_range(p, rng.choice(("span", "widen"))))
    return Fault(kind, p.tag)


def wrong_range(p: Point, mode: str) -> dict:
    """Controller range that differs from the field device. 'widen' keeps mid-scale identical."""
    lo, hi = p.lo, p.hi
    if p.scaling == "log":
        a, b = math.log10(lo), math.log10(hi)
        a, b = (a, a + 1.25 * (b - a)) if mode == "span" else (a - 1, b + 1)
        return {"lo": 10**a, "hi": 10**b, "mode": mode}
    span = hi - lo
    if mode == "span":
        return {"lo": lo, "hi": lo + 1.25 * span, "mode": mode}
    return {"lo": lo - 0.25 * span, "hi": hi + 0.25 * span, "mode": mode}
