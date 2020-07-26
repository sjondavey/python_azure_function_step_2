import math
import numpy as np
import pandas as pd
from equityportfolioevolver.rates.rates_evolver import RatesEvolver


class Portfolio():
    portfolio_columns = ['isin', 'long_short', 'volume', 'strike', 'ttm']
    portfolio = None
    portfolio_ttm = 0
    mtm = None # ndarray with shape = (num_paths, steps_per_path + 1)

    def __init__(self, portfolio:pd.DataFrame):
        # TODO error checking on the portfolio (isin in ref data, strike > 0 etc)
        # TODO add more than one asset (first without and then with correlation)
        self.portfolio = portfolio
        self.portfolio_ttm = portfolio['ttm'].max()


    def get_forward_and_volatility(self, equity_isin:str):
        """Lookup market rates from Azure Blob Storage based on equity identifier
        """
        # TODO look up values from an Azure Blob 
        return (15.0, 0.2) 

    def get_nacc_rate_for_discounting(self):
        # TODO look up values from an Azure Blob 
        return 0.06

    def calculate_monte_carlo_metrics(self, steps_per_path:int, num_paths:int, seed = None):
        # TODO: make this use the portfolio 
        # TODO: Make this use rates not hard coded nacc_rate
        re = RatesEvolver(self.portfolio_ttm, steps_per_path, num_paths)
        if seed:
            re.set_seed(seed)
        self.mtm = np.zeros((num_paths, steps_per_path + 1))
        nacc_rate = self.get_nacc_rate_for_discounting()
        for index, row in self.portfolio.iterrows():
            df = re.get_forward_discount_factors(nacc_rate, row['ttm'])
            forward, flat_volatility = self.get_forward_and_volatility(row['isin'])
            simulated_forwards = re.simulate_forwards(forward, flat_volatility)
            values = None
            if row['long_short'] == 'long':
                values = simulated_forwards - row['strike']
            # TODO: Make sure 'long_short' has been checked and made lowercase
            else: # self.portfolio['long_short'][row] == 'short': # 
                values = row['strike'] - simulated_forwards            

            self.mtm = self.mtm + ((values * df) * row['volume'])
        return None


