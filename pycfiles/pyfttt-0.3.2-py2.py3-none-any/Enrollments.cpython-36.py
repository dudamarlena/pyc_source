# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/Enrollments.py
# Compiled at: 2018-08-30 11:21:37
# Size of source mod 2**32: 599 bytes
__doc__ = '\nYearly University of Alabama enrollments from 1971 to 1992.\n'
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