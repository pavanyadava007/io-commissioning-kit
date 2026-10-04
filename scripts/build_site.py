"""Build site/index.html (single self-contained page) from the I/O list and real run outputs."""

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from iokit import iolist  # noqa: E402
from scripts.make_results import LABELS  # noqa: E402

CSS = """
:root{--bg:#fbfbf9;--fg:#1d1f21;--muted:#5b6066;--line:#d9dcdf;--head:#eef0f2;--bad:#b3261e;
--ok:#1e7a3c;--note:#fff6d6}
@media (prefers-color-scheme: dark){:root{--bg:#16181b;--fg:#e6e8ea;--muted:#a0a6ad;--line:#33373c;
--head:#22262a;--bad:#ff8a80;--ok:#7bd88f;--note:#3a3320}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1100px;margin:0 auto;padding:24px 16px 64px}h1{font-size:1.6rem;margin:.2em 0}
h2{font-size:1.2rem;margin-top:2em;border-bottom:1px solid var(--line);padding-bottom:4px}
p,li{max-width:75ch}.muted{color:var(--muted)}.note{background:var(--note);padding:10px 14px;
border-radius:6px}.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:6px}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:6px 8px;text-align:left;
border-bottom:1px solid var(--line);vertical-align:top}th{background:var(--head);position:sticky;top:0}
.FAIL{color:var(--bad);font-weight:600}.PASS{color:var(--ok)}code{font-size:12.5px}
details{margin:8px 0;border:1px solid var(--line);border-radius:6px;padding:6px 10px}
summary{cursor:pointer;font-weight:600}td:first-child,td:nth-child(2){white-space:nowrap}
nav a{margin-right:14px;color:inherit}
"""


def e(x) -> str:
    return html.escape(str(x))


def main() -> None:
    iol = iolist.load(ROOT / "config" / "io_list.yaml")
    rec = json.loads((ROOT / "results/sample_run/commissioning_record.json").read_text())
    issues = json.loads((ROOT / "results/sample_run/issue_log.json").read_text())
    camp = json.loads((ROOT / "results/campaign.json").read_text())
    ce = json.loads((ROOT / "results/cetest/ce_test_record.json").read_text())

    io_rows = []
    for p in iol.points:
        d = p.data
        rng = f"{d['range'][0]:g} .. {d['range'][1]:g} {d['units']}" if p.is_analog else (
            f"normal {'TRUE' if d['normal'] else 'FALSE'}")
        io_rows.append([p.tag, d["description"], p.signal, rng, p.channel, d["field"]["cable"],
                        d["junction_box"]["id"], " ".join(d["cabinet_terminals"])])

    rec_rows = []
    for r in rec["results"]:
        if r["signal"] in ("DI", "DO"):
            found = " / ".join(f"{s['action']}: {'T' if s['found'] else 'F'}" for s in r["steps"])
        else:
            found = " / ".join(f"{s['pct']}%: {s['found']:.4g}" for s in r["steps"])
        word = "PASS" if r["passed"] else "FAIL"
        rec_rows.append([r["tag"], r["channel"], r["signal"], found,
                         f'<span class="{word}">{word}</span>', r["cause_text"]])

    def rows_html(rows):
        out = ""
        for r in rows:
            cells = ""
            for c in r:
                if str(c).startswith('<span class="'):
                    cells += f"<td>{c}</td>"
                else:
                    cells += f"<td>{e(c)}</td>"
            out += f"<tr>{cells}</tr>"
        return out

    def tbl(header, rows):
        th = "".join(f"<th>{e(h)}</th>" for h in header)
        return (f'<div class="wrap"><table><thead><tr>{th}</tr></thead><tbody>{rows_html(rows)}'
                "</tbody></table></div>")

    o, t = camp["overall"], camp["timing_s"]
    pc = [[LABELS.get(k, k), v["n"], f"{v['kit_detected_pct']:.1f} %",
           f"{v['kit_classified_pct']:.1f} %", f"{v['naive_detected_pct']:.1f} %"]
          for k, v in {**camp["per_class"],
                       **{k: v for k, v in camp["per_variant"].items() if k.startswith("scaling/")}
                       }.items()]
    pc.append(["All faults", o["n"], f"{o['kit_detected_pct']:.1f} %",
               f"{o['kit_classified_pct']:.1f} %", f"{o['naive_detected_pct']:.1f} %"])
    s = ce["summary"]
    issue_html = "".join(
        f"<details><summary>{e(i['id'])}: {e(i['title'])}</summary><ul>"
        f"<li>Labels: {e(', '.join(i['labels']))}</li><li>Evidence: {e(i['evidence'])}</li>"
        f"<li>Location: {e(i['location'])}</li><li>Suggested action: {e(i['action'])}</li>"
        f"<li>Status: {e(i['status'])}</li></ul></details>" for i in issues)

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>io-commissioning-kit</title><style>{CSS}</style></head><body><main>
<h1>io-commissioning-kit</h1>
<p class="muted">I/O-list-driven commissioning toolkit for a simulated instrumentation rack of a
laser amplifier test bench. By Pavan Yadava Annappa.</p>
<p class="note"><strong>Everything on this page is simulated.</strong> The rack, the field devices,
the wiring faults and the OPC UA server are a local Python simulation. No real hardware, PLC or
plant data is involved. The interlock logic is a test harness, not a safety function.</p>
<nav><a href="#io">I/O list</a><a href="#record">Commissioning record</a><a href="#issues">Issue
log</a><a href="#campaign">Campaign</a></nav>
<p>Documentation chain: I/O list (YAML) &rarr; lint &rarr; cable schedule, interface description,
loop-check procedure &rarr; loop check over OPC UA &rarr; commissioning record &rarr; issue log.</p>

<h2 id="io">I/O list ({len(iol.points)} points, revision {e(iol.meta.get('revision'))})</h2>
{tbl(["Tag", "Description", "Signal", "Range / normal", "Channel", "Cable", "JB", "Cabinet"],
     io_rows)}

<h2 id="record">Sample commissioning record</h2>
<p>Run with {len(rec['injected_faults_simulation_only'])} planted wiring faults
(<code>config/demo_faults.yaml</code>), tolerance +/- {rec['tolerance_pct_of_span']} % of span,
tester "{e(rec['tester'])}". Result: {rec['summary']['passed']}/{rec['summary']['points']} passed,
{rec['summary']['failed']} failed. Sign-off fields are left blank on purpose.</p>
{tbl(["Tag", "Channel", "Signal", "As found", "Result", "Suspected cause"], rec_rows)}
<p class="muted">Injected faults (simulation only, hidden from the checker):
{e('; '.join(rec['injected_faults_simulation_only']))}</p>

<h2 id="issues">Issue log ({len(issues)} open)</h2>
{issue_html}

<h2 id="campaign">Fault-injection campaign</h2>
<p>{camp['config']['scenarios']} seeded scenarios with 0-{camp['config']['max_faults_per_scenario']}
random wiring faults each ({o['n']} faults). Kit = 5-step loop check with cross-talk check;
naive = one mid-scale reading or one digital state per point. False alarms on healthy points:
kit {o['kit_false_alarms']}/{o['healthy_point_checks']}, naive
{o['naive_false_alarms']}/{o['healthy_point_checks']}. Wall time per scenario over local OPC UA:
kit {t['kit_per_scenario']:.2f} s, naive {t['naive_per_scenario']:.2f} s.</p>
{tbl(["Fault class", "Faults", "Kit detected", "Kit classified", "Naive detected"], pc)}
<p>Cause-and-effect test: {s['causes']} causes x {s['effects']} effects
({s['matrix_cells_checked']} matrix cells), {s['checks']} checks, {s['passed']} passed,
{s['failed']} failed.</p>
<p class="muted">Page generated by <code>scripts/build_site.py</code> from the JSON outputs of the
runs. Numbers are not edited by hand.</p>
</main></body></html>
"""
    (ROOT / "site" / "index.html").write_text(page)
    print("wrote site/index.html")


if __name__ == "__main__":
    main()
