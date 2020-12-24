# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/EURUSD.py
# Compiled at: 2018-11-07 07:34:00
# Size of source mod 2**32: 662 bytes
"""
FOREX market EUR-USD pair.

Daily averaged quotations, by business day, from 2016 to 2018.
"""
from pyFTS.data import common
import pandas as pd, numpy as np

def get_data(field='avg'):
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
    df = common.get_dataframe('EURUSD.csv', 'https://query.data.world/s/od4eojioz4w6o5bbwxjfn6j5zoqtos', sep=',')
    return df