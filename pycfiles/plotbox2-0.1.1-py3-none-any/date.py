# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/plotbox/utils/date.py
# Compiled at: 2015-12-03 12:17:34
import numpy as np, pandas as pd, datetime, dateutil.parser as dp

def extract_date(date_input, to_pandas=True):
    """
    Converts any date input into a *datetime* object

    Parameters
    ----------
    date_input : int(s), float(s), or string(s)

    Returns
    -------
    date : *datetime* object(s)

    """
    if isinstance(date_input, (list, pd.core.series.Series, np.ndarray)):
        return [ extract_date(d, to_pandas=to_pandas) for d in date_input ]
    if isinstance(date_input, (int, float)):
        if pd.isnull(date_input):
            return np.nan
    date = from_unixtime(date_input)
    if isinstance(date, datetime.datetime) == False:
        date = dp.parse(str(date), fuzzy=True)
    if to_pandas:
        date = pd.to_datetime(date)
    return date


def from_unixtime(date_input):
    """
    Given a unix timestamp in seconds, milliseconds, microseconds, or nanoseconds from 1-Jan-1970:
    returns a datetime.datetime object.
    If the timestamp is not covertable to float, the method will pass and return the input as given

    Parameters
    ----------
    date_input : int, float, or string

    Returns
    -------
    date : *datetime* object

    """
    try:
        timestamp = float(timestamp)
        digits = number.count_digits(timestamp)
        if digits <= 5:
            base = datetime.datetime(1900, 1, 1)
            delta = datetime.timedelta(days=timestamp)
            timestamp = base + delta
        else:
            base = datetime.datetime(1970, 1, 1)
            if digits > 5 and digits <= 10:
                timestamp_s = timestamp
            elif digits > 10 and digits <= 13:
                timestamp_s = timestamp * 0.001
            elif digits > 13 and digits <= 16:
                timestamp_s = timestamp * 1e-06
            elif digits > 16 and digits <= 19:
                timestamp_s = timestamp * 1e-09
            delta = datetime.timedelta(seconds=timestamp_s)
            date = base + delta
    except:
        pass

    return date