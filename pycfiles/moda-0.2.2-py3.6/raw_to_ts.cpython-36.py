# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\moda\dataprep\raw_to_ts.py
# Compiled at: 2018-10-31 09:33:17
# Size of source mod 2**32: 1063 bytes
import numpy as np, pandas as pd

def raw_to_ts(raw, min_date=None, max_date=None, date_format=None):
    """
    Turns a raw pd.DataFrame into a time-series DataFrame, by creating a DatetimeIndex and a 'timestamp' column
    :param raw: a pd.DataFrame with a date column
    :param min_date: Minimum date for the time series
    :param max_date: Maximum date for the time series
    :param date_format: date format for faster conversion to datetime (optional)
    :return: a time-series DataFrame
    """
    if 'date' not in raw:
        raise ValueError('File must contain a date column')
    else:
        raw['date'] = pd.to_datetime((raw['date']), format=date_format)
        if min_date is not None:
            raw = raw[(raw['date'] >= min_date)]
        if max_date is not None:
            raw = raw[(raw['date'] <= max_date)]
        raw.set_index((pd.DatetimeIndex(raw['date'])), inplace=True, drop=True)
        if 'date' in raw:
            raw.drop(columns='date', inplace=True)
    raw.loc[:, 'timestamp'] = raw.index.astype(np.int64) // 1000000000
    return raw