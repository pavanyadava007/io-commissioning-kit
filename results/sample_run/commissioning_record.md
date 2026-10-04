# Loop-check commissioning record

**SIMULATED RUN - simulated instrumentation rack and simulated wiring faults. No real hardware or plant data.**

- Rack: Laser amplifier test bench - instrumentation rack A1 (SIMULATED)
- I/O list revision C, sha256 `8cf86df6eed1`
- Mode: kit, seed 7
- Timestamp (UTC): 2026-10-04T23:08:51Z
- Tester: simulated run
- Tolerance: +/- 0.5 % of span
- Result: 28/38 passed, 10 failed (wall time 1.89 s)

| Tag | Channel | Signal | As found | Max error % | Result | Suspected cause |
|---|---|---|---|---|---|---|
| FT-101 | A1-AI1.1 | AI_4_20mA | 0%: 0.003949 / 25%: 4.993 / 50%: 9.997 / 75%: 15.01 / 100%: 20 | 0.04 | PASS | - |
| FT-102 | A1-AI1.2 | AI_4_20mA | 0%: -9.983 / 25%: 5.023 / 50%: 20.01 / 75%: 34.98 / 100%: 49.99 | 24.97 | FAIL | scaling mismatch between field device and controller channel |
| PT-101 | A1-AI1.3 | AI_4_20mA | 0%: 0.0005416 / 25%: 2.5 / 50%: 4.999 / 75%: 7.499 / 100%: 10.01 | 0.06 | PASS | - |
| LT-101 | A1-AI1.4 | AI_4_20mA | 0%: 70 / 25%: 70 / 50%: 70 / 75%: 70 / 100%: 70 | 70.00 | FAIL | stuck / frozen value |
| TT-101 | A1-RT1.1 | AI_RTD | 0%: -0.02328 / 25%: 12.49 / 50%: 24.97 / 75%: 37.5 / 100%: 50.01 | 0.05 | PASS | - |
| TT-102 | A1-RT1.2 | AI_RTD | 0%: 2.571e+04 / 25%: 2.571e+04 / 50%: 2.571e+04 / 75%: 2.571e+04 / 100%: 2.571e+04 | 51428.60 | FAIL | open circuit |
| TT-103 | A1-RT1.3 | AI_RTD | 0%: -0.01903 / 25%: 25 / 50%: 50.01 / 75%: 75.02 / 100%: 100 | 0.02 | PASS | - |
| CH-101-RUN | A1-DI1.1 | DI | close contact: T / open contact: F | - | PASS | - |
| CH-101-FLT | A1-DI1.2 | DI | close contact: T / open contact: F | - | PASS | - |
| CH-101-EN | A1-DO1.1 | DO | command FALSE: F / command TRUE: T / command FALSE: F | - | PASS | - |
| PT-201 | A1-AV1.1 | AI_0_10V | 0%: 9.993e-09 / 25%: 3.168e-06 / 50%: 0.0009951 / 75%: 0.319 / 100%: 98.89 | 0.05 | PASS | - |
| PT-202 | A1-AV1.2 | AI_0_10V | 0%: 0.001 / 25%: 0.03162 / 50%: 1.002 / 75%: 31.61 / 100%: 996.5 | 0.03 | PASS | - |
| VP-201-RUN | A1-DI1.3 | DI | close contact: T / open contact: F | - | PASS | - |
| VV-201-CMD | A1-DO1.2 | DO | command FALSE: F / command TRUE: T / command FALSE: F | - | PASS | - |
| VV-201-ZSO | A1-DI1.4 | DI | close contact: T / open contact: F | - | PASS | - |
| VV-201-ZSC | A1-DI1.5 | DI | close contact: T / open contact: F | - | PASS | - |
| PT-301 | A1-AI2.1 | AI_4_20mA | 0%: 3.899 / 25%: 3.9 / 50%: 3.901 / 75%: 3.902 / 100%: 3.898 | 64.99 | FAIL | swapped with A1-AI2.3 (PT-302) |
| FT-301 | A1-AI2.2 | AI_4_20mA | 0%: 0.003372 / 25%: 12.49 / 50%: 25.01 / 75%: 37.51 / 100%: 50.01 | 0.02 | PASS | - |
| PT-302 | A1-AI2.3 | AI_4_20mA | 0%: 4.995 / 25%: 5.002 / 50%: 4.995 / 75%: 5 / 100%: 4.998 | 50.02 | FAIL | swapped with A1-AI2.1 (PT-301) |
| XV-301-CMD | A1-DO1.3 | DO | command FALSE: F / command TRUE: T / command FALSE: F | - | PASS | - |
| XV-301-ZSO | A1-DI1.6 | DI | close contact: T / open contact: F | - | PASS | - |
| MT-401 | A1-AI2.4 | AI_4_20mA | 0%: -0.1633 / 25%: 25.25 / 50%: 49.23 / 75%: 74.9 / 100%: 99.4 | 0.77 | FAIL | noisy signal (unstable reading) |
| TT-401 | A1-RT1.4 | AI_RTD | 0%: -0.01396 / 25%: 12.49 / 50%: 25 / 75%: 37.5 / 100%: 49.99 | 0.03 | PASS | - |
| AT-402 | A1-AV1.3 | AI_0_10V | 0%: -0.002713 / 25%: 6.242 / 50%: 12.5 / 75%: 18.76 / 100%: 25 | 0.04 | PASS | - |
| PD-501-EN | A1-DO1.4 | DO | command FALSE: F / command TRUE: T / command FALSE: F | - | PASS | - |
| PD-501-FLT | A1-DI1.7 | DI | close contact: T / open contact: F | - | PASS | - |
| PD-501-RDY | A1-DI1.8 | DI | close contact: T / open contact: F | - | PASS | - |
| JT-501 | A1-AV1.4 | AI_0_10V | 0%: 0.05945 / 25%: 125.2 / 50%: 249.8 / 75%: 374.8 / 100%: 500 | 0.04 | PASS | - |
| TT-501 | A1-RT2.1 | AI_RTD | 0%: 0.04905 / 25%: 25 / 50%: 49.99 / 75%: 75.02 / 100%: 100 | 0.05 | PASS | - |
| SH-501-CMD | A1-DO1.5 | DO | command FALSE: F / command TRUE: T / command FALSE: F | - | PASS | - |
| SH-501-ZSO | A1-DI2.1 | DI | close contact: T / open contact: T | - | FAIL | swapped with A1-DI2.2 (SH-501-ZSC) |
| SH-501-ZSC | A1-DI2.2 | DI | close contact: F / open contact: F | - | FAIL | swapped with A1-DI2.1 (SH-501-ZSO) |
| XL-501 | A1-DO1.6 | DO | command FALSE: T / command TRUE: F / command FALSE: T | - | FAIL | output polarity reversed |
| ZS-601A | A1-DI2.3 | DI | close contact: T / open contact: F | - | PASS | - |
| ZS-601B | A1-DI3.1 | DI | close contact: F / open contact: T | - | FAIL | inverted contact (NO wired as NC or vice versa) |
| HS-602A | A1-DI2.4 | DI | close contact: T / open contact: F | - | PASS | - |
| HS-602B | A1-DI3.2 | DI | close contact: T / open contact: F | - | PASS | - |
| HS-604 | A1-DI2.5 | DI | close contact: T / open contact: F | - | PASS | - |

## Sign-off

| Tested by | Witnessed by | Date |
|---|---|---|
|  |  |  |

## Injected faults (simulation only, hidden from the checker)

- swap PT-301<->PT-302
- swap SH-501-ZSO<->SH-501-ZSC
- open TT-102
- scaling FT-102
- inverted ZS-601B
- stuck LT-101
- polarity XL-501
- noise MT-401
