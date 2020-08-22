import unittest
import math
from equityportfolioevolver.rates.rates_evolver import RatesEvolver

class TestRatesEvolver(unittest.TestCase):
    def setUp(self) -> None:
        self.time_to_maturity = 1.5
        self.steps_per_path = 15
        self.num_paths = 10
        self.re = RatesEvolver(self.time_to_maturity, self.steps_per_path, self.num_paths)

    def test_simulate_forwards(self):
        initial_forward = 15.0
        vol = 0.2
        self.re.set_seed(42)
        forwards = self.re.simulate_forwards(initial_forward, vol)
        self.assertEqual(forwards.size, (self.steps_per_path + 1)* (self.num_paths))
        self.assertEqual(len(forwards.shape), 2)
        self.assertEqual(forwards.shape[0], self.num_paths)
        self.assertEqual(forwards.shape[1], self.steps_per_path + 1)
        # check the first forward is the same for all paths
        self.assertEqual(forwards[0][0], initial_forward)
        self.assertEqual(forwards[self.num_paths - 1][0], initial_forward)
        # more of a regressions test - would be impacted by many things including system architecture. Leaving exact values until I know what impacts this
        self.assertEqual(forwards[0][self.steps_per_path], 15.609312219342286)

    def test_get_forward_discount_factors(self):
        nacc_rate = 0.06
        # Test 1: we need discount factors on every time step in [0, time_to_maturity]
        df = self.re.get_forward_discount_factors(nacc_rate, self.time_to_maturity)
        self.assertEqual(df.size, self.steps_per_path + 1)
        self.assertEqual(len(df.shape), 1)
        self.assertEqual(df.shape[0], self.steps_per_path + 1)
        # Check start and end value are correct
        self.assertEqual(df[0], math.exp(-self.time_to_maturity * nacc_rate))
        self.assertEqual(df[self.steps_per_path], 1.0)

        # Test 2: ttm < self.time_to_maturity
        ttm = self.time_to_maturity * 0.435
        df = self.re.get_forward_discount_factors(nacc_rate, ttm)
        self.assertEqual(len(df.shape), 1)
        self.assertEqual(df.shape[0], self.steps_per_path + 1)
        # Check start and end value are correct
        self.assertEqual(df[0], math.exp(-(ttm * nacc_rate)))
        self.assertEqual(df[7], 0.0)
        self.assertEqual(df[self.steps_per_path], 0.0)
