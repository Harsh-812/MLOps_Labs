import unittest
from src.stats_utils import mean, median, mode, variance

class TestStatsUtils(unittest.TestCase):
    def test_mean_basic(self):
        self.assertEqual(mean([10, 20, 30]), 20)

    def test_median_odd(self):
        self.assertEqual(median([3, 1, 2]), 2)

    def test_median_even(self):
        self.assertEqual(median([1, 2, 3, 4]), 2.5)

    def test_mode(self):
        self.assertEqual(mode([4, 4, 2, 1]), 4)

    def test_variance(self):
        self.assertAlmostEqual(variance([1, 2, 3]), 0.6666, places=3)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            mean([])
        with self.assertRaises(ValueError):
            median(["a", 1, 2])

if __name__ == "__main__":
    unittest.main()

