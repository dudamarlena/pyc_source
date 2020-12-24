# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\factors\events.py
# Compiled at: 2018-01-16 04:49:13
# Size of source mod 2**32: 2753 bytes
"""
Factors describing information about event data (e.g. earnings
announcements, acquisitions, dividends, etc.).
"""
from numpy import newaxis
from strategycontainer.utils.numpy_utils import NaTD, busday_count_mask_NaT, datetime64D_dtype, float64_dtype
from .factor import Factor

class BusinessDaysSincePreviousEvent(Factor):
    __doc__ = "\n    Abstract class for business days since a previous event.\n    Returns the number of **business days** (not trading days!) since\n    the most recent event date for each asset.\n\n    This doesn't use trading days for symmetry with\n    BusinessDaysUntilNextEarnings.\n\n    Assets which announced or will announce the event today will produce a\n    value of 0.0. Assets that announced the event on the previous business\n    day will produce a value of 1.0.\n\n    Assets for which the event date is `NaT` will produce a value of `NaN`.\n    "
    window_length = 0
    dtype = float64_dtype

    def _compute(self, arrays, dates, assets, mask):
        announce_dates = arrays[0].astype(datetime64D_dtype)
        announce_dates[~mask] = NaTD
        reference_dates = dates.values.astype(datetime64D_dtype)[:, newaxis]
        return busday_count_mask_NaT(announce_dates, reference_dates)


class BusinessDaysUntilNextEvent(Factor):
    __doc__ = "\n    Abstract class for business days since a next event.\n    Returns the number of **business days** (not trading days!) until\n    the next known event date for each asset.\n\n    This doesn't use trading days because the trading calendar includes\n    information that may not have been available to the algorithm at the time\n    when `compute` is called.\n\n    For example, the NYSE closings September 11th 2001, would not have been\n    known to the algorithm on September 10th.\n\n    Assets that announced or will announce the event today will produce a value\n    of 0.0.  Assets that will announce the event on the next upcoming business\n    day will produce a value of 1.0.\n\n    Assets for which the event date is `NaT` will produce a value of `NaN`.\n    "
    window_length = 0
    dtype = float64_dtype

    def _compute(self, arrays, dates, assets, mask):
        announce_dates = arrays[0].astype(datetime64D_dtype)
        announce_dates[~mask] = NaTD
        reference_dates = dates.values.astype(datetime64D_dtype)[:, newaxis]
        return busday_count_mask_NaT(reference_dates, announce_dates)