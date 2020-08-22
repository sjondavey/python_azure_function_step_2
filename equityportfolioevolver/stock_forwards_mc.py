import numpy as np
import pandas as pd
import json
from .contracts.portfolio import Portfolio

def get_forward_data_from_single_row(input_json: str)->tuple:
    row = (input_json)
    isin = row.get('isin')
    long_short = row.get('long_short')
    long_short = long_short.lower()
    if not (long_short == 'long' or long_short == 'short'):
        raise ValueError('"long_short variable can only be "long" or "short" for ' + isin)
    volume = row.get('volume')
    try:
        volume = float(volume)
    except ValueError:
        raise ValueError('"volume" variable cannot be converted to float for ' + isin)
    
    strike = row.get('strike')
    try:
        strike = float(strike)
    except ValueError:
        raise ValueError('"strike" variable cannot be converted to float for ' + isin)

    ttm = row.get('ttm')
    try:
        ttm = float(ttm)
    except ValueError:
        raise ValueError('"ttm" variable cannot be converted to float for ' + isin)
    return (isin, long_short, volume, strike, ttm)


def convert_dict_to_dataframe(input_json: str)->pd.DataFrame:
    portfolio = (input_json).get('forwards')
    if portfolio == None:
        raise ValueError('Input JSON message incorrectly formed: should have "forwards"')
    elif len(portfolio) == 0:
        raise ValueError('Input JSON message contains no transactions')
    portfolio_columns = ['isin', 'long_short', 'volume', 'strike', 'ttm']
    data = []
    for row in portfolio:
        (isin, long_short, volume, strike, ttm) = get_forward_data_from_single_row(row)               
        data.append([isin, long_short, volume, strike, ttm])
    stock_df = pd.DataFrame(data, columns = portfolio_columns)
    return stock_df

class StockForwardMC():
    portfolio = None
    # Make these function inputs
    steps_per_path = 10
    num_paths = 2

    def __init__(self, portfolio_df:pd.DataFrame):
        self.portfolio = Portfolio(portfolio_df)

    def get_expected_value(self)->np.ndarray:
        self.portfolio.calculate_monte_carlo_metrics(self.steps_per_path, self.num_paths, 42)
        expected_value = np.mean(self.portfolio.mtm, axis=0)        
        return expected_value


