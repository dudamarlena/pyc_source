# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/seasonal/common.py
# Compiled at: 2019-04-10 20:10:26
# Size of source mod 2**32: 3693 bytes
import numpy as np, pandas as pd
from enum import Enum
from pyFTS.common import FuzzySet, Membership
from pyFTS.partitioners import partitioner, Grid
from datetime import date as dt, datetime as dtm

class DateTime(Enum):
    __doc__ = '\n    Data and Time granularity for time granularity and seasonality identification\n    '
    year = 1
    half = 2
    third = 3
    quarter = 4
    sixth = 6
    month = 12
    day_of_month = 30
    day_of_year = 364
    day_of_week = 7
    hour = 24
    minute = 60
    second = 60
    hour_of_day = 24
    hour_of_week = 168
    hour_of_month = 744
    hour_of_year = 8736
    minute_of_hour = 60
    minute_of_day = 1440
    minute_of_week = 10080
    minute_of_month = 44640
    minute_of_year = 524160
    second_of_minute = 60.00001
    second_of_hour = 3600
    second_of_day = 86400


def strip_datepart(date, date_part, mask=''):
    if isinstance(date, str):
        date = dtm.strptime(date, mask)
    else:
        if date_part == DateTime.year:
            tmp = date.year
        else:
            if date_part == DateTime.month:
                tmp = date.month
            else:
                if date_part in (DateTime.half, DateTime.third, DateTime.quarter, DateTime.sixth):
                    tmp = date.month // date_part.value + 1
                else:
                    if date_part == DateTime.day_of_year:
                        tmp = date.timetuple().tm_yday
                    else:
                        if date_part == DateTime.day_of_month:
                            tmp = date.day
                        else:
                            if date_part == DateTime.day_of_week:
                                tmp = date.weekday()
                            else:
                                if date_part == DateTime.hour or date_part == DateTime.hour_of_day:
                                    tmp = date.hour
                                else:
                                    if date_part == DateTime.hour_of_week:
                                        wk = (date.weekday() - 1) * 24
                                        tmp = date.hour + wk
                                    else:
                                        if date_part == DateTime.hour_of_month:
                                            wk = (date.day - 1) * 24
                                            tmp = date.hour + wk
                                        else:
                                            if date_part == DateTime.hour_of_year:
                                                wk = (date.timetuple().tm_yday - 1) * 24
                                                tmp = date.hour + wk
                                            else:
                                                if date_part == DateTime.minute or date_part == DateTime.minute_of_hour:
                                                    tmp = date.minute
                                                else:
                                                    if date_part == DateTime.minute_of_day:
                                                        wk = date.hour * 60
                                                        tmp = date.minute + wk
                                                    else:
                                                        if date_part == DateTime.minute_of_week:
                                                            wk1 = (date.weekday() - 1) * 1440
                                                            wk2 = date.hour * 60
                                                            tmp = date.minute + wk1 + wk2
                                                        else:
                                                            if date_part == DateTime.minute_of_month:
                                                                wk1 = (date.day - 1) * 1440
                                                                wk2 = date.hour * 60
                                                                tmp = date.minute + wk1 + wk2
                                                            else:
                                                                if date_part == DateTime.minute_of_year:
                                                                    wk1 = (date.timetuple().tm_yday - 1) * 1440
                                                                    wk2 = date.hour * 60
                                                                    tmp = date.minute + wk1 + wk2
                                                                else:
                                                                    if date_part == DateTime.second or date_part == DateTime.second_of_minute:
                                                                        tmp = date.second
                                                                    else:
                                                                        if date_part == DateTime.second_of_hour:
                                                                            wk1 = date.minute * 60
                                                                            tmp = date.second + wk1
                                                                        else:
                                                                            if date_part == DateTime.second_of_day:
                                                                                wk1 = date.hour * 3600
                                                                                wk2 = date.minute * 60
                                                                                tmp = date.second + wk1 + wk2
                                                                            else:
                                                                                raise Exception('Unknown DateTime value!')
    return tmp


class FuzzySet(FuzzySet.FuzzySet):
    __doc__ = '\n    Temporal/Seasonal Fuzzy Set\n    '

    def __init__(self, datepart, name, mf, parameters, centroid, alpha=1.0, **kwargs):
        (super(FuzzySet, self).__init__)(name, mf, parameters, centroid, alpha, **kwargs)
        self.datepart = datepart
        self.type = kwargs.get('type', 'seasonal')

    def transform(self, x):
        if self.type == 'seasonal':
            if isinstance(x, (dt, pd.Timestamp)):
                dp = strip_datepart(x, self.datepart)
        else:
            dp = x
        return dp