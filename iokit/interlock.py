"""Interlock logic under test, written the way a PLC scan would be (one pure function per cycle).

A real system would implement this in the PLC (for example IEC 61131-3 Structured Text) and
the safety-relevant part in a certified safety controller. This module is a logic test
harness only and is NOT a safety function.
"""

from __future__ import annotations

from dataclasses import dataclass, field

FLOW_HEAD_MIN = 8.0       # L/min
FLOW_DIODE_MIN = 15.0     # L/min
COOLANT_TEMP_MAX = 28.0   # degC
VACUUM_MAX = 1.0e-3       # mbar
FOREVAC_MAX = 1.0         # mbar
O2_MIN = 19.5             # %vol


@dataclass
class State:
    latched: set[str] = field(default_factory=set)


def active_trips(i: dict) -> set[str]:
    trips = set()
    if not (i["ZS-601A"] and i["ZS-601B"]):
        trips.add("door")
    if not (i["HS-602A"] and i["HS-602B"]):
        trips.add("estop")
    if i["FT-101"] < FLOW_HEAD_MIN or i["FT-102"] < FLOW_DIODE_MIN:
        trips.add("flow")
    if i["TT-101"] > COOLANT_TEMP_MAX:
        trips.add("temp")
    if i["PT-201"] > VACUUM_MAX:
        trips.add("vacuum")
    if i["PT-202"] > FOREVAC_MAX:
        trips.add("forevac")
    if i["AT-402"] < O2_MIN:
        trips.add("oxygen")
    if i["SH-501-ZSO"] == i["SH-501-ZSC"]:
        trips.add("shutter_unknown")
    if not i["CH-101-FLT"] or not i["PD-501-FLT"]:
        trips.add("equipment")
    return trips


def scan(i: dict, req: dict, state: State) -> dict:
    """One controller cycle. Trips latch until the cause is gone and HS-604 reset is pressed."""
    trips = active_trips(i)
    state.latched |= trips
    if i["HS-604"]:
        state.latched &= trips
    permit = not state.latched
    pump = bool(req.get("pump_request")) and permit
    return {
        "LASER_PERMIT": permit,
        "PD-501-EN": pump,
        "SH-501-CMD": bool(req.get("shutter_request")) and permit,
        "XL-501": pump,
        "VV-201-CMD": bool(req.get("gate_valve_request"))
        and not ({"estop", "forevac"} & state.latched),
        "XV-301-CMD": bool(req.get("purge_request"))
        and not ({"estop", "oxygen"} & state.latched),
        "alarms": sorted(state.latched),
    }
