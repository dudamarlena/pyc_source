# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyfmpcloud\info.py
# Compiled at: 2020-05-07 13:35:55
# Size of source mod 2**32: 1081 bytes
from urllib.request import urlopen
import pandas as pd
from pyfmpcloud import settings

def stocks_list():
    """Stocks list API from https://financialmodelingprep.com/developer/docs/#Company-Profile
    
    Input:
        ticker : ticker for which we need the company profile
    Returns:
        Dataframe -- Returns company profile of the requested company (ticker)
    """
    urlroot = settings.get_urlrootfmp()
    apikey = settings.get_apikey()
    url = urlroot + 'company/stock/list?apikey=' + apikey
    response = urlopen(url)
    data = response.read().decode('utf-8')
    return pd.read_json(data)


def company_profile(ticker):
    """Company profile API from https://financialmodelingprep.com/developer/docs/#Symbols-List
    
    Returns:
        DataFrame -- Returns company profile
    """
    urlrootfmp = settings.get_urlrootfmp()
    url = urlrootfmp + 'company/profile/' + ticker
    response = urlopen(url)
    data = response.read().decode('utf-8')
    return pd.read_json(data)