# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/DowJones.py
# Compiled at: 2018-11-07 07:35:28
# Size of source mod 2**32: 715 bytes
"""
DJI - Dow Jones

Daily averaged index, by business day, from 1985 to 2017.

Source: https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC
"""
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
    df = common.get_dataframe('DowJones.csv', 'https://query.data.world/s/d4hfir3xrelkx33o3bfs5dbhyiztml', sep=',')
    return df