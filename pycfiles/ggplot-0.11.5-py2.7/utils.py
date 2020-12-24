# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/utils.py
# Compiled at: 2016-08-17 15:55:34
from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.cbook as cbook, numpy as np, pandas as pd, datetime

def format_ticks(ticks):
    are_ints = True
    for t in ticks:
        try:
            if int(t) != t:
                are_ints = False
        except:
            return ticks

    if are_ints == True:
        return [ int(t) for t in ticks ]
    return ticks


def is_sequence_of_strings(obj):
    """
    Returns true if *obj* is iterable and contains strings
    """
    if not cbook.iterable(obj):
        return False
    if not isinstance(obj, np.ndarray) and cbook.is_string_like(obj):
        return False
    for o in obj:
        if not cbook.is_string_like(o):
            return False

    return True


def is_sequence_of_booleans(obj):
    """
    Return True if *obj* is array-like and contains boolean values
    """
    if not cbook.iterable(obj):
        return False
    _it = (isinstance(x, bool) for x in obj)
    if all(_it):
        return True
    return False


def is_categorical(obj):
    """
    Return True if *obj* is array-like and has categorical values

    Categorical values include:
        - strings
        - booleans
    """
    try:
        float(obj.iloc[0])
        return False
    except:
        return True

    if is_sequence_of_strings(obj):
        return True
    if is_sequence_of_booleans(obj):
        return True
    return False


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except:
        return False


date_types = (
 pd.tslib.Timestamp,
 pd.DatetimeIndex,
 pd.Period,
 pd.PeriodIndex,
 datetime.datetime,
 datetime.time)

def is_date(x):
    return isinstance(x, date_types)


def calc_n_bins(series):
    """https://en.wikipedia.org/wiki/Histogram#Number_of_bins_and_width"""
    q75, q25 = np.percentile(series, [75, 25])
    iqr = q75 - q25
    h = 2 * iqr / len(series) ** 0.3333333333333333
    k = (series.max() - series.min()) / h
    return k


def sorted_unique(series):
    """Return the unique values of *series*, correctly sorted."""
    return list(pd.Series(series.unique()).sort_values())