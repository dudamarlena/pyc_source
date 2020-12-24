# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/chile.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC
from holidays.constants import WED, THU
from holidays.holiday_base import HolidayBase

class Chile(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'CL'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        name_fri = 'Semana Santa (Viernes Santo)  [Holy day (Holy Friday)]'
        name_easter = 'Día de Pascuas [Easter Day]'
        self[easter(year) + rd(weekday=FR(-1))] = name_fri
        self[easter(year)] = name_easter
        name = 'Día del Trabajo [Labour Day]'
        self[date(year, MAY, 1)] = name
        name = 'Día de las Glorias Navales [Naval Glories Day]'
        self[date(year, MAY, 21)] = name
        name = 'San Pedro y San Pablo [Saint Peter and Saint Paul]'
        self[date(year, JUN, 29)] = name
        name = 'Virgen del Carmen [Virgin of Carmen]'
        self[date(year, JUL, 16)] = name
        name = 'Asunsión de la Virgen [Assumption of the Virgin]'
        self[date(year, AUG, 15)] = name
        name = 'Día de la Independencia [Independence Day]'
        self[date(year, SEP, 18)] = name
        name = 'Día de las Glorias del Ejército de Chile [Day of Glories of the Army of Chile]'
        self[date(year, SEP, 19)] = name
        name = 'Fiestas Patrias [National Holidays]'
        if year > 2014 and date(year, SEP, 19).weekday() in [WED, THU]:
            self[date(year, SEP, 20)] = name
        if year < 2010:
            self[date(year, OCT, 12)] = 'Día de la Raza [Columbus day]'
        else:
            self[date(year, OCT, 12)] = 'Día del Respeto a la Diversidad [Day of the Meeting  of Two Worlds]'
        name = 'Día Nacional de las Iglesias Evangélicas y Protestantes  [National Day of the  Evangelical and  Protestant Churches]'
        self[date(year, OCT, 31)] = name
        name = 'Día de Todos los Santos [All Saints Day]'
        self[date(year, NOV, 1)] = name
        self[date(year, DEC, 8)] = 'La Inmaculada Concepción [Immaculate Conception]'
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'


class CL(Chile):
    pass


class CHL(Chile):
    pass