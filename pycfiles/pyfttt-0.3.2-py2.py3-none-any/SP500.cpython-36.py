# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/SP500.py
# Compiled at: 2018-08-30 11:41:49
# Size of source mod 2**32: 784 bytes
__doc__ = "\nS&P500 - Standard & Poor's 500\n\nDaily averaged index, by business day, from 1950 to 2017.\n\nSource: https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC\n"
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