# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/argentina.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR, TH
from holidays.constants import WEEKEND
from holidays.constants import JAN, MAR, APR, MAY, JUN, JUL, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class Argentina(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'AR'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if not self.observed and date(year, JAN, 1).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        name = "Día de Carnaval [Carnival's Day]"
        self[easter(year) - rd(days=48)] = name
        self[easter(year) - rd(days=47)] = name
        name = "Día Nacional de la Memoria por la Verdad y la Justicia [Memory's National Day for the Truth and Justice]"
        if not self.observed and date(year, MAR, 24).weekday() in WEEKEND:
            pass
        else:
            self[date(year, MAR, 24)] = name
        name_thu = 'Semana Santa (Jueves Santo)  [Holy day (Holy Thursday)]'
        name_fri = 'Semana Santa (Viernes Santo)  [Holy day (Holy Friday)]'
        name_easter = 'Día de Pascuas [Easter Day]'
        self[easter(year) + rd(weekday=TH(-1))] = name_thu
        self[easter(year) + rd(weekday=FR(-1))] = name_fri
        if not self.observed and easter(year).weekday() in WEEKEND:
            pass
        else:
            self[easter(year)] = name_easter
        if not self.observed and date(year, APR, 2).weekday() in WEEKEND:
            pass
        else:
            self[date(year, APR, 2)] = 'Día del Veterano y de los Caidos en la Guerra de Malvinas [Veterans Day and the Fallen in the Malvinas War]'
        name = 'Día del Trabajo [Labour Day]'
        if not self.observed and date(year, MAY, 1).weekday() in WEEKEND:
            pass
        else:
            self[date(year, MAY, 1)] = name
        name = 'Día de la Revolucion de Mayo [May Revolution Day]'
        if not self.observed and date(year, MAY, 25).weekday() in WEEKEND:
            pass
        else:
            self[date(year, MAY, 25)] = name
        name = 'Día Pase a la Inmortalidad del General Martín Miguel de Güemes [Day Pass to the Immortality of General Martín Miguel de Güemes]'
        if not self.observed and date(year, JUN, 17).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JUN, 17)] = name
        name = 'Día Pase a la Inmortalidad del General D. Manuel Belgrano [Day Pass to the Immortality of General D. Manuel Belgrano]'
        if not self.observed and date(year, JUN, 20).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JUN, 20)] = name
        name = 'Día de la Independencia [Independence Day]'
        if not self.observed and date(year, JUL, 9).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JUL, 9)] = name
        name = 'Día Pase a la Inmortalidad del General D. José de San Martin [Day Pass to the Immortality of General D. José de San Martin]'
        if not self.observed and date(year, AUG, 17).weekday() in WEEKEND:
            pass
        else:
            self[date(year, AUG, 17)] = name
        if not self.observed and date(year, OCT, 12).weekday() in WEEKEND:
            pass
        elif year < 2010:
            self[date(year, OCT, 12)] = 'Día de la Raza [Columbus day]'
        else:
            self[date(year, OCT, 12)] = 'Día del Respeto a la Diversidad Cultural [Respect for Cultural Diversity Day]'
        name = 'Día Nacional de la Soberanía [National Sovereignty Day]'
        if not self.observed and date(year, NOV, 20).weekday() in WEEKEND:
            pass
        elif year >= 2010:
            self[date(year, NOV, 20)] = name
        if not self.observed and date(year, DEC, 8).weekday() in WEEKEND:
            pass
        else:
            self[date(year, DEC, 8)] = 'La Inmaculada Concepción [Immaculate Conception]'
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'


class AR(Argentina):
    pass


class ARG(Argentina):
    pass