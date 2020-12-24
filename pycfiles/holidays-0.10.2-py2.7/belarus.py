# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/belarus.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter, EASTER_ORTHODOX
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, MAR, MAY, JUL, NOV, DEC
from holidays.holiday_base import HolidayBase

class Belarus(HolidayBase):
    """
    http://president.gov.by/en/holidays_en/
    http://www.belarus.by/en/about-belarus/national-holidays
    """

    def __init__(self, **kwargs):
        self.country = 'BY'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year <= 1998:
            return
        self[date(year, JAN, 1)] = 'Новый год'
        if year >= 2020:
            self[date(year, JAN, 2)] = 'Новый год'
        self[date(year, JAN, 7)] = 'Рождество Христово (православное Рождество)'
        self[date(year, MAR, 8)] = 'День женщин'
        self[easter(year, method=EASTER_ORTHODOX) + rd(days=9)] = 'Радуница'
        self[date(year, MAY, 1)] = 'Праздник труда'
        self[date(year, MAY, 9)] = 'День Победы'
        self[date(year, JUL, 3)] = 'День Независимости Республики Беларусь (День Республики)'
        self[date(year, NOV, 7)] = 'День Октябрьской революции'
        self[date(year, DEC, 25)] = 'Рождество Христово (католическое Рождество)'


class BY(Belarus):
    pass


class BLR(Belarus):
    pass