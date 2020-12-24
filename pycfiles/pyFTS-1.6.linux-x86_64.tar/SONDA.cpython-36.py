# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/SONDA.py
# Compiled at: 2018-08-29 18:21:07
# Size of source mod 2**32: 973 bytes
"""
SONDA - Sistema de Organização Nacional de Dados Ambientais, from INPE - Instituto Nacional de Pesquisas Espaciais, Brasil.

Brasilia station

Source: http://sonda.ccst.inpe.br/

"""
from pyFTS.data import common
import pandas as pd, numpy as np

def get_data(field):
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
    dat = common.get_dataframe('SONDA_BSB.csv.bz2', 'https://github.com/petroniocandido/pyFTS/raw/8f20f3634aa6a8f58083bdcd1bbf93795e6ed767/pyFTS/data/SONDA_BSB.csv.bz2',
      sep=';',
      compression='bz2')
    dat['datahora'] = pd.to_datetime((dat['datahora']), format='%Y-%m-%d %H:%M:%S')
    return dat