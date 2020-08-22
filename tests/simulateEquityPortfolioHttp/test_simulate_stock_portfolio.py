import unittest
import json

import azure.functions as func

from equityportfolioevolver.simulateEquityPortfolioHttp import simulate

class TestSimulateEquityPortfolio(unittest.TestCase):
    def setUp(self) -> None:
        self.isin = "isin_1"
        self.long_short = 'long'
        self.volume = '1234'
        self.strike = '16.4'
        self.ttm = '154'

    def test_simulate_forwards(self): 

        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/simulateEquityPortfolio',
            params={'isin': self.isin, 'long_short': self.long_short, 'volume': self.volume, 'strike': self.strike, 'ttm': self.ttm})

        # Call the function.
        resp = simulate(req)
        
        # Check the output.
        self.assertEqual(
            resp.get_body(),
            b'{"Expected Value": "[-1.68e-01,  1.74e+00,  6.61e+00,  6.94e+01,  8.40e+02,  2.39e+03,  6.88e+03,  8.58e+04,  5.42e+05,  1.28e+06,  6.76e+06]"}',
        )

        # Test with JSON portfolio
        portfolio = {"forwards":[
            {'isin': 'isin_1', 'long_short': 'long', 'volume': 1000, 'strike': 16.4, 'ttm': 1.52},
            {'isin': 'isin_1', 'long_short': 'short', 'volume': 500, 'strike': 12.3, 'ttm': 0.98}
        ]}
        portfolio_dump=json.dumps(portfolio)
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(portfolio).encode('utf8'),
            url='/api/simulateEquityPortfolio',
            params=None)

        resp = simulate(req)
        self.assertEqual(
            resp.get_body(),
            b'{"Expected Value": "[-2550.88, -2795.45, -3586.95, -3115.19, -2332.38, -3337.22, -3391.31, -1350.66,  -581.95, -1264.48, -1261.7 ]"}',
        )
