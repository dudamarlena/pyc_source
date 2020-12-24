# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/colombia.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, MO, TH, FR
from holidays.constants import JAN, MAR, MAY, JUN, JUL, AUG, OCT, NOV, DEC
from holidays.constants import MON, WEEKEND
from holidays.holiday_base import HolidayBase

class Colombia(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'CO'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if self.observed and date(year, JAN, 1).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        self[date(year, MAY, 1)] = 'Día del Trabajo [Labour Day]'
        name = 'Día de la Independencia [Independence Day]'
        if self.observed and date(year, JUL, 20).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JUL, 20)] = name
        self[date(year, AUG, 7)] = 'Batalla de Boyacá [Battle of Boyacá]'
        if self.observed and date(year, DEC, 8).weekday() in WEEKEND:
            pass
        else:
            self[date(year, DEC, 8)] = 'La Inmaculada Concepción [Immaculate Conception]'
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'
        name = 'Día de los Reyes Magos [Epiphany]'
        if date(year, JAN, 6).weekday() == MON or not self.observed:
            self[date(year, JAN, 6)] = name
        else:
            self[date(year, JAN, 6) + rd(weekday=MO)] = name + '(Observed)'
        name = "Día de San José [Saint Joseph's Day]"
        if date(year, MAR, 19).weekday() == MON or not self.observed:
            self[date(year, MAR, 19)] = name
        else:
            self[date(year, MAR, 19) + rd(weekday=MO)] = name + '(Observed)'
        name = 'San Pedro y San Pablo [Saint Peter and Saint Paul]'
        if date(year, JUN, 29).weekday() == MON or not self.observed:
            self[date(year, JUN, 29)] = name
        else:
            self[date(year, JUN, 29) + rd(weekday=MO)] = name + '(Observed)'
        name = 'La Asunción [Assumption of Mary]'
        if date(year, AUG, 15).weekday() == MON or not self.observed:
            self[date(year, AUG, 15)] = name
        else:
            self[date(year, AUG, 15) + rd(weekday=MO)] = name + '(Observed)'
        name = 'Descubrimiento de América [Discovery of America]'
        if date(year, OCT, 12).weekday() == MON or not self.observed:
            self[date(year, OCT, 12)] = name
        else:
            self[date(year, OCT, 12) + rd(weekday=MO)] = name + '(Observed)'
        name = "Dia de Todos los Santos [All Saint's Day]"
        if date(year, NOV, 1).weekday() == MON or not self.observed:
            self[date(year, NOV, 1)] = name
        else:
            self[date(year, NOV, 1) + rd(weekday=MO)] = name + '(Observed)'
        name = 'Independencia de Cartagena [Independence of Cartagena]'
        if date(year, NOV, 11).weekday() == MON or not self.observed:
            self[date(year, NOV, 11)] = name
        else:
            self[date(year, NOV, 11) + rd(weekday=MO)] = name + '(Observed)'
        self[easter(year) + rd(weekday=TH(-1))] = 'Jueves Santo [Maundy Thursday]'
        self[easter(year) + rd(weekday=FR(-1))] = 'Viernes Santo [Good Friday]'
        name = 'Ascensión del señor [Ascension of Jesus]'
        hdate = easter(year) + rd(days=+39)
        if hdate.weekday() == MON or not self.observed:
            self[hdate] = name
        else:
            self[hdate + rd(weekday=MO)] = name + '(Observed)'
        name = 'Corpus Christi [Corpus Christi]'
        hdate = easter(year) + rd(days=+60)
        if hdate.weekday() == MON or not self.observed:
            self[hdate] = name
        else:
            self[hdate + rd(weekday=MO)] = name + '(Observed)'
        name = 'Sagrado Corazón [Sacred Heart]'
        hdate = easter(year) + rd(days=+68)
        if hdate.weekday() == MON or not self.observed:
            self[hdate] = name
        else:
            self[hdate + rd(weekday=MO)] = name + '(Observed)'


class CO(Colombia):
    pass


class COL(Colombia):
    pass