# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/Enrollments.py
# Compiled at: 2018-08-30 11:21:37
# Size of source mod 2**32: 599 bytes
"""
Yearly University of Alabama enrollments from 1971 to 1992.
"""
from pyFTS.data import common
import pandas as pd, numpy as np

def get_data():
    """
    Get a simple univariate time series data.

    :return: numpy array
    """
    dat = get_dataframe()
    dat = np.array(dat['Enrollments'])
    return dat


def get_dataframe():
    dat = common.get_dataframe('Enrollments.csv', 'https://github.com/petroniocandido/pyFTS/raw/8f20f3634aa6a8f58083bdcd1bbf93795e6ed767/pyFTS/data/Enrollments.csv',
      sep=';')
    return dat