import numpy as np
import pandas as pd
from ..equityportfolioevolver.contracts.portfolio import Portfolio

class SingleStockMC():
    portfolio = None
    # Make these function inputs
    steps_per_path = 10
    num_paths = 2

    def __init__(self, isin:str, long_short:str, volume:float, strike:float, ttm:float):
        portfolio_columns = ['isin', 'long_short', 'volume', 'strike', 'ttm']
        one_stock_df = pd.DataFrame([[isin, long_short, volume, strike, ttm]],
                                    columns = portfolio_columns)
        self.portfolio = Portfolio(one_stock_df)

    def get_expected_value(self)->np.ndarray:
        self.portfolio.calculate_monte_carlo_metrics(self.steps_per_path, self.num_paths, 42)
        one_stock_mtm = np.mean(self.portfolio.mtm, axis=0)        
        return one_stock_mtm


