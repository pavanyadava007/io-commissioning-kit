# Interface description - vacuum

> SIMULATED bench. Generated from `config/io_list.yaml` - do not edit by hand.

Rack A1, 6 signals. OPC UA namespace `urn:iokit:sim-rack`; each input exposes `<tag>` (engineering value), `<tag>.raw` (mA, V, ohm or bool) and `<tag>.status` (OK, WIRE_BREAK, OVERRANGE, UNDERRANGE). Outputs expose a writable Boolean `<tag>`.

## Analog inputs

| Tag | Description | Signal | Range | Nominal | Alarms | Channel | Device |
|---|---|---|---|---|---|---|---|
| PT-201 | Vacuum, spatial filter tube | AI_0_10V | 1e-08 .. 100 mbar (log) | 1e-05 | hi 0.001 | A1-AV1.1 | PG-201 combination gauge |
| PT-202 | Vacuum, forevacuum line | AI_0_10V | 0.001 .. 1000 mbar (log) | 0.05 | hi 1 | A1-AV1.2 | PG-202 Pirani gauge |

## Digital signals

| Tag | Description | Direction | Contact | Normal state | Pair | Channel | Device |
|---|---|---|---|---|---|---|---|
| VP-201-RUN | Roughing pump running | field -> controller | NO | TRUE | - | A1-DI1.3 | Pump VP-201 status contact (NO) |
| VV-201-CMD | Gate valve open command | controller -> field | - | FALSE | - | A1-DO1.2 | VV-201 solenoid pilot valve |
| VV-201-ZSO | Gate valve open limit | field -> controller | NO | TRUE | - | A1-DI1.4 | VV-201 open limit switch (NO) |
| VV-201-ZSC | Gate valve closed limit | field -> controller | NO | FALSE | - | A1-DI1.5 | VV-201 closed limit switch (NO) |
