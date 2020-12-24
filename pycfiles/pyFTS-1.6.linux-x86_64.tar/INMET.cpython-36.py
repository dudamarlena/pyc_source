# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/INMET.py
# Compiled at: 2018-08-29 17:47:38
# Size of source mod 2**32: 665 bytes
"""
INMET - Instituto Nacional Meteorologia / Brasil

Belo Horizonte station, from 2000-01-01 to  31/12/2012

Source: http://www.inmet.gov.br
"""
from pyFTS.data import common
import pandas as pd

def get_dataframe():
    """
    Get the complete multivariate time series data.

    :return: Pandas DataFrame
    """
    dat = common.get_dataframe('INMET.csv.bz2', 'https://github.com/petroniocandido/pyFTS/raw/8f20f3634aa6a8f58083bdcd1bbf93795e6ed767/pyFTS/data/INMET.csv.bz2',
      sep=';',
      compression='bz2')
    dat['DataHora'] = pd.to_datetime((dat['DataHora']), format='%d/%m/%Y %H:%M')
    return dat