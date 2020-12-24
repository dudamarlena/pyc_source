# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/slovakia.py
# Compiled at: 2020-01-26 19:25:31
import warnings
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, MAY, JUL, AUG, SEP, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class Slovakia(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'SK'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Deň vzniku Slovenskej republiky'
        self[date(year, JAN, 6)] = 'Zjavenie Pána (Traja králi a vianočnýsviatok pravoslávnych kresťanov)'
        e = easter(year)
        self[e - rd(days=2)] = 'Veľký piatok'
        self[e + rd(days=1)] = 'Veľkonočný pondelok'
        self[date(year, MAY, 1)] = 'Sviatok práce'
        if year >= 1997:
            self[date(year, MAY, 8)] = 'Deň víťazstva nad fašizmom'
        self[date(year, JUL, 5)] = 'Sviatok svätého Cyrila a svätého Metoda'
        self[date(year, AUG, 29)] = 'Výročie Slovenského národného povstania'
        self[date(year, SEP, 1)] = 'Deň Ústavy Slovenskej republiky'
        self[date(year, SEP, 15)] = 'Sedembolestná Panna Mária'
        if year == 2018:
            self[date(year, OCT, 30)] = '100. výročie prijatia Deklarácie slovenského národa'
        self[date(year, NOV, 1)] = 'Sviatok Všetkých svätých'
        if year >= 2001:
            self[date(year, NOV, 17)] = 'Deň boja za slobodu a demokraciu'
        self[date(year, DEC, 24)] = 'Štedrý deň'
        self[date(year, DEC, 25)] = 'Prvý sviatok vianočný'
        self[date(year, DEC, 26)] = 'Druhý sviatok vianočný'


class SK(Slovakia):
    pass


class SVK(Slovakia):
    pass


class Slovak(Slovakia):

    def __init__(self, **kwargs):
        warnings.warn('Slovak is deprecated, use Slovakia instead.', DeprecationWarning)
        super(Slovak, self).__init__(**kwargs)