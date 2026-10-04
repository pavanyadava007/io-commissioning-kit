"""Document generators: cable schedule, interface descriptions, loop-check procedure.

Output is deterministic (no timestamps) so CI can diff it against the committed copy.
"""

from __future__ import annotations

import csv
import io
from pathlib import Path

from .iolist import SIGNAL_UNITS, IOList, Point

STEPS = (0.0, 0.25, 0.5, 0.75, 1.0)
BANNER = "> SIMULATED bench. Generated from `config/io_list.yaml` - do not edit by hand."


def _fmt(v: float) -> str:
    return f"{v:.3g}" if abs(v) < 1e-2 or abs(v) >= 1e4 else f"{v:.4g}"


def _range(p: Point) -> str:
    return f"{_fmt(p.lo)} .. {_fmt(p.hi)} {p.units}" + (" (log)" if p.scaling == "log" else "")


def _alarms(p: Point) -> str:
    al = p.data.get("alarms") or {}
    return ", ".join(f"{k} {_fmt(v)}" for k, v in al.items()) or "-"


def _table(header: list[str], rows: list[list]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(lines)


def cable_rows(iol: IOList) -> list[list]:
    rows = []
    for p in iol.points:
        d = p.data
        rows.append([
            d["field"]["cable"], p.tag, p.signal, d["field"]["device"],
            "/".join(d["field"]["cores"]), d["junction_box"]["id"],
            " ".join(d["junction_box"]["terminals"]), d["trunk"]["cable"],
            "/".join(str(c) for c in d["trunk"]["cores"]), " ".join(d["cabinet_terminals"]),
            p.channel,
        ])
    return rows


CABLE_HEADER = ["field_cable", "tag", "signal", "from_device", "field_cores", "via_jb",
                "jb_terminals", "trunk_cable", "trunk_cores", "to_cabinet_terminals", "channel"]


def cable_schedule_csv(iol: IOList) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(CABLE_HEADER)
    w.writerows(cable_rows(iol))
    return buf.getvalue()


def cable_schedule_md(iol: IOList) -> str:
    out = [f"# Cable schedule - {iol.meta.get('title', '')}", "", BANNER, "",
           f"Revision {iol.meta.get('revision', '-')}, I/O list sha256 `{iol.sha256}`, "
           f"{len(iol.points)} points.", ""]
    rows = cable_rows(iol)
    for trunk in sorted({r[7] for r in rows}):
        part = [r for r in rows if r[7] == trunk]
        out += [f"## Trunk {trunk} ({sum(len(r[8].split('/')) for r in part)} cores used)", "",
                _table(["Field cable", "Tag", "Signal", "From", "Cores", "JB terminals",
                        "Trunk cores", "Cabinet terminals", "Channel"],
                       [[r[0], r[1], r[2], r[3], r[4], r[6], r[8], r[9], r[10]] for r in part]),
                ""]
    return "\n".join(out)


def interface_md(iol: IOList, subsystem: str) -> str:
    pts = [p for p in iol.points if p.data["subsystem"] == subsystem]
    out = [f"# Interface description - {subsystem}", "", BANNER, "",
           f"Rack A1, {len(pts)} signals. OPC UA namespace `urn:iokit:sim-rack`; each input "
           "exposes `<tag>` (engineering value), `<tag>.raw` (mA, V, ohm or bool) and "
           "`<tag>.status` (OK, WIRE_BREAK, OVERRANGE, UNDERRANGE). Outputs expose a writable "
           "Boolean `<tag>`.", ""]
    analog = [p for p in pts if p.is_analog]
    digital = [p for p in pts if not p.is_analog]
    if analog:
        out += ["## Analog inputs", "", _table(
            ["Tag", "Description", "Signal", "Range", "Nominal", "Alarms", "Channel", "Device"],
            [[p.tag, p.data["description"], p.signal, _range(p), _fmt(p.data["nominal"]),
              _alarms(p), p.channel, p.data["field"]["device"]] for p in analog]), ""]
    if digital:
        out += ["## Digital signals", "", _table(
            ["Tag", "Description", "Direction", "Contact", "Normal state", "Pair", "Channel",
             "Device"],
            [[p.tag, p.data["description"],
              "field -> controller" if p.signal == "DI" else "controller -> field",
              p.data.get("contact", "-"), "TRUE" if p.data["normal"] else "FALSE",
              p.data.get("redundant_pair", "-"), p.channel, p.data["field"]["device"]]
             for p in digital]), ""]
    return "\n".join(out)


def procedure_md(iol: IOList, tol_pct: float) -> str:
    out = ["# Loop-check test procedure", "", BANNER, "",
           f"Tolerance for analog points: +/- {tol_pct} % of span. Each step is run by "
           "`iokit loopcheck`; the same steps can be followed by hand with a loop calibrator.",
           "", "General steps for every point:", "",
           "1. Confirm the field device is isolated and the loop calibrator is connected at the "
           "field terminals listed below.",
           "2. Record the readings of all other channels (cross-talk baseline).",
           "3. Run the injection steps and record the as-found value read over OPC UA.",
           "4. After each step check that no other channel moved (catches crossed cores).",
           "5. Restore the field device and record the result.", ""]
    for p in iol.points:
        d = p.data
        out += [f"## {p.tag} - {d['description']}", "",
                f"Channel {p.channel}, cable {d['field']['cable']} via {d['junction_box']['id']} "
                f"{' '.join(d['junction_box']['terminals'])}, trunk {d['trunk']['cable']} cores "
                f"{'/'.join(str(c) for c in d['trunk']['cores'])}.", ""]
        if p.is_analog:
            unit = SIGNAL_UNITS[p.signal]
            rows = [[f"{int(f * 100)} %", f"{p.frac_to_signal(f):.3f} {unit}",
                     f"{_fmt(p.eng_at(f))} {p.units}", "", ""] for f in STEPS]
            out += [_table(["Step", "Inject", "Expected", "As found", "Pass"], rows), ""]
        elif p.signal == "DI":
            out += [_table(["Step", "Field action", "Expected tag", "As found", "Pass"],
                           [["1", "close contact", "TRUE", "", ""],
                            ["2", "open contact", "FALSE", "", ""]]), ""]
        else:
            out += [_table(["Step", "Command over OPC UA", "Expected at field", "As found",
                            "Pass"],
                           [["1", "FALSE", "de-energised", "", ""],
                            ["2", "TRUE", "energised", "", ""],
                            ["3", "FALSE", "de-energised", "", ""]]), ""]
    return "\n".join(out)


def generate_all(iol: IOList, out_dir: str | Path, tol_pct: float) -> list[Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    files = {"cable_schedule.csv": cable_schedule_csv(iol),
             "cable_schedule.md": cable_schedule_md(iol),
             "loopcheck_procedure.md": procedure_md(iol, tol_pct)}
    for sub in sorted({p.data["subsystem"] for p in iol.points}):
        files[f"interface_{sub}.md"] = interface_md(iol, sub)
    written = []
    for name, text in files.items():
        path = out_dir / name
        path.write_text(text if text.endswith("\n") else text + "\n")
        written.append(path)
    return written
