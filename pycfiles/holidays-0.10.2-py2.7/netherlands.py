# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/netherlands.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, APR, MAY, AUG, DEC
from holidays.constants import SUN
from holidays.holiday_base import HolidayBase

class Netherlands(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'NL'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nieuwjaarsdag'
        easter_date = easter(year)
        self[easter_date] = 'Eerste paasdag'
        self[easter_date + rd(days=1)] = 'Tweede paasdag'
        self[easter_date + rd(days=39)] = 'Hemelvaart'
        self[easter_date + rd(days=49)] = 'Eerste Pinksterdag'
        self[easter_date + rd(days=50)] = 'Tweede Pinksterdag'
        self[date(year, DEC, 25)] = 'Eerste Kerstdag'
        self[date(year, DEC, 26)] = 'Tweede Kerstdag'
        if year >= 1945 and year % 5 == 0:
            self[date(year, MAY, 5)] = 'Bevrijdingsdag'
        if year >= 2014:
            kings_day = date(year, APR, 27)
            if kings_day.weekday() == SUN:
                kings_day = kings_day - rd(days=1)
            self[kings_day] = 'Koningsdag'
        if 1891 <= year <= 2013:
            queens_day = date(year, APR, 30)
            if year <= 1948:
                queens_day = date(year, AUG, 31)
            if queens_day.weekday() == SUN:
                if year < 1980:
                    queens_day = queens_day + rd(days=1)
                else:
                    queens_day = queens_day - rd(days=1)
            self[queens_day] = 'Koninginnedag'


class NL(Netherlands):
    pass


class NLD(Netherlands):
    pass