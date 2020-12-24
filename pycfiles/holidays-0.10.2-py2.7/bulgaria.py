# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/bulgaria.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter, EASTER_ORTHODOX
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, MAR, MAY, SEP, NOV, DEC
from holidays.holiday_base import HolidayBase

class Bulgaria(HolidayBase):
    """
    Official holidays in Bulgaria in their current form. This class does not
    any return holidays before 1990, as holidays in the People's Republic of
    Bulgaria and earlier were different.

    Most holidays are fixed and if the date falls on a Saturday or a Sunday,
    the following Monday is a non-working day. The exceptions are (1) the
    Easter holidays, which are always a consecutive Friday, Saturday, and
    Sunday; and (2) the National Awakening Day which, while an official holiday
    and a non-attendance day for schools, is still a working day.

    Sources (Bulgarian):
    - http://lex.bg/laws/ldoc/1594373121
    - https://www.parliament.bg/bg/24

    Sources (English):
    - https://en.wikipedia.org/wiki/Public_holidays_in_Bulgaria
    """

    def __init__(self, **kwargs):
        self.country = 'BG'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year < 1990:
            return
        self[date(year, JAN, 1)] = 'Нова година'
        self[date(year, MAR, 3)] = 'Ден на Освобождението на България от османско иго'
        self[date(year, MAY, 1)] = 'Ден на труда и на международната работническа солидарност'
        self[date(year, MAY, 6)] = 'Гергьовден, Ден на храбростта и Българската армия'
        self[date(year, MAY, 24)] = 'Ден на българската просвета и култура и на славянската писменост'
        self[date(year, SEP, 6)] = 'Ден на Съединението'
        self[date(year, SEP, 22)] = 'Ден на Независимостта на България'
        self[date(year, NOV, 1)] = 'Ден на народните будители'
        self[date(year, DEC, 24)] = 'Бъдни вечер'
        self[date(year, DEC, 25)] = 'Рождество Христово'
        self[date(year, DEC, 26)] = 'Рождество Христово'
        self[easter(year, method=EASTER_ORTHODOX) - rd(days=2)] = 'Велики петък'
        self[easter(year, method=EASTER_ORTHODOX) - rd(days=1)] = 'Велика събота'
        self[easter(year, method=EASTER_ORTHODOX)] = 'Великден'


class BG(Bulgaria):
    pass


class BLG(Bulgaria):
    pass