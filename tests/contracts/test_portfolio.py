import unittest
import pandas as pd
from equityportfolioevolver.contracts.portfolio import Portfolio

class TestPortfolio(unittest.TestCase):
    def setUp(self) -> None:
        portfolio_columns = ['isin', 'long_short', 'volume', 'strike', 'ttm']
        self.one_stock_df = pd.DataFrame([['some_isin', 'long', 10000, 16.70, 1.53]],
                                    columns = portfolio_columns)
        self.two_stock_df = pd.DataFrame([['some_isin', 'long', 10000, 16.70, 1.53],
                                     ['another_isin', 'short', 5000, 40.2, 0.96]],
                                    columns = portfolio_columns)

    def test_construction(self):
        max_ttm = self.two_stock_df['ttm'].max()
        portfolio = Portfolio(self.two_stock_df)
        self.assertEqual(portfolio.portfolio_ttm, max_ttm)

    def test_get_forward_and_volatility(self):
        portfolio = Portfolio(self.one_stock_df)
        equity_isin = "universal_isin"
        (forward, volatility) = portfolio.get_forward_and_volatility(equity_isin)
        self.assertEqual(forward, 15.0)
        self.assertEqual(volatility, 0.2)

    def test_calculate_monte_carlo_metrics(self):
        steps_per_path = 10
        num_paths = 2
        # Tests of one stock portfolio
        portfolio = Portfolio(self.one_stock_df)
        portfolio.calculate_monte_carlo_metrics(steps_per_path, num_paths, 42)
        one_stock_mtm = portfolio.mtm
        self.assertEqual(one_stock_mtm.shape, (num_paths, steps_per_path + 1))
        self.assertEqual(one_stock_mtm[0][0], -15508.88900991141)
        # Each path should have the same starting value
        self.assertEqual(one_stock_mtm[1][0], -15508.88900991141)
        self.assertEqual(one_stock_mtm[1][steps_per_path], -83679.05431650515)

        # Tests of two stock portfolio
        portfolio = Portfolio(self.two_stock_df)
        portfolio.calculate_monte_carlo_metrics(steps_per_path, num_paths, 42)
        two_stock_mtm = portfolio.mtm
        self.assertEqual(two_stock_mtm.shape, (num_paths, steps_per_path + 1))
        self.assertEqual(two_stock_mtm[0][0], 103438.5738377359)
        self.assertEqual(two_stock_mtm[1][0], 103438.5738377359)
        # should be the same as the 1 stock portfolio after the second position matures
        self.assertEqual(two_stock_mtm[0][7], one_stock_mtm[0][7]) 
        self.assertEqual(two_stock_mtm[1][7], one_stock_mtm[1][7]) 
        self.assertEqual(two_stock_mtm[1][steps_per_path], one_stock_mtm[1][steps_per_path]) 

