from iokit import iolist
from iokit.lint import lint

from .conftest import ROOT


def test_real_io_list_is_clean():
    findings = lint(iolist.load_raw(ROOT / "config" / "io_list.yaml"))
    assert [f for f in findings if f.severity == "error"] == []


def test_broken_io_list_finds_every_planted_error():
    findings = lint(iolist.load_raw(ROOT / "tests" / "data" / "io_list_broken.yaml"))
    got = {(f.code, f.tag) for f in findings}
    expected = {
        ("E011", "FT-101"),   # alarm outside range
        ("E002", "FT-101"),   # duplicate tag
        ("E003", "FT-101"),   # duplicate channel
        ("E004", "FT-101"),   # trunk core reused
        ("E006", "TT-101"),   # RTD with bar
        ("E009", "TT-101"),   # core count
        ("E006", "PT-201"),   # log scale from 0
        ("E013", "ZS-601A"),  # missing redundant partner
        ("E007", "ZS-601A"),  # DI on AI module
        ("E001", "XL-501"),   # missing description
    }
    assert expected <= got
    assert got - expected == set(), f"unexpected findings: {got - expected}"


def test_pair_on_same_card_is_a_warning(iol):
    doc = iolist.load_raw(ROOT / "config" / "io_list.yaml")
    for p in doc["points"]:
        if p["tag"] == "ZS-601B":
            p["channel"] = "A1-DI2.8"  # same card as ZS-601A (A1-DI2.3)
    codes = {f.code for f in lint(doc)}
    assert "W102" in codes
