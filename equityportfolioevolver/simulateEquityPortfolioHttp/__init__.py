import logging

import json
import numpy as np
import pandas as pd
import azure.functions as func
from .. import stock_forwards_mc

def simulate(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    portfolio_df = None
    try:
        req_body = req.get_json()
        # I have encountered 2 types of errors when there is no JSON,  
        # From Test mock GET call: AttributeError: 'NoneType' object has no attribute 'decode'
        # When running as a Function and using HTTP Call: ValueError: HTTP request does not contain valid JSON data
    except (AttributeError, ValueError): 
        try:
            (isin, long_short, volume, strike, ttm) = stock_forwards_mc.get_forward_data_from_single_row(req.params)
            portfolio_columns = ['isin', 'long_short', 'volume', 'strike', 'ttm']
            portfolio_df = pd.DataFrame([[isin, long_short, volume, strike, ttm]],
                                        columns = portfolio_columns)
        except ValueError as e:
             return func.HttpResponse(str(e), status_code=400)
    else:
        try:
            portfolio_df = stock_forwards_mc.convert_dict_to_dataframe(req_body)
        except ValueError as e:
             return func.HttpResponse(str(e), status_code=400)


    mc = stock_forwards_mc.StockForwardMC(portfolio_df)
    expected_values = mc.get_expected_value()
    ev_as_string = np.array2string(expected_values, precision=2, separator=', ', max_line_width=1000000)
    response_json = json.dumps({"Expected Value": ev_as_string})
    return func.HttpResponse(body=response_json, status_code=200)


