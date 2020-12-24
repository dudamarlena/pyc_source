# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/mexico.py
# Compiled at: 2020-02-03 17:09:42
from datetime import date
from dateutil.relativedelta import relativedelta as rd, MO
from holidays.constants import FRI, SAT, SUN
from holidays.constants import JAN, FEB, MAR, MAY, SEP, NOV, DEC
from holidays.holiday_base import HolidayBase

class Mexico(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'MX'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        name = "Año Nuevo [New Year's Day]"
        self[date(year, JAN, 1)] = name
        if self.observed and date(year, JAN, 1).weekday() == SUN:
            self[date(year, JAN, 1) + rd(days=+1)] = name + ' (Observed)'
        if self.observed and date(year, DEC, 31).weekday() == FRI:
            self[date(year, DEC, 31)] = name + ' (Observed)'
        name = 'Día de la Constitución [Constitution Day]'
        if self.observed and year >= 2007:
            self[date(year, FEB, 1) + rd(weekday=MO(+1))] = name + ' (Observed)'
        if year >= 1917:
            self[date(year, FEB, 5)] = name
        name = "Natalicio de Benito Juárez [Benito Juárez's birthday]"
        if self.observed and year >= 2007:
            self[date(year, MAR, 1) + rd(weekday=MO(+3))] = name + ' (Observed)'
        if year >= 1917:
            self[date(year, MAR, 21)] = name
        if year >= 1923:
            self[date(year, MAY, 1)] = 'Día del Trabajo [Labour Day]'
            if self.observed and date(year, MAY, 1).weekday() == SAT:
                self[date(year, MAY, 1) + rd(days=-1)] = name + ' (Observed)'
            elif self.observed and date(year, MAY, 1).weekday() == SUN:
                self[date(year, MAY, 1) + rd(days=+1)] = name + ' (Observed)'
        name = 'Día de la Independencia [Independence Day]'
        self[date(year, SEP, 16)] = name
        if self.observed and date(year, SEP, 16).weekday() == SAT:
            self[date(year, SEP, 16) + rd(days=-1)] = name + ' (Observed)'
        elif self.observed and date(year, SEP, 16).weekday() == SUN:
            self[date(year, SEP, 16) + rd(days=+1)] = name + ' (Observed)'
        name = 'Día de la Revolución [Revolution Day]'
        if self.observed and year >= 2007:
            self[date(year, NOV, 1) + rd(weekday=MO(+3))] = name + ' (Observed)'
        if year >= 1917:
            self[date(year, NOV, 20)] = name
        name = 'Transmisión del Poder Ejecutivo Federal'
        name += ' [Change of Federal Government]'
        if year >= 1970 and (2096 - year) % 6 == 0:
            self[date(year, DEC, 1)] = name
            if self.observed and date(year, DEC, 1).weekday() == SAT:
                self[date(year, DEC, 1) + rd(days=-1)] = name + ' (Observed)'
            elif self.observed and date(year, DEC, 1).weekday() == SUN:
                self[date(year, DEC, 1) + rd(days=+1)] = name + ' (Observed)'
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'
        if self.observed and date(year, DEC, 25).weekday() == SAT:
            self[date(year, DEC, 25) + rd(days=-1)] = name + ' (Observed)'
        elif self.observed and date(year, DEC, 25).weekday() == SUN:
            self[date(year, DEC, 25) + rd(days=+1)] = name + ' (Observed)'


class MX(Mexico):
    pass


class MEX(Mexico):
    pass