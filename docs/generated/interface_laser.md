# Interface description - laser

> SIMULATED bench. Generated from `config/io_list.yaml` - do not edit by hand.

Rack A1, 9 signals. OPC UA namespace `urn:iokit:sim-rack`; each input exposes `<tag>` (engineering value), `<tag>.raw` (mA, V, ohm or bool) and `<tag>.status` (OK, WIRE_BREAK, OVERRANGE, UNDERRANGE). Outputs expose a writable Boolean `<tag>`.

## Analog inputs

| Tag | Description | Signal | Range | Nominal | Alarms | Channel | Device |
|---|---|---|---|---|---|---|---|
| JT-501 | Diode pump current monitor | AI_0_10V | 0 .. 500 A | 0 | hi 450 | A1-AV1.4 | Diode driver PD-501 current monitor output |
| TT-501 | Diode heat sink temperature | AI_RTD | 0 .. 100 degC | 28 | hi 40 | A1-RT2.1 | TE-501 PT100 sensor |

## Digital signals

| Tag | Description | Direction | Contact | Normal state | Pair | Channel | Device |
|---|---|---|---|---|---|---|---|
| PD-501-EN | Diode pump driver enable | controller -> field | - | FALSE | - | A1-DO1.4 | Diode driver PD-501 enable input |
| PD-501-FLT | Diode pump driver healthy (opens on fault) | field -> controller | NC | TRUE | - | A1-DI1.7 | Diode driver PD-501 fault relay (NC) |
| PD-501-RDY | Diode pump driver ready | field -> controller | NO | TRUE | - | A1-DI1.8 | Diode driver PD-501 ready relay (NO) |
| SH-501-CMD | Beam shutter open command | controller -> field | - | FALSE | - | A1-DO1.5 | SH-501 shutter actuator |
| SH-501-ZSO | Beam shutter open limit | field -> controller | NO | FALSE | - | A1-DI2.1 | SH-501 open limit switch (NO) |
| SH-501-ZSC | Beam shutter closed limit | field -> controller | NO | TRUE | - | A1-DI2.2 | SH-501 closed limit switch (NO) |
| XL-501 | Laser-on warning lamp | controller -> field | - | FALSE | - | A1-DO1.6 | XL-501 warning lamp above enclosure door |
