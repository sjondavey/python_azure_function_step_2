import numpy as np
import math 


class RatesEvolver():
    time_to_maturity = 0.0 
    steps_per_path = 0
    num_paths = 0
    dt = 0

    def __init__(self, time_to_maturity:float, steps_per_path:int, num_paths:int):
        self.time_to_maturity = time_to_maturity
        self.steps_per_path = steps_per_path
        self.num_paths = num_paths
        self.dt = self.time_to_maturity / self.steps_per_path
        self.partition = np.linspace(0, time_to_maturity, steps_per_path + 1)

    def set_seed(self, seed:int):
        np.random.seed(seed)

    def simulate_forwards(self, forward:float, vol:float)->np.ndarray:
        sd = vol * np.sqrt(self.dt)
        log_return_matrix = (0.5* sd* sd) + sd*np.random.normal(0,1,(self.num_paths, self.steps_per_path))
        cumsum_log_return_matrix = np.cumsum(log_return_matrix, axis=1)
        stock_price_matrix = forward * np.exp(cumsum_log_return_matrix)
        # append initial foraward
        stock_price_matrix = np.insert(stock_price_matrix, 0, forward, axis=1)
        return stock_price_matrix


    def get_forward_discount_factors(self, nacc_rate:float, ttm:float)->np.ndarray:
        """nacc_rate = Continuously Compounded interset rate
        ttm = the time to maturity for one specific contract (assumed <= rates_evolver.time_to_maturity)
        Returns an array of discount factors at 'time_to_maturity / steps_per_path'
        time intervals. If these time steps exceed 'ttm' the discount factors are 
        set to zero
         """
        # TODO ensure ttm <=  self.time_to_maturity
        times = ttm - self.partition
        mask = times >= 0 # these are times in the partition that are after this 'ttm' 
        discount_factors = np.exp(-times * nacc_rate)
        return discount_factors * mask # Set the ones beyond ttm to zero
