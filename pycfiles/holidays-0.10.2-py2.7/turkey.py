# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/turkey.py
# Compiled at: 2020-01-30 17:23:45
from datetime import date
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, APR, MAY, JUL, AUG, OCT
from holidays.holiday_base import HolidayBase
from holidays.utils import get_gre_date

class Turkey(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'TR'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "New Year's Day"
        self[date(year, APR, 23)] = "National Sovereignty and Children's Day"
        self[date(year, MAY, 1)] = 'Labour Day'
        self[date(year, MAY, 19)] = 'Commemoration of Ataturk, Youth and Sports Day'
        if year > 2016:
            self[date(year, JUL, 15)] = 'Democracy and National Unity Day'
        self[date(year, AUG, 30)] = 'Victory Day'
        self[date(year, OCT, 29)] = 'Republic Day'
        for date_obs in get_gre_date(year, 10, 1):
            hol_date = date_obs
            self[hol_date] = 'Ramadan Feast'
            self[hol_date + rd(days=1)] = 'Ramadan Feast Holiday'
            self[hol_date + rd(days=2)] = 'Ramadan Feast Holiday'

        for date_obs in get_gre_date(year, 12, 10):
            hol_date = date_obs
            self[hol_date] = 'Sacrifice Feast'
            self[hol_date + rd(days=1)] = 'Sacrifice Feast Holiday'
            self[hol_date + rd(days=2)] = 'Sacrifice Feast Holiday'
            self[hol_date + rd(days=3)] = 'Sacrifice Feast Holiday'


class TR(Turkey):
    pass


class TUR(Turkey):
    pass