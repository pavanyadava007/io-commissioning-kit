# Cable schedule - Laser amplifier test bench - instrumentation rack A1 (SIMULATED)

> SIMULATED bench. Generated from `config/io_list.yaml` - do not edit by hand.

Revision C, I/O list sha256 `8cf86df6eed1`, 38 points.

## Trunk W-JB-1-A1 (23 cores used)

| Field cable | Tag | Signal | From | Cores | JB terminals | Trunk cores | Cabinet terminals | Channel |
|---|---|---|---|---|---|---|---|---|
| W-FT-101 | FT-101 | AI_4_20mA | FT-101 flow transmitter | BN/WH | X1:1 X1:2 | 1/2 | A1-X2:1 A1-X2:2 | A1-AI1.1 |
| W-FT-102 | FT-102 | AI_4_20mA | FT-102 flow transmitter | BN/WH | X1:3 X1:4 | 3/4 | A1-X2:3 A1-X2:4 | A1-AI1.2 |
| W-PT-101 | PT-101 | AI_4_20mA | PT-101 pressure transmitter | BN/WH | X1:5 X1:6 | 5/6 | A1-X2:5 A1-X2:6 | A1-AI1.3 |
| W-LT-101 | LT-101 | AI_4_20mA | LT-101 level transmitter | BN/WH | X1:7 X1:8 | 7/8 | A1-X2:7 A1-X2:8 | A1-AI1.4 |
| W-TT-101 | TT-101 | AI_RTD | TE-101 PT100 sensor | RD/RD/WH | X1:9 X1:10 X1:11 | 9/10/11 | A1-X2:9 A1-X2:10 A1-X2:11 | A1-RT1.1 |
| W-TT-102 | TT-102 | AI_RTD | TE-102 PT100 sensor | RD/RD/WH | X1:12 X1:13 X1:14 | 12/13/14 | A1-X2:12 A1-X2:13 A1-X2:14 | A1-RT1.2 |
| W-TT-103 | TT-103 | AI_RTD | TE-103 PT100 sensor | RD/RD/WH | X1:15 X1:16 X1:17 | 15/16/17 | A1-X2:15 A1-X2:16 A1-X2:17 | A1-RT1.3 |
| W-CH-101-RUN | CH-101-RUN | DI | Chiller CH-101 status relay (NO) | BN/BU | X1:18 X1:19 | 18/19 | A1-X2:18 A1-X2:19 | A1-DI1.1 |
| W-CH-101-FLT | CH-101-FLT | DI | Chiller CH-101 fault relay (NC) | BN/BU | X1:20 X1:21 | 20/21 | A1-X2:20 A1-X2:21 | A1-DI1.2 |
| W-CH-101-EN | CH-101-EN | DO | Chiller CH-101 remote start input | BK/BU | X1:22 X1:23 | 22/23 | A1-X2:22 A1-X2:23 | A1-DO1.1 |

## Trunk W-JB-2-A1 (14 cores used)

| Field cable | Tag | Signal | From | Cores | JB terminals | Trunk cores | Cabinet terminals | Channel |
|---|---|---|---|---|---|---|---|---|
| W-PT-201 | PT-201 | AI_0_10V | PG-201 combination gauge | BN/WH/BU | X1:1 X1:2 X1:3 | 1/2/3 | A1-X2:24 A1-X2:25 A1-X2:26 | A1-AV1.1 |
| W-PT-202 | PT-202 | AI_0_10V | PG-202 Pirani gauge | BN/WH/BU | X1:4 X1:5 X1:6 | 4/5/6 | A1-X2:27 A1-X2:28 A1-X2:29 | A1-AV1.2 |
| W-VP-201-RUN | VP-201-RUN | DI | Pump VP-201 status contact (NO) | BN/BU | X1:7 X1:8 | 7/8 | A1-X2:30 A1-X2:31 | A1-DI1.3 |
| W-VV-201-CMD | VV-201-CMD | DO | VV-201 solenoid pilot valve | BK/BU | X1:9 X1:10 | 9/10 | A1-X2:32 A1-X2:33 | A1-DO1.2 |
| W-VV-201-ZSO | VV-201-ZSO | DI | VV-201 open limit switch (NO) | BN/BU | X1:11 X1:12 | 11/12 | A1-X2:34 A1-X2:35 | A1-DI1.4 |
| W-VV-201-ZSC | VV-201-ZSC | DI | VV-201 closed limit switch (NO) | BN/BU | X1:13 X1:14 | 13/14 | A1-X2:36 A1-X2:37 | A1-DI1.5 |

## Trunk W-JB-3-A1 (18 cores used)

| Field cable | Tag | Signal | From | Cores | JB terminals | Trunk cores | Cabinet terminals | Channel |
|---|---|---|---|---|---|---|---|---|
| W-PT-301 | PT-301 | AI_4_20mA | PT-301 pressure transmitter | BN/WH | X1:1 X1:2 | 1/2 | A1-X2:38 A1-X2:39 | A1-AI2.1 |
| W-FT-301 | FT-301 | AI_4_20mA | FT-301 thermal mass flow meter | BN/WH | X1:3 X1:4 | 3/4 | A1-X2:40 A1-X2:41 | A1-AI2.2 |
| W-PT-302 | PT-302 | AI_4_20mA | PT-302 pressure transmitter | BN/WH | X1:5 X1:6 | 5/6 | A1-X2:42 A1-X2:43 | A1-AI2.3 |
| W-XV-301-CMD | XV-301-CMD | DO | XV-301 solenoid valve | BK/BU | X1:7 X1:8 | 7/8 | A1-X2:44 A1-X2:45 | A1-DO1.3 |
| W-XV-301-ZSO | XV-301-ZSO | DI | XV-301 open position switch (NO) | BN/BU | X1:9 X1:10 | 9/10 | A1-X2:46 A1-X2:47 | A1-DI1.6 |
| W-MT-401 | MT-401 | AI_4_20mA | MT-401 humidity transmitter | BN/WH | X1:11 X1:12 | 11/12 | A1-X2:48 A1-X2:49 | A1-AI2.4 |
| W-TT-401 | TT-401 | AI_RTD | TE-401 PT100 sensor | RD/RD/WH | X1:13 X1:14 X1:15 | 13/14/15 | A1-X2:50 A1-X2:51 A1-X2:52 | A1-RT1.4 |
| W-AT-402 | AT-402 | AI_0_10V | AT-402 oxygen depletion monitor | BN/WH/BU | X1:16 X1:17 X1:18 | 16/17/18 | A1-X2:53 A1-X2:54 A1-X2:55 | A1-AV1.3 |

## Trunk W-JB-4-A1 (30 cores used)

| Field cable | Tag | Signal | From | Cores | JB terminals | Trunk cores | Cabinet terminals | Channel |
|---|---|---|---|---|---|---|---|---|
| W-PD-501-EN | PD-501-EN | DO | Diode driver PD-501 enable input | BK/BU | X1:1 X1:2 | 1/2 | A1-X2:56 A1-X2:57 | A1-DO1.4 |
| W-PD-501-FLT | PD-501-FLT | DI | Diode driver PD-501 fault relay (NC) | BN/BU | X1:3 X1:4 | 3/4 | A1-X2:58 A1-X2:59 | A1-DI1.7 |
| W-PD-501-RDY | PD-501-RDY | DI | Diode driver PD-501 ready relay (NO) | BN/BU | X1:5 X1:6 | 5/6 | A1-X2:60 A1-X2:61 | A1-DI1.8 |
| W-JT-501 | JT-501 | AI_0_10V | Diode driver PD-501 current monitor output | BN/WH/BU | X1:7 X1:8 X1:9 | 7/8/9 | A1-X2:62 A1-X2:63 A1-X2:64 | A1-AV1.4 |
| W-TT-501 | TT-501 | AI_RTD | TE-501 PT100 sensor | RD/RD/WH | X1:10 X1:11 X1:12 | 10/11/12 | A1-X2:65 A1-X2:66 A1-X2:67 | A1-RT2.1 |
| W-SH-501-CMD | SH-501-CMD | DO | SH-501 shutter actuator | BK/BU | X1:13 X1:14 | 13/14 | A1-X2:68 A1-X2:69 | A1-DO1.5 |
| W-SH-501-ZSO | SH-501-ZSO | DI | SH-501 open limit switch (NO) | BN/BU | X1:15 X1:16 | 15/16 | A1-X2:70 A1-X2:71 | A1-DI2.1 |
| W-SH-501-ZSC | SH-501-ZSC | DI | SH-501 closed limit switch (NO) | BN/BU | X1:17 X1:18 | 17/18 | A1-X2:72 A1-X2:73 | A1-DI2.2 |
| W-XL-501 | XL-501 | DO | XL-501 warning lamp above enclosure door | BK/BU | X1:19 X1:20 | 19/20 | A1-X2:74 A1-X2:75 | A1-DO1.6 |
| W-ZS-601A | ZS-601A | DI | ZS-601 door switch contact A (NC, forced opening) | BN/BU | X1:21 X1:22 | 21/22 | A1-X2:76 A1-X2:77 | A1-DI2.3 |
| W-ZS-601B | ZS-601B | DI | ZS-601 door switch contact B (NC, forced opening) | BN/BU | X1:23 X1:24 | 23/24 | A1-X2:78 A1-X2:79 | A1-DI3.1 |
| W-HS-602A | HS-602A | DI | E-stop chain HS-602 contact A (NC) | BN/BU | X1:25 X1:26 | 25/26 | A1-X2:80 A1-X2:81 | A1-DI2.4 |
| W-HS-602B | HS-602B | DI | E-stop chain HS-602 contact B (NC) | BN/BU | X1:27 X1:28 | 27/28 | A1-X2:82 A1-X2:83 | A1-DI3.2 |
| W-HS-604 | HS-604 | DI | HS-604 reset pushbutton (NO) | BN/BU | X1:29 X1:30 | 29/30 | A1-X2:84 A1-X2:85 | A1-DI2.5 |
