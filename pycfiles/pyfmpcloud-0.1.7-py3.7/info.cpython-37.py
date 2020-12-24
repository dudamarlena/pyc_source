# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyfmpcloud\info.py
# Compiled at: 2020-05-06 11:16:16
# Size of source mod 2**32: 1034 bytes
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
    urlrootfmp = settings.get_urlrootfmp()
    url = urlrootfmp + 'company/stock/list'
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