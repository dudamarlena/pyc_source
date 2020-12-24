# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/hungary.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAR, APR, MAY, AUG, OCT, NOV, DEC
from holidays.constants import MON, TUE, THU, WEEKEND
from holidays.holiday_base import HolidayBase

class Hungary(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'HU'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self._add_with_observed_day_off(date(year, JAN, 1), 'Újév', since=2014)
        if 1945 <= year <= 1950 or 1989 <= year:
            self._add_with_observed_day_off(date(year, MAR, 15), 'Nemzeti ünnep')
        if 1950 <= year <= 1989:
            self[date(year, MAR, 21)] = 'A Tanácsköztársaság kikiáltásának ünnepe'
            self[date(year, APR, 4)] = 'A felszabadulás ünnepe'
            if year not in (1956, 1989):
                self[date(year, NOV, 7)] = 'A nagy októberi szocialista forradalom ünnepe'
        easter_date = easter(year)
        if 2017 <= year:
            self[easter_date + rd(weekday=FR(-1))] = 'Nagypéntek'
        self[easter_date] = 'Húsvét'
        if 1955 != year:
            self[easter_date + rd(days=1)] = 'Húsvét Hétfő'
        self[easter_date + rd(days=49)] = 'Pünkösd'
        if year <= 1952 or 1992 <= year:
            self[easter_date + rd(days=50)] = 'Pünkösdhétfő'
        if 1946 <= year:
            self._add_with_observed_day_off(date(year, MAY, 1), 'A Munka ünnepe')
        if 1950 <= year <= 1953:
            self[date(year, MAY, 2)] = 'A Munka ünnepe'
        if 1950 <= year < 1990:
            self[date(year, AUG, 20)] = 'A kenyér ünnepe'
        else:
            self._add_with_observed_day_off(date(year, AUG, 20), 'Az államalapítás ünnepe')
        if 1991 <= year:
            self._add_with_observed_day_off(date(year, OCT, 23), 'Nemzeti ünnep')
        if 1999 <= year:
            self._add_with_observed_day_off(date(year, NOV, 1), 'Mindenszentek')
        if self.observed and 2010 <= year and date(year, DEC, 24).weekday() not in WEEKEND:
            self[date(year, DEC, 24)] = 'Szenteste'
        self[date(year, DEC, 25)] = 'Karácsony'
        if 1955 != year:
            self._add_with_observed_day_off(date(year, DEC, 26), 'Karácsony másnapja', since=2013, before=False, after=True)
        if self.observed and 2014 <= year and date(year, DEC, 31).weekday() == MON:
            self[date(year, DEC, 31)] = 'Szilveszter'

    def _add_with_observed_day_off(self, day, desc, since=2010, before=True, after=True):
        self[day] = desc
        if self.observed and since <= day.year:
            if day.weekday() == TUE and before:
                self[day - rd(days=1)] = desc + ' előtti pihenőnap'
            elif day.weekday() == THU and after:
                self[day + rd(days=1)] = desc + ' utáni pihenőnap'


class HU(Hungary):
    pass


class HUN(Hungary):
    pass