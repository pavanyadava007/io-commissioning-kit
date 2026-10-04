import asyncio

import pytest

from iokit.cli import load_faults
from iokit.loopcheck import loopcheck
from iokit.opcua import RackClient, RackServer
from iokit.rack import Fault, FieldRack

from .conftest import ROOT


@pytest.fixture(scope="module")
def demo(iol):
    faults, seed = load_faults(ROOT / "config" / "demo_faults.yaml")
    kit = asyncio.run(loopcheck(iol, FieldRack(iol, faults, seed), "kit"))
    naive = asyncio.run(loopcheck(iol, FieldRack(iol, faults, seed), "naive"))
    return {r.tag: r for r in kit}, {r.tag: r for r in naive}


def test_opcua_round_trip(iol):
    async def go():
        rack = FieldRack(iol, seed=0)
        async with RackServer(iol, rack) as srv, RackClient(srv.url, iol) as cli:
            rack.inject("FT-101", 12.0)  # 50 % of 0..20 L/min
            await srv.scan()
            raw, eng, status = (await cli.read_inputs())["FT-101"]
            await cli.write_command("XL-501", True)
            await srv.scan()
            return raw, eng, status, rack.field_output("XL-501")

    raw, eng, status, lamp = asyncio.run(go())
    assert abs(raw - 12.0) < 0.05 and abs(eng - 10.0) < 0.1 and status == "OK" and lamp is True


def test_healthy_rack_passes_everywhere(iol):
    results = asyncio.run(loopcheck(iol, FieldRack(iol, seed=3), "kit"))
    assert [r.tag for r in results if not r.passed] == []


@pytest.mark.parametrize("tag,cause,partner", [
    ("PT-301", "swap", "PT-302"), ("PT-302", "swap", "PT-301"),
    ("SH-501-ZSO", "swap", "SH-501-ZSC"), ("SH-501-ZSC", "swap", "SH-501-ZSO"),
    ("TT-102", "open", None), ("FT-102", "scaling", None), ("ZS-601B", "inverted", None),
    ("LT-101", "stuck", None), ("XL-501", "polarity", None), ("MT-401", "noise", None),
])
def test_each_fault_class_is_detected_and_classified(demo, tag, cause, partner):
    kit, _ = demo
    assert not kit[tag].passed
    assert kit[tag].cause == cause
    assert kit[tag].partner == partner


def test_no_false_alarms_in_demo(demo):
    kit, _ = demo
    flagged = {t for t, r in kit.items() if not r.passed}
    assert flagged == {"PT-301", "PT-302", "SH-501-ZSO", "SH-501-ZSC", "TT-102", "FT-102",
                       "ZS-601B", "LT-101", "XL-501", "MT-401"}


def test_naive_check_misses_mid_scale_coincidences(demo):
    _, naive = demo
    assert naive["FT-102"].passed      # widened range reads correct at 50 %
    assert naive["SH-501-ZSO"].passed  # partner switch rests TRUE
    assert not naive["TT-102"].passed  # open RTD is obvious


def test_open_4_20_reads_wire_break(iol):
    rack = FieldRack(iol, [Fault("open", "FT-101")])
    raw, _, status = rack.read_channel("FT-101")
    assert raw < 3.6 and status == "WIRE_BREAK"


def test_two_faults_on_one_point_rejected(iol):
    with pytest.raises(ValueError):
        FieldRack(iol, [Fault("open", "FT-101"), Fault("swap", "FT-101", "FT-102")])
