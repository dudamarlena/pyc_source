# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/sunspots.py
# Compiled at: 2018-08-30 11:45:35
# Size of source mod 2**32: 746 bytes
"""
Monthly sunspot numbers from 1749 to May 2016

Source: https://www.esrl.noaa.gov/psd/gcos_wgsp/Timeseries/SUNSPOT/
"""
from pyFTS.data import common
import pandas as pd, numpy as np

def get_data():
    """
    Get a simple univariate time series data.

    :return: numpy array
    """
    dat = get_dataframe()
    dat = np.array(dat['SUNACTIVITY'])
    return dat


def get_dataframe():
    """
    Get the complete multivariate time series data.

    :return: Pandas DataFrame
    """
    dat = common.get_dataframe('sunspots.csv', 'https://github.com/petroniocandido/pyFTS/raw/8f20f3634aa6a8f58083bdcd1bbf93795e6ed767/pyFTS/data/sunspots.csv',
      sep=',')
    return dat