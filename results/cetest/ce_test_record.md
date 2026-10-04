# Cause-and-effect test record

**SIMULATED RUN - simulated instrumentation rack and simulated wiring faults. No real hardware or plant data. Logic test harness only, not a safety function.**

- Timestamp (UTC): 2026-10-04T23:08:52Z, tester: simulated run
- 15 causes x 6 effects = 90 matrix cells checked; 327 checks, 327 passed, 0 failed

## Matrix (X = cause trips effect; result of the trip step)

| Cause | Description | LASER_PERMIT | PD-501-EN | SH-501-CMD | XL-501 | VV-201-CMD | XV-301-CMD | Result |
|---|---|---|---|---|---|---|---|---|
| C01 | Door open (both channels) | X | X | X | X |  |  | PASS |
| C02 | Door channels disagree (A closed | X | X | X | X |  |  | PASS |
| C03 | Door channels disagree (A open | X | X | X | X |  |  | PASS |
| C04 | E-stop chain open | X | X | X | X | X | X | PASS |
| C05 | E-stop channels disagree | X | X | X | X | X | X | PASS |
| C06 | Amplifier head coolant flow below 8 L/min | X | X | X | X |  |  | PASS |
| C07 | Diode coolant flow below 15 L/min | X | X | X | X |  |  | PASS |
| C08 | Coolant supply temperature above 28 degC | X | X | X | X |  |  | PASS |
| C09 | Spatial filter vacuum worse than 1e-3 mbar | X | X | X | X |  |  | PASS |
| C10 | Forevacuum worse than 1 mbar | X | X | X | X | X |  | PASS |
| C11 | Lab oxygen below 19.5 %vol | X | X | X | X |  | X | PASS |
| C12 | Shutter position unknown (both limits off) | X | X | X | X |  |  | PASS |
| C13 | Shutter position unknown (both limits on) | X | X | X | X |  |  | PASS |
| C14 | Chiller fault | X | X | X | X |  |  | PASS |
| C15 | Diode driver fault | X | X | X | X |  |  | PASS |

Steps per cause: trip, cause cleared without reset (trip must stay latched), reset, and a boundary value just inside the limit where given.

## Sign-off

| Tested by | Witnessed by | Date |
|---|---|---|
|  |  |  |
