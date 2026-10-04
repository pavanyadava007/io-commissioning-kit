# Loop-check test procedure

> SIMULATED bench. Generated from `config/io_list.yaml` - do not edit by hand.

Tolerance for analog points: +/- 0.5 % of span. Each step is run by `iokit loopcheck`; the same steps can be followed by hand with a loop calibrator.

General steps for every point:

1. Confirm the field device is isolated and the loop calibrator is connected at the field terminals listed below.
2. Record the readings of all other channels (cross-talk baseline).
3. Run the injection steps and record the as-found value read over OPC UA.
4. After each step check that no other channel moved (catches crossed cores).
5. Restore the field device and record the result.

## FT-101 - Coolant flow, amplifier head circuit

Channel A1-AI1.1, cable W-FT-101 via JB-1 X1:1 X1:2, trunk W-JB-1-A1 cores 1/2.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 4.000 mA | 0 L/min |  |  |
| 25 % | 8.000 mA | 5 L/min |  |  |
| 50 % | 12.000 mA | 10 L/min |  |  |
| 75 % | 16.000 mA | 15 L/min |  |  |
| 100 % | 20.000 mA | 20 L/min |  |  |

## FT-102 - Coolant flow, diode pump modules

Channel A1-AI1.2, cable W-FT-102 via JB-1 X1:3 X1:4, trunk W-JB-1-A1 cores 3/4.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 4.000 mA | 0 L/min |  |  |
| 25 % | 8.000 mA | 10 L/min |  |  |
| 50 % | 12.000 mA | 20 L/min |  |  |
| 75 % | 16.000 mA | 30 L/min |  |  |
| 100 % | 20.000 mA | 40 L/min |  |  |

## PT-101 - Coolant supply pressure

Channel A1-AI1.3, cable W-PT-101 via JB-1 X1:5 X1:6, trunk W-JB-1-A1 cores 5/6.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 4.000 mA | 0 bar |  |  |
| 25 % | 8.000 mA | 2.5 bar |  |  |
| 50 % | 12.000 mA | 5 bar |  |  |
| 75 % | 16.000 mA | 7.5 bar |  |  |
| 100 % | 20.000 mA | 10 bar |  |  |

## LT-101 - Coolant tank level

Channel A1-AI1.4, cable W-LT-101 via JB-1 X1:7 X1:8, trunk W-JB-1-A1 cores 7/8.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 4.000 mA | 0 % |  |  |
| 25 % | 8.000 mA | 25 % |  |  |
| 50 % | 12.000 mA | 50 % |  |  |
| 75 % | 16.000 mA | 75 % |  |  |
| 100 % | 20.000 mA | 100 % |  |  |

## TT-101 - Coolant supply temperature

Channel A1-RT1.1, cable W-TT-101 via JB-1 X1:9 X1:10 X1:11, trunk W-JB-1-A1 cores 9/10/11.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 100.000 ohm | 0 degC |  |  |
| 25 % | 104.812 ohm | 12.5 degC |  |  |
| 50 % | 109.625 ohm | 25 degC |  |  |
| 75 % | 114.437 ohm | 37.5 degC |  |  |
| 100 % | 119.250 ohm | 50 degC |  |  |

## TT-102 - Coolant return temperature

Channel A1-RT1.2, cable W-TT-102 via JB-1 X1:12 X1:13 X1:14, trunk W-JB-1-A1 cores 12/13/14.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 100.000 ohm | 0 degC |  |  |
| 25 % | 104.812 ohm | 12.5 degC |  |  |
| 50 % | 109.625 ohm | 25 degC |  |  |
| 75 % | 114.437 ohm | 37.5 degC |  |  |
| 100 % | 119.250 ohm | 50 degC |  |  |

## TT-103 - Amplifier head body temperature

Channel A1-RT1.3, cable W-TT-103 via JB-1 X1:15 X1:16 X1:17, trunk W-JB-1-A1 cores 15/16/17.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 100.000 ohm | 0 degC |  |  |
| 25 % | 109.625 ohm | 25 degC |  |  |
| 50 % | 119.250 ohm | 50 degC |  |  |
| 75 % | 128.875 ohm | 75 degC |  |  |
| 100 % | 138.500 ohm | 100 degC |  |  |

## CH-101-RUN - Chiller running

Channel A1-DI1.1, cable W-CH-101-RUN via JB-1 X1:18 X1:19, trunk W-JB-1-A1 cores 18/19.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## CH-101-FLT - Chiller healthy (opens on fault)

Channel A1-DI1.2, cable W-CH-101-FLT via JB-1 X1:20 X1:21, trunk W-JB-1-A1 cores 20/21.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## CH-101-EN - Chiller remote start

Channel A1-DO1.1, cable W-CH-101-EN via JB-1 X1:22 X1:23, trunk W-JB-1-A1 cores 22/23.

| Step | Command over OPC UA | Expected at field | As found | Pass |
|---|---|---|---|---|
| 1 | FALSE | de-energised |  |  |
| 2 | TRUE | energised |  |  |
| 3 | FALSE | de-energised |  |  |

## PT-201 - Vacuum, spatial filter tube

Channel A1-AV1.1, cable W-PT-201 via JB-2 X1:1 X1:2 X1:3, trunk W-JB-2-A1 cores 1/2/3.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 0.000 V | 1e-08 mbar |  |  |
| 25 % | 2.500 V | 3.16e-06 mbar |  |  |
| 50 % | 5.000 V | 0.001 mbar |  |  |
| 75 % | 7.500 V | 0.3162 mbar |  |  |
| 100 % | 10.000 V | 100 mbar |  |  |

## PT-202 - Vacuum, forevacuum line

Channel A1-AV1.2, cable W-PT-202 via JB-2 X1:4 X1:5 X1:6, trunk W-JB-2-A1 cores 4/5/6.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 0.000 V | 0.001 mbar |  |  |
| 25 % | 2.500 V | 0.03162 mbar |  |  |
| 50 % | 5.000 V | 1 mbar |  |  |
| 75 % | 7.500 V | 31.62 mbar |  |  |
| 100 % | 10.000 V | 1000 mbar |  |  |

## VP-201-RUN - Roughing pump running

Channel A1-DI1.3, cable W-VP-201-RUN via JB-2 X1:7 X1:8, trunk W-JB-2-A1 cores 7/8.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## VV-201-CMD - Gate valve open command

Channel A1-DO1.2, cable W-VV-201-CMD via JB-2 X1:9 X1:10, trunk W-JB-2-A1 cores 9/10.

| Step | Command over OPC UA | Expected at field | As found | Pass |
|---|---|---|---|---|
| 1 | FALSE | de-energised |  |  |
| 2 | TRUE | energised |  |  |
| 3 | FALSE | de-energised |  |  |

## VV-201-ZSO - Gate valve open limit

Channel A1-DI1.4, cable W-VV-201-ZSO via JB-2 X1:11 X1:12, trunk W-JB-2-A1 cores 11/12.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## VV-201-ZSC - Gate valve closed limit

Channel A1-DI1.5, cable W-VV-201-ZSC via JB-2 X1:13 X1:14, trunk W-JB-2-A1 cores 13/14.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## PT-301 - N2 purge supply pressure

Channel A1-AI2.1, cable W-PT-301 via JB-3 X1:1 X1:2, trunk W-JB-3-A1 cores 1/2.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 4.000 mA | 0 bar |  |  |
| 25 % | 8.000 mA | 1.5 bar |  |  |
| 50 % | 12.000 mA | 3 bar |  |  |
| 75 % | 16.000 mA | 4.5 bar |  |  |
| 100 % | 20.000 mA | 6 bar |  |  |

## FT-301 - N2 purge flow

Channel A1-AI2.2, cable W-FT-301 via JB-3 X1:3 X1:4, trunk W-JB-3-A1 cores 3/4.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 4.000 mA | 0 L/min |  |  |
| 25 % | 8.000 mA | 12.5 L/min |  |  |
| 50 % | 12.000 mA | 25 L/min |  |  |
| 75 % | 16.000 mA | 37.5 L/min |  |  |
| 100 % | 20.000 mA | 50 L/min |  |  |

## PT-302 - Instrument air pressure

Channel A1-AI2.3, cable W-PT-302 via JB-3 X1:5 X1:6, trunk W-JB-3-A1 cores 5/6.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 4.000 mA | 0 bar |  |  |
| 25 % | 8.000 mA | 2.5 bar |  |  |
| 50 % | 12.000 mA | 5 bar |  |  |
| 75 % | 16.000 mA | 7.5 bar |  |  |
| 100 % | 20.000 mA | 10 bar |  |  |

## XV-301-CMD - N2 purge valve open command

Channel A1-DO1.3, cable W-XV-301-CMD via JB-3 X1:7 X1:8, trunk W-JB-3-A1 cores 7/8.

| Step | Command over OPC UA | Expected at field | As found | Pass |
|---|---|---|---|---|
| 1 | FALSE | de-energised |  |  |
| 2 | TRUE | energised |  |  |
| 3 | FALSE | de-energised |  |  |

## XV-301-ZSO - N2 purge valve open feedback

Channel A1-DI1.6, cable W-XV-301-ZSO via JB-3 X1:9 X1:10, trunk W-JB-3-A1 cores 9/10.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## MT-401 - Lab room humidity

Channel A1-AI2.4, cable W-MT-401 via JB-3 X1:11 X1:12, trunk W-JB-3-A1 cores 11/12.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 4.000 mA | 0 %rH |  |  |
| 25 % | 8.000 mA | 25 %rH |  |  |
| 50 % | 12.000 mA | 50 %rH |  |  |
| 75 % | 16.000 mA | 75 %rH |  |  |
| 100 % | 20.000 mA | 100 %rH |  |  |

## TT-401 - Lab room temperature

Channel A1-RT1.4, cable W-TT-401 via JB-3 X1:13 X1:14 X1:15, trunk W-JB-3-A1 cores 13/14/15.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 100.000 ohm | 0 degC |  |  |
| 25 % | 104.812 ohm | 12.5 degC |  |  |
| 50 % | 109.625 ohm | 25 degC |  |  |
| 75 % | 114.437 ohm | 37.5 degC |  |  |
| 100 % | 119.250 ohm | 50 degC |  |  |

## AT-402 - Lab oxygen concentration

Channel A1-AV1.3, cable W-AT-402 via JB-3 X1:16 X1:17 X1:18, trunk W-JB-3-A1 cores 16/17/18.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 0.000 V | 0 %vol |  |  |
| 25 % | 2.500 V | 6.25 %vol |  |  |
| 50 % | 5.000 V | 12.5 %vol |  |  |
| 75 % | 7.500 V | 18.75 %vol |  |  |
| 100 % | 10.000 V | 25 %vol |  |  |

## PD-501-EN - Diode pump driver enable

Channel A1-DO1.4, cable W-PD-501-EN via JB-4 X1:1 X1:2, trunk W-JB-4-A1 cores 1/2.

| Step | Command over OPC UA | Expected at field | As found | Pass |
|---|---|---|---|---|
| 1 | FALSE | de-energised |  |  |
| 2 | TRUE | energised |  |  |
| 3 | FALSE | de-energised |  |  |

## PD-501-FLT - Diode pump driver healthy (opens on fault)

Channel A1-DI1.7, cable W-PD-501-FLT via JB-4 X1:3 X1:4, trunk W-JB-4-A1 cores 3/4.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## PD-501-RDY - Diode pump driver ready

Channel A1-DI1.8, cable W-PD-501-RDY via JB-4 X1:5 X1:6, trunk W-JB-4-A1 cores 5/6.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## JT-501 - Diode pump current monitor

Channel A1-AV1.4, cable W-JT-501 via JB-4 X1:7 X1:8 X1:9, trunk W-JB-4-A1 cores 7/8/9.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 0.000 V | 0 A |  |  |
| 25 % | 2.500 V | 125 A |  |  |
| 50 % | 5.000 V | 250 A |  |  |
| 75 % | 7.500 V | 375 A |  |  |
| 100 % | 10.000 V | 500 A |  |  |

## TT-501 - Diode heat sink temperature

Channel A1-RT2.1, cable W-TT-501 via JB-4 X1:10 X1:11 X1:12, trunk W-JB-4-A1 cores 10/11/12.

| Step | Inject | Expected | As found | Pass |
|---|---|---|---|---|
| 0 % | 100.000 ohm | 0 degC |  |  |
| 25 % | 109.625 ohm | 25 degC |  |  |
| 50 % | 119.250 ohm | 50 degC |  |  |
| 75 % | 128.875 ohm | 75 degC |  |  |
| 100 % | 138.500 ohm | 100 degC |  |  |

## SH-501-CMD - Beam shutter open command

Channel A1-DO1.5, cable W-SH-501-CMD via JB-4 X1:13 X1:14, trunk W-JB-4-A1 cores 13/14.

| Step | Command over OPC UA | Expected at field | As found | Pass |
|---|---|---|---|---|
| 1 | FALSE | de-energised |  |  |
| 2 | TRUE | energised |  |  |
| 3 | FALSE | de-energised |  |  |

## SH-501-ZSO - Beam shutter open limit

Channel A1-DI2.1, cable W-SH-501-ZSO via JB-4 X1:15 X1:16, trunk W-JB-4-A1 cores 15/16.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## SH-501-ZSC - Beam shutter closed limit

Channel A1-DI2.2, cable W-SH-501-ZSC via JB-4 X1:17 X1:18, trunk W-JB-4-A1 cores 17/18.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## XL-501 - Laser-on warning lamp

Channel A1-DO1.6, cable W-XL-501 via JB-4 X1:19 X1:20, trunk W-JB-4-A1 cores 19/20.

| Step | Command over OPC UA | Expected at field | As found | Pass |
|---|---|---|---|---|
| 1 | FALSE | de-energised |  |  |
| 2 | TRUE | energised |  |  |
| 3 | FALSE | de-energised |  |  |

## ZS-601A - Enclosure door closed, channel A

Channel A1-DI2.3, cable W-ZS-601A via JB-4 X1:21 X1:22, trunk W-JB-4-A1 cores 21/22.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## ZS-601B - Enclosure door closed, channel B

Channel A1-DI3.1, cable W-ZS-601B via JB-4 X1:23 X1:24, trunk W-JB-4-A1 cores 23/24.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## HS-602A - E-stop chain healthy, channel A

Channel A1-DI2.4, cable W-HS-602A via JB-4 X1:25 X1:26, trunk W-JB-4-A1 cores 25/26.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## HS-602B - E-stop chain healthy, channel B

Channel A1-DI3.2, cable W-HS-602B via JB-4 X1:27 X1:28, trunk W-JB-4-A1 cores 27/28.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |

## HS-604 - Interlock reset pushbutton

Channel A1-DI2.5, cable W-HS-604 via JB-4 X1:29 X1:30, trunk W-JB-4-A1 cores 29/30.

| Step | Field action | Expected tag | As found | Pass |
|---|---|---|---|---|
| 1 | close contact | TRUE |  |  |
| 2 | open contact | FALSE |  |  |
