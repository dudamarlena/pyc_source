# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/NASDAQ.py
# Compiled at: 2018-08-30 11:42:23
# Size of source mod 2**32: 944 bytes
"""
National Association of Securities Dealers Automated Quotations - Composite Index (NASDAQ IXIC)

Daily averaged index by business day, from 2000 to 2016.

Source: http://www.nasdaq.com/aspx/flashquotes.aspx?symbol=IXIC&selected=IXIC
"""
from pyFTS.data import common
import pandas as pd, numpy as np

def get_data(field='avg'):
    """
    Get a simple univariate time series data.

    :param field: the dataset field name to extract
    :return: numpy array
    """
    dat = get_dataframe()
    dat = np.array(dat[field])
    return dat


def get_dataframe():
    """
    Get the complete multivariate time series data.

    :return: Pandas DataFrame
    """
    dat = common.get_dataframe('NASDAQ.csv.bz2', 'https://github.com/petroniocandido/pyFTS/raw/8f20f3634aa6a8f58083bdcd1bbf93795e6ed767/pyFTS/data/NASDAQ.csv.bz2',
      sep=',',
      compression='bz2')
    return dat