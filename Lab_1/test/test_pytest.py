import pytest
from src.stats_utils import mean, median, mode, variance

def test_mean_basic():
    assert mean([1, 2, 3, 4, 5]) == 3

def test_median_odd():
    assert median([1, 3, 2]) == 2

def test_median_even():
    assert median([1, 2, 3, 4]) == 2.5

def test_mode():
    assert mode([1, 2, 2, 3]) == 2

def test_variance():
    assert variance([1, 2, 3]) == pytest.approx(0.6666, rel=1e-3)

def test_empty_input():
    with pytest.raises(ValueError):
        mean([])

