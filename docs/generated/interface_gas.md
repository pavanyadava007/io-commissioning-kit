# Interface description - gas

> SIMULATED bench. Generated from `config/io_list.yaml` - do not edit by hand.

Rack A1, 5 signals. OPC UA namespace `urn:iokit:sim-rack`; each input exposes `<tag>` (engineering value), `<tag>.raw` (mA, V, ohm or bool) and `<tag>.status` (OK, WIRE_BREAK, OVERRANGE, UNDERRANGE). Outputs expose a writable Boolean `<tag>`.

## Analog inputs

| Tag | Description | Signal | Range | Nominal | Alarms | Channel | Device |
|---|---|---|---|---|---|---|---|
| PT-301 | N2 purge supply pressure | AI_4_20mA | 0 .. 6 bar | 3 | lo 1.5, hi 4.5 | A1-AI2.1 | PT-301 pressure transmitter |
| FT-301 | N2 purge flow | AI_4_20mA | 0 .. 50 L/min | 10 | lo 2 | A1-AI2.2 | FT-301 thermal mass flow meter |
| PT-302 | Instrument air pressure | AI_4_20mA | 0 .. 10 bar | 6.5 | lo 5 | A1-AI2.3 | PT-302 pressure transmitter |

## Digital signals

| Tag | Description | Direction | Contact | Normal state | Pair | Channel | Device |
|---|---|---|---|---|---|---|---|
| XV-301-CMD | N2 purge valve open command | controller -> field | - | FALSE | - | A1-DO1.3 | XV-301 solenoid valve |
| XV-301-ZSO | N2 purge valve open feedback | field -> controller | NO | FALSE | - | A1-DI1.6 | XV-301 open position switch (NO) |
