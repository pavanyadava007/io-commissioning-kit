"""I/O list model: loading, signal ranges and engineering scaling."""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from pathlib import Path

import yaml

ANALOG = ("AI_4_20mA", "AI_0_10V", "AI_RTD")
DIGITAL = ("DI", "DO")
SIGNAL_TYPES = ANALOG + DIGITAL
SIGNAL_UNITS = {"AI_4_20mA": "mA", "AI_0_10V": "V", "AI_RTD": "ohm"}

# PT100 per IEC 60751, linear approximation (the quadratic term is ignored in this demo).
RTD_R0 = 100.0
RTD_ALPHA = 0.00385


def rtd_ohm(temp_c: float, r0: float = RTD_R0, alpha: float = RTD_ALPHA) -> float:
    return r0 * (1.0 + alpha * temp_c)


def rtd_temp(ohm: float, r0: float = RTD_R0, alpha: float = RTD_ALPHA) -> float:
    return (ohm / r0 - 1.0) / alpha


def eng_to_frac(lo: float, hi: float, scaling: str, value: float) -> float:
    """Position of an engineering value inside its range (0.0 = low end, 1.0 = high end)."""
    if scaling == "log":
        if value <= 0:
            return -1.0
        return (math.log10(value) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
    return (value - lo) / (hi - lo)


def frac_to_eng(lo: float, hi: float, scaling: str, frac: float) -> float:
    if scaling == "log":
        return 10 ** (math.log10(lo) + frac * (math.log10(hi) - math.log10(lo)))
    return lo + frac * (hi - lo)


@dataclass(frozen=True)
class Point:
    """One I/O point. `data` keeps the full YAML record for the document generators."""

    tag: str
    signal: str
    channel: str
    data: dict

    @property
    def is_analog(self) -> bool:
        return self.signal in ANALOG

    @property
    def lo(self) -> float:
        return float(self.data["range"][0])

    @property
    def hi(self) -> float:
        return float(self.data["range"][1])

    @property
    def scaling(self) -> str:
        return self.data.get("scaling", "linear")

    @property
    def units(self) -> str:
        return self.data.get("units", "")

    @property
    def signal_range(self) -> tuple[float, float]:
        """Raw signal at 0 % and 100 % of the engineering range."""
        if self.signal == "AI_4_20mA":
            return (4.0, 20.0)
        if self.signal == "AI_0_10V":
            return (0.0, 10.0)
        return (rtd_ohm(self.lo), rtd_ohm(self.hi))

    def frac_to_signal(self, frac: float) -> float:
        s_lo, s_hi = self.signal_range
        return s_lo + frac * (s_hi - s_lo)

    def signal_to_frac(self, raw: float) -> float:
        s_lo, s_hi = self.signal_range
        return (raw - s_lo) / (s_hi - s_lo)

    def eng_frac(self, value: float) -> float:
        return eng_to_frac(self.lo, self.hi, self.scaling, value)

    def eng_at(self, frac: float) -> float:
        return frac_to_eng(self.lo, self.hi, self.scaling, frac)

    @property
    def rest_value(self):
        """Field-side value while the loop is not under test (process nominal / normal state)."""
        if self.is_analog:
            return self.frac_to_signal(self.eng_frac(float(self.data["nominal"])))
        return bool(self.data.get("normal", False))


@dataclass(frozen=True)
class IOList:
    meta: dict
    points: tuple[Point, ...]
    sha256: str

    def by_tag(self) -> dict[str, Point]:
        return {p.tag: p for p in self.points}

    def of_type(self, *signals: str) -> list[Point]:
        return [p for p in self.points if p.signal in signals]


def load_raw(path: str | Path) -> dict:
    return yaml.safe_load(Path(path).read_text())


def load(path: str | Path) -> IOList:
    text = Path(path).read_text()
    doc = yaml.safe_load(text)
    points = tuple(Point(r["tag"], r["signal"], r["channel"], r) for r in doc["points"])
    return IOList(doc.get("meta", {}), points, hashlib.sha256(text.encode()).hexdigest()[:12])
