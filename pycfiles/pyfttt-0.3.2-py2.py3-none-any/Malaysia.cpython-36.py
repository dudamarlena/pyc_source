# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/Malaysia.py
# Compiled at: 2018-11-07 07:30:15
# Size of source mod 2**32: 633 bytes
__doc__ = '\nHourly Malaysia eletric load and tempeature\n'
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