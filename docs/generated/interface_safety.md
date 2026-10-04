# Interface description - safety

> SIMULATED bench. Generated from `config/io_list.yaml` - do not edit by hand.

Rack A1, 5 signals. OPC UA namespace `urn:iokit:sim-rack`; each input exposes `<tag>` (engineering value), `<tag>.raw` (mA, V, ohm or bool) and `<tag>.status` (OK, WIRE_BREAK, OVERRANGE, UNDERRANGE). Outputs expose a writable Boolean `<tag>`.

## Digital signals

| Tag | Description | Direction | Contact | Normal state | Pair | Channel | Device |
|---|---|---|---|---|---|---|---|
| ZS-601A | Enclosure door closed, channel A | field -> controller | NC | TRUE | ZS-601B | A1-DI2.3 | ZS-601 door switch contact A (NC, forced opening) |
| ZS-601B | Enclosure door closed, channel B | field -> controller | NC | TRUE | ZS-601A | A1-DI3.1 | ZS-601 door switch contact B (NC, forced opening) |
| HS-602A | E-stop chain healthy, channel A | field -> controller | NC | TRUE | HS-602B | A1-DI2.4 | E-stop chain HS-602 contact A (NC) |
| HS-602B | E-stop chain healthy, channel B | field -> controller | NC | TRUE | HS-602A | A1-DI3.2 | E-stop chain HS-602 contact B (NC) |
| HS-604 | Interlock reset pushbutton | field -> controller | NO | FALSE | - | A1-DI2.5 | HS-604 reset pushbutton (NO) |
