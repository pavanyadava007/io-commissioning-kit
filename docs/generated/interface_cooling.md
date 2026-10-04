# Interface description - cooling

> SIMULATED bench. Generated from `config/io_list.yaml` - do not edit by hand.

Rack A1, 10 signals. OPC UA namespace `urn:iokit:sim-rack`; each input exposes `<tag>` (engineering value), `<tag>.raw` (mA, V, ohm or bool) and `<tag>.status` (OK, WIRE_BREAK, OVERRANGE, UNDERRANGE). Outputs expose a writable Boolean `<tag>`.

## Analog inputs

| Tag | Description | Signal | Range | Nominal | Alarms | Channel | Device |
|---|---|---|---|---|---|---|---|
| FT-101 | Coolant flow, amplifier head circuit | AI_4_20mA | 0 .. 20 L/min | 12 | lo 8, lolo 6 | A1-AI1.1 | FT-101 flow transmitter |
| FT-102 | Coolant flow, diode pump modules | AI_4_20mA | 0 .. 40 L/min | 24 | lo 15 | A1-AI1.2 | FT-102 flow transmitter |
| PT-101 | Coolant supply pressure | AI_4_20mA | 0 .. 10 bar | 4 | lo 2, hi 6 | A1-AI1.3 | PT-101 pressure transmitter |
| LT-101 | Coolant tank level | AI_4_20mA | 0 .. 100 % | 70 | lo 20 | A1-AI1.4 | LT-101 level transmitter |
| TT-101 | Coolant supply temperature | AI_RTD | 0 .. 50 degC | 20 | hi 25, hihi 28 | A1-RT1.1 | TE-101 PT100 sensor |
| TT-102 | Coolant return temperature | AI_RTD | 0 .. 50 degC | 24 | hi 30, hihi 35 | A1-RT1.2 | TE-102 PT100 sensor |
| TT-103 | Amplifier head body temperature | AI_RTD | 0 .. 100 degC | 30 | hi 45 | A1-RT1.3 | TE-103 PT100 sensor |

## Digital signals

| Tag | Description | Direction | Contact | Normal state | Pair | Channel | Device |
|---|---|---|---|---|---|---|---|
| CH-101-RUN | Chiller running | field -> controller | NO | TRUE | - | A1-DI1.1 | Chiller CH-101 status relay (NO) |
| CH-101-FLT | Chiller healthy (opens on fault) | field -> controller | NC | TRUE | - | A1-DI1.2 | Chiller CH-101 fault relay (NC) |
| CH-101-EN | Chiller remote start | controller -> field | - | FALSE | - | A1-DO1.1 | Chiller CH-101 remote start input |
