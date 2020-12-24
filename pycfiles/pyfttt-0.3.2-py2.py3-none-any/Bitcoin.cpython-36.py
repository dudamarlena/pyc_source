# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/Bitcoin.py
# Compiled at: 2018-11-07 07:34:41
# Size of source mod 2**32: 714 bytes
__doc__ = '\nBitcoin to USD quotations\n\nDaily averaged index, by business day, from 2010 to 2018.\n\nSource: https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD\n'
from pyFTS.data import common
import pandas as pd, numpy as np

def get_data(field='AVG'):
    """
    Get the univariate time series data.

    :param field: dataset field to load
    :return: numpy array
    """
    dat = get_dataframe()
    return np.array(dat[field])


def get_dataframe():
    """
    Get the complete multivariate time series data.

    :return: Pandas DataFrame
    """
    df = common.get_dataframe('BTCUSD.csv', 'https://query.data.world/s/72gews5w3c7oaf7by5vp7evsasluia', sep=',')
    return df