# io-commissioning-kit

An I/O-list-driven commissioning toolkit for a **simulated** instrumentation rack of a
high-energy laser amplifier test bench. One YAML I/O list drives the cable schedule, the
interface descriptions, the loop-check procedure, an automated loop check over OPC UA, the
commissioning record and an issue log ready for an issue tracker.

**Live page:** https://huggingface.co/spaces/pavanyadava07/io-commissioning-kit (I/O list, sample commissioning record, issue log and campaign results)

> **Everything here is simulated.** The rack, field devices, wiring faults and the OPC UA server
> are a local Python simulation (asyncua). There is no real PLC, no EtherCAT or TwinCAT, and no
> real plant data. The interlock code is a logic test harness, not a safety function.

## Why

Control-system support during commissioning is mostly about keeping a documentation chain
consistent and following every problem to a fix:

```
I/O list (config/io_list.yaml)
  -> iokit lint            catches duplicate channels/cores, bad ranges, alarm limits, broken pairs
  -> iokit docs            cable schedule (CSV + MD), interface description per subsystem,
                           loop-check procedure with expected mA / V / ohm per step
  -> iokit loopcheck       inject at the field side, read back over OPC UA, cross-talk check
  -> commissioning record  JSON + Markdown, as-found values, pass/fail, blank sign-off fields
  -> issue log             one ticket per failing point with evidence and suspected cause
```

`iokit cetest` does the same for the interlock cause-and-effect matrix, and `iokit campaign`
measures how well the loop check finds wiring faults compared with a quick one-point check.

## What is in the box

| Part | File | What it does |
|---|---|---|
| I/O list | `config/io_list.yaml` | 38 points: 4-20 mA, 0-10 V (incl. log-scale vacuum), PT100, DI, DO; channel, cable, cores, junction box, cabinet terminals |
| Lint | `iokit/lint.py` | duplicate tags / channels / trunk cores / cables, missing fields, alarm limits outside range or out of order, unit vs signal type, module vs signal type, core count, redundant DI pairs |
| Generators | `iokit/docs.py` | `docs/generated/`: cable schedule, 6 interface descriptions, loop-check procedure (deterministic, checked in CI) |
| Simulated rack | `iokit/rack.py` | field devices, loop calibrator, input/output cards; faults: swapped cores, open circuit, wrong scaling, inverted contact, stuck value, DO polarity reversal, noise (seeded) |
| OPC UA | `iokit/opcua.py` | local asyncua server: `<tag>`, `<tag>.raw`, `<tag>.status` per input, writable `<tag>` per output; `scan()` is one controller cycle |
| Loop check | `iokit/loopcheck.py` | 0/25/50/75/100 % with 3 readings per step, cross-talk check, DI/DO both states, cause classification; naive baseline |
| Records | `iokit/records.py` | commissioning record and issue log (JSON + Markdown) |
| Interlocks | `config/cause_effect.yaml`, `iokit/interlock.py`, `iokit/cetest.py` | C&E matrix as the spec, hand-written scan function as the code under test, test record |
| Campaign | `iokit/campaign.py`, `scripts/run_campaign.py` | seeded fault-injection campaign, per-fault-class results |

## Quickstart

```bash
make setup        # uv venv --python 3.11 .venv && uv pip install -e ".[dev]"
make lint test    # ruff + I/O list lint + pytest
make docs         # regenerate docs/generated/
make loopcheck    # sample run with planted faults -> results/sample_run/
make cetest       # C&E test -> results/cetest/
make campaign     # 200 seeded scenarios -> results/campaign.json (a few minutes)
make results      # docs/RESULTS.md, README block below, site/index.html
```

Other commands: `iokit --io tests/data/io_list_broken.yaml lint` shows the linter on a broken
list, `iokit serve` starts the simulated rack on `opc.tcp://127.0.0.1:4840/iokit/` for browsing
with any OPC UA client (for example `uals` from asyncua).

## Measured results

From the runs in `results/` (details per fault class in [docs/RESULTS.md](docs/RESULTS.md)).
The block below is written by `scripts/make_results.py`; numbers are not edited by hand.

<!-- RESULTS:START -->
Campaign: 200 seeded scenarios (seed 1), 0-3 random wiring faults each, 38 I/O points, 288 faults in total. Simulated rack and faults.

| Metric | Kit (full loop check) | Naive baseline |
|---|---|---|
| Faults detected | 288/288 (100.0 %) | 227/288 (78.8 %) |
| Cause classified correctly | 288/288 (100.0 %) | not attempted |
| False alarms on healthy points | 0/7277 (0.0 %) | 0/7277 (0.0 %) |
| Wall time per scenario (local OPC UA, this host) | 0.74 s | 0.09 s |

Cause-and-effect test: 15 causes x 6 effects (90 matrix cells), 327 checks, 327 passed, 0 failed.

Read the 100 % figures with care: the fault simulator and the classification rules were written together, so the campaign shows that the rules separate the seven modelled fault classes without false alarms. It is not a measure of accuracy on real wiring.

Sample loop check (`config/demo_faults.yaml`, 8 planted faults): 10 of 38 points flagged.

Per fault class:

| Fault class | Faults | Kit detected | Kit classified | Naive detected |
|---|---|---|---|---|
| Inverted DI contact (NO/NC) | 48 | 100.0 % | 100.0 % | 100.0 % |
| Noise | 37 | 100.0 % | 100.0 % | 62.2 % |
| Open circuit | 33 | 100.0 % | 100.0 % | 100.0 % |
| DO polarity reversal | 39 | 100.0 % | 100.0 % | 100.0 % |
| Scaling mismatch | 53 | 100.0 % | 100.0 % | 62.3 % |
| Stuck / frozen value | 43 | 100.0 % | 100.0 % | 55.8 % |
| Swapped channels (crossed cores) | 35 | 100.0 % | 100.0 % | 77.1 % |
<!-- RESULTS:END -->

## How the loop check decides

For each analog point the field signal is injected at 5 steps, read back 3 times over OPC UA, and
the readings of all other channels of the same signal type are compared with the injected value.

| Observation | Classified as |
|---|---|
| another channel follows the injection at >= 4 of 5 steps | swapped with that channel |
| readings unstable within one step (> tolerance) | noise |
| status WIRE_BREAK / OVERRANGE, or raw at the open-circuit value at every step | open circuit |
| raw signal correct but engineering value wrong | scaling mismatch (range or RTD curve) |
| raw value does not move | stuck / frozen |
| DI follows inverted / DO output inverted | inverted contact / polarity reversal |
| DI or DO constant FALSE / TRUE | open circuit / stuck (shorted) |

## Limitations

- Simulated rack, simulated field devices and simulated faults. Real loops have effects that are
  not modelled: transmitter damping, card filter times, ground loops, intermittent faults.
- No real PLC: there is no TwinCAT, EtherCAT, Modbus TCP or SCADA in this project. The OPC UA
  server is a local asyncua simulation, and `scan()` is called by the test runner instead of a
  cyclic task.
- The PT100 conversion uses the linear alpha approximation, not the full IEC 60751 polynomial.
- Each campaign scenario puts at most one fault on a point; combined faults on one loop are not
  tested. Faults are drawn from the seven classes listed above only, so the detection rates say
  nothing about other fault types.
- The interlock logic is a test harness only and **not a safety function**. A real system
  implements the logic in the PLC (for example IEC 61131-3 Structured Text) and the safety part in
  a certified safety controller developed to IEC 61508 / IEC 62061 / ISO 13849.
- The naive baseline is a deliberately simple check; a careful technician doing a quick check
  would often do better than it.

## Layout

```
config/       io_list.yaml, cause_effect.yaml, demo_faults.yaml
iokit/        package (lint, docs, rack, opcua, loopcheck, records, interlock, cetest, campaign, cli)
docs/         generated/ (from the I/O list), RESULTS.md (from the runs)
results/      sample_run/, cetest/, campaign.json
scripts/      run_campaign.py, make_results.py, build_site.py
site/         static demo page (index.html) + Space README
tests/        pytest suite, tests/data/io_list_broken.yaml
```

## License

MIT, Pavan Yadava Annappa.
