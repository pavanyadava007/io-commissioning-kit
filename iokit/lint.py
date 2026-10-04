"""Static checks on the I/O list before anything is generated or tested."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .iolist import ANALOG, SIGNAL_TYPES

COMMON_FIELDS = ("tag", "description", "subsystem", "signal", "channel", "field",
                 "junction_box", "trunk", "cabinet_terminals")
ANALOG_FIELDS = ("range", "units", "scaling", "nominal")
MODULE_PREFIX = {"AI_4_20mA": "AI", "AI_0_10V": "AV", "AI_RTD": "RT", "DI": "DI", "DO": "DO"}
CORE_COUNT = {"AI_4_20mA": 2, "AI_0_10V": 3, "AI_RTD": 3, "DI": 2, "DO": 2}
TEMP_UNITS = ("degC", "K")
ALARM_ORDER = ("lolo", "lo", "hi", "hihi")


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str  # "error" or "warning"
    tag: str
    message: str

    def __str__(self) -> str:
        return f"{self.severity.upper():7} {self.code} {self.tag}: {self.message}"


def lint(doc: dict) -> list[Finding]:
    out: list[Finding] = []

    def err(code, tag, msg, severity="error"):
        out.append(Finding(code, severity, tag, msg))

    points = doc.get("points") or []
    tags, channels, cables, cores = defaultdict(int), defaultdict(list), defaultdict(list), {}
    by_tag = {}
    for p in points:
        tag = p.get("tag", "<no tag>")
        by_tag[tag] = p
        tags[tag] += 1
        sig = p.get("signal")
        missing = [f for f in COMMON_FIELDS if f not in p]
        if sig in ANALOG:
            missing += [f for f in ANALOG_FIELDS if f not in p]
        if missing:
            err("E001", tag, f"missing field(s): {', '.join(missing)}")
        if sig not in SIGNAL_TYPES:
            err("E006", tag, f"unknown signal type {sig!r}")
            continue
        ch = p.get("channel", "")
        channels[ch].append(tag)
        module = ch.split("-")[-1].split(".")[0] if ch else ""
        if not module.startswith(MODULE_PREFIX[sig]):
            err("E007", tag, f"channel {ch} is not on a {MODULE_PREFIX[sig]} module ({sig})")
        field = p.get("field") or {}
        if field.get("cable"):
            cables[field["cable"]].append(tag)
        if len(field.get("cores") or []) != CORE_COUNT[sig]:
            err("E009", tag, f"{sig} needs {CORE_COUNT[sig]} field cores, "
                f"found {len(field.get('cores') or [])}")
        trunk = p.get("trunk") or {}
        for core in trunk.get("cores") or []:
            key = (trunk.get("cable"), core)
            if key in cores:
                err("E004", tag, f"trunk core {key[0]}/{core} already used by {cores[key]}")
            else:
                cores[key] = tag
        if sig in ANALOG and "range" in p:
            out.extend(_check_analog(p, tag, sig))
        elif sig not in ANALOG:
            if "range" in p or "units" in p:
                err("E006", tag, f"{sig} point must not have range/units")
            if not isinstance(p.get("normal"), bool):
                err("E001", tag, "digital point needs boolean 'normal' state")
            if sig == "DI" and p.get("contact") not in ("NO", "NC"):
                err("E001", tag, "DI needs contact: NO or NC")

    for tag, n in tags.items():
        if n > 1:
            err("E002", tag, f"tag defined {n} times")
    for ch, owners in channels.items():
        if len(owners) > 1:
            err("E003", owners[1], f"channel {ch} shared by {', '.join(owners)}")
    for cable, owners in cables.items():
        if len(owners) > 1:
            err("E005", owners[1], f"field cable {cable} used by {', '.join(owners)}")
    out.extend(_check_pairs(by_tag))
    return out


def _check_analog(p: dict, tag: str, sig: str) -> list[Finding]:
    out = []
    lo, hi = p["range"]
    units, scaling = p.get("units"), p.get("scaling")
    if lo >= hi:
        out.append(Finding("E008", "error", tag, f"range low {lo} >= high {hi}"))
        return out
    if scaling not in ("linear", "log"):
        out.append(Finding("E006", "error", tag, f"unknown scaling {scaling!r}"))
    if scaling == "log" and lo <= 0:
        out.append(Finding("E006", "error", tag, "log scaling needs a range low end > 0"))
    if sig == "AI_RTD" and units not in TEMP_UNITS:
        out.append(Finding("E006", "error", tag, f"RTD input with non-temperature units {units!r}"))
    if sig != "AI_RTD" and units in TEMP_UNITS:
        out.append(Finding("W101", "warning", tag, "temperature on a non-RTD input, check device"))
    nominal = p.get("nominal")
    if nominal is not None and not lo <= nominal <= hi:
        out.append(Finding("E010", "error", tag, f"nominal {nominal} outside range [{lo}, {hi}]"))
    alarms = p.get("alarms") or {}
    last = None
    for key in ALARM_ORDER:
        if key not in alarms:
            continue
        val = alarms[key]
        if not lo <= val <= hi:
            out.append(Finding("E011", "error", tag, f"alarm {key}={val} outside range [{lo}, {hi}]"))
        if last is not None and val <= last[1]:
            out.append(Finding("E012", "error", tag, f"alarm {key}={val} not above {last[0]}={last[1]}"))
        last = (key, val)
    for key in alarms:
        if key not in ALARM_ORDER:
            out.append(Finding("E012", "error", tag, f"unknown alarm key {key!r}"))
    return out


def _check_pairs(by_tag: dict) -> list[Finding]:
    out = []
    for tag, p in by_tag.items():
        partner = p.get("redundant_pair")
        if partner is None:
            continue
        q = by_tag.get(partner)
        if q is None:
            out.append(Finding("E013", "error", tag, f"redundant partner {partner} not in I/O list"))
            continue
        if p.get("signal") != "DI" or q.get("signal") != "DI":
            out.append(Finding("E013", "error", tag, "redundant interlock pair must be two DIs"))
        if q.get("redundant_pair") != tag:
            out.append(Finding("E013", "error", tag, f"{partner} does not point back to {tag}"))
        mod = str(p.get("channel", "")).split(".")[0]
        if mod and mod == str(q.get("channel", "")).split(".")[0]:
            out.append(Finding("W102", "warning", tag,
                               f"pair {tag}/{partner} on the same input card {mod}"))
    return out
