# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/peru.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, TH, FR, SA, SU
from holidays.constants import JAN, MAY, JUN, JUL, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class Peru(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'PE'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        name = 'San Pedro y San Pablo [Feast of Saints Peter and Paul]'
        self[date(year, JUN, 29)] = name
        name = 'Día de la Independencia [Independence Day]'
        self[date(year, JUL, 28)] = name
        name = 'Día de las Fuerzas Armadas y la Policía del Perú'
        self[date(year, JUL, 29)] = name
        name = 'Día de Santa Rosa de Lima'
        self[date(year, AUG, 30)] = name
        name = 'Combate Naval de Angamos [Battle of Angamos]'
        self[date(year, OCT, 8)] = name
        self[easter(year) + rd(weekday=TH(-1))] = 'Jueves Santo [Maundy Thursday]'
        self[easter(year) + rd(weekday=FR(-1))] = 'Viernes Santo [Good Friday]'
        self[easter(year) + rd(weekday=SA(-1))] = 'Sábado de Gloria [Holy Saturday]'
        self[easter(year) + rd(weekday=SU(-1))] = 'Domingo de Resurrección [Easter Sunday]'
        self[date(year, MAY, 1)] = 'Día del Trabajo [Labour Day]'
        name = 'Día de Todos Los Santos [All Saints Day]'
        self[date(year, NOV, 1)] = name
        name = 'Inmaculada Concepción [Immaculate Conception]'
        self[date(year, DEC, 8)] = name
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'


class PE(Peru):
    pass


class PER(Peru):
    pass