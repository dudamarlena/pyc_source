# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/lnpay_py/utility_helpers.py
# Compiled at: 2020-02-09 16:37:30
# Size of source mod 2**32: 1186 bytes
import requests, lnpay_py, json

def get_request(location):
    """
    Network utility method for making a GET call to a LNPay endpoint

    Parameters
    ----------
    location (str): URL path requested

    Returns
    -------
    Network response as a JSON Object.
    """
    endpoint = lnpay_py.__ENDPOINT_URL__ + location
    headers = {'X-Api-Key':lnpay_py.__PUBLIC_API_KEY__, 
     'X-LNPay-sdk':lnpay_py.__VERSION__}
    r = requests.get(url=endpoint, headers=headers)
    return r.json()


def post_request(location, params):
    """
    Network utility method for making a POST call to a LNPay endpoint

    Parameters
    ----------
    location (str): URL path requested
    params (object): the `data` to be POSTed in the network request

    Returns
    -------
    Network response as a JSON Object.
    """
    endpoint = lnpay_py.__ENDPOINT_URL__ + location
    headers = {'Content-Type':'application/json', 
     'X-Api-Key':lnpay_py.__PUBLIC_API_KEY__, 
     'X-LNPay-sdk':lnpay_py.__VERSION__}
    data = json.dumps(params)
    r = requests.post(url=endpoint, data=data, headers=headers)
    return r.json()