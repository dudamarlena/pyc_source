# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/INMET.py
# Compiled at: 2018-08-29 17:47:38
# Size of source mod 2**32: 665 bytes
__doc__ = '\nINMET - Instituto Nacional Meteorologia / Brasil\n\nBelo Horizonte station, from 2000-01-01 to  31/12/2012\n\nSource: http://www.inmet.gov.br\n'
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