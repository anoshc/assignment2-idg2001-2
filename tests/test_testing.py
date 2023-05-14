import pytest

from src.testing import things
def test_things():
    assert things(2) == 6
    assert things(0) == 0
    assert things(-5) == -15
