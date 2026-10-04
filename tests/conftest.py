from pathlib import Path

import pytest

from iokit import iolist

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def iol():
    return iolist.load(ROOT / "config" / "io_list.yaml")
