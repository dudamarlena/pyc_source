# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/Malaysia.py
# Compiled at: 2018-11-07 07:30:15
# Size of source mod 2**32: 633 bytes
"""
Hourly Malaysia eletric load and tempeature
"""
from pyFTS.data import common
import pandas as pd, numpy as np

def get_data(field='load'):
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
    df = common.get_dataframe('malaysia.csv', 'https://query.data.world/s/e5arbthdytod3m7wfcg7gmtluh3wa5', sep=';')
    return df