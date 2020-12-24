# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/poland.py
# Compiled at: 2020-01-26 19:25:31
import warnings
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, MAY, AUG, NOV, DEC
from holidays.holiday_base import HolidayBase

class Poland(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'PL'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nowy Rok'
        if year >= 2011:
            self[date(year, JAN, 6)] = 'Święto Trzech Króli'
        e = easter(year)
        self[e] = 'Niedziela Wielkanocna'
        self[e + rd(days=1)] = 'Poniedziałek Wielkanocny'
        if year >= 1950:
            self[date(year, MAY, 1)] = 'Święto Państwowe'
        if year >= 1919:
            self[date(year, MAY, 3)] = 'Święto Narodowe Trzeciego Maja'
        self[e + rd(days=49)] = 'Zielone Świątki'
        self[e + rd(days=60)] = 'Dzień Bożego Ciała'
        self[date(year, AUG, 15)] = 'Wniebowzięcie Najświętszej Marii Panny'
        self[date(year, NOV, 1)] = 'Uroczystość Wszystkich świętych'
        if 1937 <= year <= 1945 or year >= 1989:
            self[date(year, NOV, 11)] = 'Narodowe Święto Niepodległości'
        self[date(year, DEC, 25)] = 'Boże Narodzenie (pierwszy dzień)'
        self[date(year, DEC, 26)] = 'Boże Narodzenie (drugi dzień)'


class PL(Poland):
    pass


class POL(Poland):
    pass


class Polish(Poland):

    def __init__(self, **kwargs):
        warnings.warn('Polish is deprecated, use Poland instead.', DeprecationWarning)
        super(Polish, self).__init__(**kwargs)