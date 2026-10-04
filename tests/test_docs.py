from iokit import docs
from iokit.loopcheck import TOL_PCT

from .conftest import ROOT


def test_generators_are_deterministic_and_committed(iol, tmp_path):
    a = docs.generate_all(iol, tmp_path / "a", TOL_PCT)
    b = docs.generate_all(iol, tmp_path / "b", TOL_PCT)
    for pa, pb in zip(a, b, strict=True):
        assert pa.read_text() == pb.read_text()
        committed = ROOT / "docs" / "generated" / pa.name
        assert committed.read_text() == pa.read_text(), f"{pa.name} is stale, run make docs"


def test_cable_schedule_has_one_row_per_point(iol):
    lines = docs.cable_schedule_csv(iol).strip().splitlines()
    assert len(lines) == len(iol.points) + 1
    assert lines[0].startswith("field_cable,tag,signal")


def test_procedure_lists_expected_mA_for_4_20_loop(iol):
    text = docs.procedure_md(iol, TOL_PCT)
    assert "## FT-101" in text and "12.000 mA" in text and "10 L/min" in text
