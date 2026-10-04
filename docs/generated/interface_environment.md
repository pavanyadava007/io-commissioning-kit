# Interface description - environment

> SIMULATED bench. Generated from `config/io_list.yaml` - do not edit by hand.

Rack A1, 3 signals. OPC UA namespace `urn:iokit:sim-rack`; each input exposes `<tag>` (engineering value), `<tag>.raw` (mA, V, ohm or bool) and `<tag>.status` (OK, WIRE_BREAK, OVERRANGE, UNDERRANGE). Outputs expose a writable Boolean `<tag>`.

## Analog inputs

| Tag | Description | Signal | Range | Nominal | Alarms | Channel | Device |
|---|---|---|---|---|---|---|---|
| MT-401 | Lab room humidity | AI_4_20mA | 0 .. 100 %rH | 40 | hi 60 | A1-AI2.4 | MT-401 humidity transmitter |
| TT-401 | Lab room temperature | AI_RTD | 0 .. 50 degC | 21 | hi 24 | A1-RT1.4 | TE-401 PT100 sensor |
| AT-402 | Lab oxygen concentration | AI_0_10V | 0 .. 25 %vol | 20.9 | lo 19.5 | A1-AV1.3 | AT-402 oxygen depletion monitor |
