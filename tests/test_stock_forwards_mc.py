import unittest
import json
import equityportfolioevolver.stock_forwards_mc as fwd_mc
import pandas as pd
from pandas._testing import assert_frame_equal

class TestStockForwardMC(unittest.TestCase):

    def test_get_forward_data_from_single_row(self):
        # 1: long_short not valid variable 
        trade = {'isin': 'isin_1', 'long_short': 'lon', 'volume': 1000, 'strike': 16.4, 'ttm': 1.52}
        self.assertRaisesRegex(ValueError, '"long_short variable can only be "long" or "short" for ', fwd_mc.get_forward_data_from_single_row, trade)

        # 2: Volume not a number
        trade = {'isin': 'isin_1', 'long_short': 'long', 'volume': 's', 'strike': 16.4, 'ttm': 1.52}
        self.assertRaisesRegex(ValueError, '"volume" variable cannot be converted to float for isin_1', fwd_mc.get_forward_data_from_single_row, trade)

        # 3: strike not a number
        trade = {'isin': 'isin_2', 'long_short': 'short', 'volume': 500, 'strike': 's', 'ttm': 0.98}
        self.assertRaisesRegex(ValueError, '"strike" variable cannot be converted to float for isin_2', fwd_mc.get_forward_data_from_single_row, trade)

        # 4: ttm not a number
        trade = {'isin': 'isin_2', 'long_short': 'short', 'volume': 500, 'strike': 12.3, 'ttm': 's'}
        self.assertRaisesRegex(ValueError, '"ttm" variable cannot be converted to float for isin_2', fwd_mc.get_forward_data_from_single_row, trade)


    def test_convert_dict_to_dataframe(self):
        # 1: wrong description 'forward' != 'forwards'
        portfolio = {"forward":[
            {'isin': 'isin_1', 'long_short': 'long', 'volume': 1000.0, 'strike': 16.4, 'ttm': 1.52},
            {'isin': 'isin_1', 'long_short': 'short', 'volume': 500.0, 'strike': 12.3, 'ttm': 0.98}
        ]}
        self.assertRaisesRegex(ValueError, 'Input JSON message incorrectly formed: should have "forwards"', fwd_mc.convert_dict_to_dataframe, portfolio)
        # 2: Contains no transactions
        portfolio = {"forwards":[]}
        self.assertRaisesRegex(ValueError, 'Input JSON message contains no transactions', fwd_mc.convert_dict_to_dataframe, portfolio)

        portfolio = {"forwards":[
            {'isin': 'isin_1', 'long_short': 'long', 'volume': 1000, 'strike': 16.4, 'ttm': 1.52},
            {'isin': 'isin_2', 'long_short': 'short', 'volume': 500, 'strike': 12.3, 'ttm': 0.98}
        ]}
        portfolio_df = fwd_mc.convert_dict_to_dataframe(portfolio)
        portfolio_columns = ['isin', 'long_short', 'volume', 'strike', 'ttm']
        manual_df = pd.DataFrame([['isin_1', 'long', 1000.0, 16.4, 1.52],
                                  ['isin_2', 'short', 500.0, 12.3, 0.98]], 
        columns = portfolio_columns)
        assert_frame_equal(portfolio_df, manual_df)
