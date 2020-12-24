# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/czechia.py
# Compiled at: 2020-01-26 19:25:31
import warnings
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, MAY, JUL, SEP, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class Czechia(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'CZ'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Den obnovy samostatného českého státu' if year >= 2000 else 'Nový rok'
        e = easter(year)
        if year <= 1951 or year >= 2016:
            self[e - rd(days=2)] = 'Velký pátek'
        self[e + rd(days=1)] = 'Velikonoční pondělí'
        if year >= 1951:
            self[date(year, MAY, 1)] = 'Svátek práce'
        if year >= 1992:
            self[date(year, MAY, 8)] = 'Den vítězství'
        elif year >= 1947:
            self[date(year, MAY, 9)] = 'Den vítězství nad hitlerovským fašismem'
        if year >= 1951:
            self[date(year, JUL, 5)] = 'Den slovanských věrozvěstů Cyrila a Metoděje'
            self[date(year, JUL, 6)] = 'Den upálení mistra Jana Husa'
        if year >= 2000:
            self[date(year, SEP, 28)] = 'Den české státnosti'
        if year >= 1951:
            self[date(year, OCT, 28)] = 'Den vzniku samostatného československého státu'
        if year >= 1990:
            self[date(year, NOV, 17)] = 'Den boje za svobodu a demokracii'
        if year >= 1990:
            self[date(year, DEC, 24)] = 'Štědrý den'
        if year >= 1951:
            self[date(year, DEC, 25)] = '1. svátek vánoční'
            self[date(year, DEC, 26)] = '2. svátek vánoční'


class CZ(Czechia):
    pass


class CZE(Czechia):
    pass


class Czech(Czechia):

    def __init__(self, **kwargs):
        warnings.warn('Czech is deprecated, use Czechia instead.', DeprecationWarning)
        super(Czech, self).__init__(**kwargs)