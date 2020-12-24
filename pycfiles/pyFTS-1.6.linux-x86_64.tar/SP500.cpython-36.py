# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/SP500.py
# Compiled at: 2018-08-30 11:41:49
# Size of source mod 2**32: 784 bytes
"""
S&P500 - Standard & Poor's 500

Daily averaged index, by business day, from 1950 to 2017.

Source: https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC
"""
from pyFTS.data import common
import pandas as pd, numpy as np

def get_data():
    """
    Get the univariate time series data.

    :return: numpy array
    """
    dat = get_dataframe()
    return np.array(dat['Avg'])


def get_dataframe():
    """
    Get the complete multivariate time series data.

    :return: Pandas DataFrame
    """
    dat = common.get_dataframe('SP500.csv.bz2', 'https://github.com/petroniocandido/pyFTS/raw/8f20f3634aa6a8f58083bdcd1bbf93795e6ed767/pyFTS/data/SP500.csv.bz2',
      sep=',',
      compression='bz2')
    return dat