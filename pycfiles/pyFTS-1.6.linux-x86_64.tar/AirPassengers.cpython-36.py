# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/AirPassengers.py
# Compiled at: 2018-08-30 11:18:50
# Size of source mod 2**32: 838 bytes
"""
Monthly totals of a airline passengers from USA, from January 1949 through December 1960.

Source: Hyndman, R.J., Time Series Data Library, http://www-personal.buseco.monash.edu.au/~hyndman/TSDL/.
"""
from pyFTS.data import common
import pandas as pd, numpy as np

def get_data():
    """
    Get a simple univariate time series data.

    :return: numpy array
    """
    dat = get_dataframe()
    dat = np.array(dat['Passengers'])
    return dat


def get_dataframe():
    """
    Get the complete multivariate time series data.

    :return: Pandas DataFrame
    """
    dat = common.get_dataframe('AirPassengers.csv', 'https://github.com/petroniocandido/pyFTS/raw/8f20f3634aa6a8f58083bdcd1bbf93795e6ed767/pyFTS/data/AirPassengers.csv',
      sep=',')
    return dat