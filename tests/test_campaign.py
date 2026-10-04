import random

from iokit.campaign import make_scenario, score
from iokit.loopcheck import PointResult
from iokit.rack import Fault


def test_scenarios_are_seeded(iol):
    a = [make_scenario(iol, random.Random(5), 3) for _ in range(1)]
    b = [make_scenario(iol, random.Random(5), 3) for _ in range(1)]
    assert a == b


def test_scenario_faults_never_share_a_point(iol):
    rng = random.Random(11)
    for _ in range(300):
        tags = [t for f in make_scenario(iol, rng, 3) for t in (f.tag, f.partner) if t]
        assert len(tags) == len(set(tags))


def test_score_known_answer():
    faults = [Fault("swap", "A", "B"), Fault("open", "C")]
    results = [PointResult("A", "x", "DI", False, "swap", "B"),
               PointResult("B", "x", "DI", False, "stuck"),
               PointResult("C", "x", "DI", False, "open"),
               PointResult("D", "x", "DI", False, "noise"),
               PointResult("E", "x", "DI", True)]
    s = score(faults, results, 5)
    assert [f["detected"] for f in s["faults"]] == [True, True]
    assert [f["classified"] for f in s["faults"]] == [False, True]
    assert s["false_alarms"] == ["D"] and s["healthy_points"] == 2
