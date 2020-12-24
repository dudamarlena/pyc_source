# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/russia.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from holidays.constants import JAN, FEB, MAR, MAY, JUN, NOV
from holidays.holiday_base import HolidayBase

class Russia(HolidayBase):
    """
    https://en.wikipedia.org/wiki/Public_holidays_in_Russia
    """

    def __init__(self, **kwargs):
        self.country = 'RU'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Новый год'
        self[date(year, JAN, 2)] = 'Новый год'
        self[date(year, JAN, 3)] = 'Новый год'
        self[date(year, JAN, 4)] = 'Новый год'
        self[date(year, JAN, 5)] = 'Новый год'
        self[date(year, JAN, 6)] = 'Новый год'
        self[date(year, JAN, 7)] = 'Православное Рождество'
        self[date(year, JAN, 8)] = 'Новый год'
        self[date(year, FEB, 23)] = 'День защитника отечества'
        self[date(year, MAR, 8)] = 'День женщин'
        self[date(year, MAY, 1)] = 'Праздник Весны и Труда'
        self[date(year, MAY, 9)] = 'День Победы'
        self[date(year, JUN, 12)] = 'День России'
        self[date(year, NOV, 4)] = 'День народного единства'


class RU(Russia):
    pass


class RUS(Russia):
    pass