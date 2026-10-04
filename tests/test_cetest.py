from iokit import cetest, interlock

from .conftest import ROOT


def spec():
    return cetest.load_spec(ROOT / "config" / "cause_effect.yaml")


def test_matrix_fully_covered_and_passing():
    rec = cetest.run_cetest(spec())
    s = rec["summary"]
    assert s["failed"] == 0
    assert s["matrix_cells_checked"] == s["causes"] * s["effects"]
    assert s["effects_covered"] == s["effects"]


def test_missing_discrepancy_logic_is_caught():
    def buggy(i, req, state):
        # Door trips only when BOTH channels are open: discrepancy goes unnoticed.
        j = dict(i)
        if j["ZS-601A"] != j["ZS-601B"]:
            j["ZS-601A"] = j["ZS-601B"] = True
        return interlock.scan(j, req, state)

    rec = cetest.run_cetest(spec(), scan=buggy)
    failed_causes = {k["cause"] for k in rec["failed"]}
    assert failed_causes == {"C02", "C03"}


def test_wrong_setpoint_is_caught_by_boundary_check(monkeypatch):
    monkeypatch.setattr(interlock, "FLOW_HEAD_MIN", 8.5)
    rec = cetest.run_cetest(spec())
    assert {(k["cause"], k["step"]) for k in rec["failed"]} == {("C06", "boundary")}


def test_trip_latches_until_reset():
    s = spec()
    state = interlock.State()
    req = dict.fromkeys(s["requests"], True)
    assert not interlock.scan(s["healthy"] | {"FT-101": 5.0}, req, state)["LASER_PERMIT"]
    assert not interlock.scan(s["healthy"], req, state)["LASER_PERMIT"]
    assert interlock.scan(s["healthy"] | {"HS-604": True}, req, state)["LASER_PERMIT"]
