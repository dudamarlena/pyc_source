# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/dominican_republic.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, MO, FR
from holidays.constants import JAN, FEB, MAY, JUN, AUG, SEP, NOV, DEC
from holidays.holiday_base import HolidayBase

class DominicanRepublic(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'DO'
        HolidayBase.__init__(self, **kwargs)

    @staticmethod
    def __change_day_by_law(holiday, latest_days=(3, 4)):
        if holiday >= date(1997, 6, 27):
            if holiday.weekday() in (1, 2):
                holiday -= rd(weekday=MO(-1))
            elif holiday.weekday() in latest_days:
                holiday += rd(weekday=MO(1))
        return holiday

    def _populate(self, year):
        self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        epiphany_day = self.__change_day_by_law(date(year, JAN, 6))
        self[epiphany_day] = 'Día de los Santos Reyes [Epiphany]'
        self[date(year, JAN, 21)] = 'Día de la Altagracia [Lady of Altagracia]'
        duarte_day = self.__change_day_by_law(date(year, JAN, 26))
        self[duarte_day] = 'Día de Duarte [Juan Pablo Duarte Day]'
        self[date(year, FEB, 27)] = 'Día de Independencia [Independence Day]'
        self[easter(year) + rd(weekday=FR(-1))] = 'Viernes Santo [Good Friday]'
        labor_day = self.__change_day_by_law(date(year, MAY, 1), (3, 4, 6))
        self[labor_day] = 'Día del Trabajo [Labor Day]'
        self[date(year, JUN, 11)] = 'Corpus Christi [Feast of Corpus Christi]'
        restoration_day = date(year, AUG, 16) if (year - 2000) % 4 == 0 and year < 2008 else self.__change_day_by_law(date(year, AUG, 16))
        self[restoration_day] = 'Día de la Restauración [Restoration Day]'
        self[date(year, SEP, 24)] = 'Día de las Mercedes             [Our Lady of Mercedes Day]'
        constitution_day = self.__change_day_by_law(date(year, NOV, 6))
        self[constitution_day] = 'Día de la Constitución [Constitution Day]'
        self[date(year, DEC, 25)] = 'Día de Navidad [Christmas Day]'


class DO(DominicanRepublic):
    pass


class DOM(DominicanRepublic):
    pass