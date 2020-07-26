import logging

import json
import numpy as np
import azure.functions as func
from . import single_stock_mc

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    isin = None
    long_short = None
    volume = None
    strike = None
    ttm = None

    try:
        req_body = req.get_json()
    except ValueError:
        isin = req.params.get('isin')
        long_short = req.params.get('long_short')
        volume = float(req.params.get('volume'))
        strike = float(req.params.get('strike'))
        ttm = float(req.params.get('ttm'))
    else:
        isin = req_body.get('isin')
        long_short = req_body.get('long_short')
        volume = float(req_body.get('volume'))
        strike = float(req_body.get('strike'))
        ttm = float(req_body.get('ttm'))

    if not isin:
        return func.HttpResponse("Function must have an input \'isin\'", status_code=400)
    if not long_short:
        return func.HttpResponse("Function must have an input \'long_short\'", status_code=400)
    if not volume:
        return func.HttpResponse("Function must have an input \'volume\'", status_code=400)
    if not strike:
        return func.HttpResponse("Function must have an input \'strike\'", status_code=400)
    if not ttm:
        return func.HttpResponse("Function must have an input \'ttm\'", status_code=400)

    long_short = long_short.lower()
    if long_short != 'long' and long_short != 'short':
        return func.HttpResponse("long_short must be either \'long\' or \'short\'", status_code=400)
    if volume < 0:
        return func.HttpResponse("Volume must be positive", status_code=400)
    if strike < 0:
        return func.HttpResponse("Strike must be positive", status_code=400)
    if ttm < 0:
        return func.HttpResponse("ttm must be positive", status_code=400)

    mc = single_stock_mc.SingleStockMC(isin, long_short, volume, strike, ttm)
    expected_values = mc.get_expected_value()
    ev_as_string = np.array2string(expected_values, precision=2, separator=', ', max_line_width=1000000)
    response_json = json.dumps({"Expected Value": ev_as_string})
    return func.HttpResponse(body=response_json, status_code=200)
