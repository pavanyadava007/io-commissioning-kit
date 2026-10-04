# Issue log

**SIMULATED RUN - simulated instrumentation rack and simulated wiring faults. No real hardware or plant data.**

10 open issue(s). Each entry can be pasted into an issue tracker.

## ISSUE-001: FT-102 (A1-AI1.2) - scaling mismatch between field device and controller channel

- Labels: commissioning, configuration, cooling
- Suspected cause: scaling
- Evidence: raw signal correct at every step, but 0 % reads -9.983 and 100 % reads 49.99 L/min (I/O list: 0 .. 40)
- Location: cable W-FT-102 via JB-1 X1:3 X1:4, trunk W-JB-1-A1 cores 3/4, cabinet A1-X2:3 A1-X2:4
- Suggested action: Compare transmitter range / sensor type with the controller channel configuration and correct one of them (update the I/O list if the device changed).
- Status: open

## ISSUE-002: LT-101 (A1-AI1.4) - stuck / frozen value

- Labels: commissioning, wiring, cooling
- Suspected cause: stuck
- Evidence: raw frozen at 15.2 mA for all steps
- Location: cable W-LT-101 via JB-1 X1:7 X1:8, trunk W-JB-1-A1 cores 7/8, cabinet A1-X2:7 A1-X2:8
- Suggested action: Check whether the channel or device is frozen (forced value, failed card, shorted contact).
- Status: open

## ISSUE-003: TT-102 (A1-RT1.2) - open circuit

- Labels: commissioning, wiring, cooling
- Suspected cause: open
- Evidence: raw 1e+04 ohm, status OVERRANGE at every step
- Location: cable W-TT-102 via JB-1 X1:12 X1:13 X1:14, trunk W-JB-1-A1 cores 12/13/14, cabinet A1-X2:12 A1-X2:13 A1-X2:14
- Suggested action: Check continuity of field cable and trunk cores, terminal screws and fuses.
- Status: open

## ISSUE-004: PT-301 (A1-AI2.1) - swapped with A1-AI2.3 (PT-302)

- Labels: commissioning, wiring, gas
- Suspected cause: swap
- Evidence: injection at PT-301 field terminals moved channel A1-AI2.3 (PT-302); A1-AI2.1 stayed near 14.4 mA
- Location: cable W-PT-301 via JB-3 X1:1 X1:2, trunk W-JB-3-A1 cores 1/2, cabinet A1-X2:38 A1-X2:39
- Suggested action: Check core termination at the junction box and cabinet terminals for both loops; correct the crossed cores, then repeat the loop check for both points.
- Status: open

## ISSUE-005: PT-302 (A1-AI2.3) - swapped with A1-AI2.1 (PT-301)

- Labels: commissioning, wiring, gas
- Suspected cause: swap
- Evidence: injection at PT-302 field terminals moved channel A1-AI2.1 (PT-301); A1-AI2.3 stayed near 11.99 mA
- Location: cable W-PT-302 via JB-3 X1:5 X1:6, trunk W-JB-3-A1 cores 5/6, cabinet A1-X2:42 A1-X2:43
- Suggested action: Check core termination at the junction box and cabinet terminals for both loops; correct the crossed cores, then repeat the loop check for both points.
- Status: open

## ISSUE-006: MT-401 (A1-AI2.4) - noisy signal (unstable reading)

- Labels: commissioning, wiring, environment
- Suspected cause: noise
- Evidence: reading spread up to 3.53 % of span within one step
- Location: cable W-MT-401 via JB-3 X1:11 X1:12, trunk W-JB-3-A1 cores 11/12, cabinet A1-X2:48 A1-X2:49
- Suggested action: Check shield termination (one end), cable routing near power cables and grounding.
- Status: open

## ISSUE-007: SH-501-ZSO (A1-DI2.1) - swapped with A1-DI2.2 (SH-501-ZSC)

- Labels: commissioning, wiring, laser
- Suspected cause: swap
- Evidence: toggling SH-501-ZSO switched SH-501-ZSC (A1-DI2.2) instead
- Location: cable W-SH-501-ZSO via JB-4 X1:15 X1:16, trunk W-JB-4-A1 cores 15/16, cabinet A1-X2:70 A1-X2:71
- Suggested action: Check core termination at the junction box and cabinet terminals for both loops; correct the crossed cores, then repeat the loop check for both points.
- Status: open

## ISSUE-008: SH-501-ZSC (A1-DI2.2) - swapped with A1-DI2.1 (SH-501-ZSO)

- Labels: commissioning, wiring, laser
- Suspected cause: swap
- Evidence: toggling SH-501-ZSC switched SH-501-ZSO (A1-DI2.1) instead
- Location: cable W-SH-501-ZSC via JB-4 X1:17 X1:18, trunk W-JB-4-A1 cores 17/18, cabinet A1-X2:72 A1-X2:73
- Suggested action: Check core termination at the junction box and cabinet terminals for both loops; correct the crossed cores, then repeat the loop check for both points.
- Status: open

## ISSUE-009: XL-501 (A1-DO1.6) - output polarity reversed

- Labels: commissioning, wiring, laser
- Suspected cause: polarity
- Evidence: state follows the stimulus inverted
- Location: cable W-XL-501 via JB-4 X1:19 X1:20, trunk W-JB-4-A1 cores 19/20, cabinet A1-X2:74 A1-X2:75
- Suggested action: Check output wiring and the configured output logic (normally energised vs normally de-energised).
- Status: open

## ISSUE-010: ZS-601B (A1-DI3.1) - inverted contact (NO wired as NC or vice versa)

- Labels: commissioning, wiring, safety
- Suspected cause: inverted
- Evidence: state follows the stimulus inverted
- Location: cable W-ZS-601B via JB-4 X1:23 X1:24, trunk W-JB-4-A1 cores 23/24, cabinet A1-X2:78 A1-X2:79
- Suggested action: Check whether the device contact is NO or NC against the I/O list and rewire or change the configured logic.
- Status: open
