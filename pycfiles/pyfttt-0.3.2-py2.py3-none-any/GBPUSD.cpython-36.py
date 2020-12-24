# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/GBPUSD.py
# Compiled at: 2018-11-07 07:34:01
# Size of source mod 2**32: 662 bytes
__doc__ = '\nFOREX market GBP-USD pair.\n\nDaily averaged quotations, by business day, from 2016 to 2018.\n'
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
    df = common.get_dataframe('GBPUSD.csv', 'https://query.data.world/s/sw4mijpowb3mqv6bsat7cdj54hyxix', sep=',')
    return df