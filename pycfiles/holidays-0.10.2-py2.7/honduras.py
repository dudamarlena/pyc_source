# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/honduras.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, TH, FR, SA, SU
from holidays.constants import JAN, FEB, MAR, APR, MAY, SEP, OCT, DEC
from holidays.holiday_base import HolidayBase

class Honduras(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'HND'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if self.observed and date(year, JAN, 1):
            self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        if self.observed and date(year, JAN, 6):
            name = 'Día de los Reyes Magos [The Three Wise Men Day] (Observed)'
            self[date(year, JAN, 6)] = name
        if self.observed and date(year, FEB, 3):
            name = 'Día de la virgen de Suyapa [Our Lady of Suyapa] (Observed)'
            self[date(year, FEB, 3)] = name
        if self.observed and date(year, MAR, 19):
            name = "Día del Padre [Father's Day] (Observed)"
            self[date(year, MAR, 19)] = name
        self[easter(year) + rd(weekday=TH(-1))] = 'Jueves Santo [Maundy Thursday]'
        self[easter(year) + rd(weekday=FR(-1))] = 'Viernes Santo [Good Friday]'
        self[easter(year) + rd(weekday=SA(-1))] = 'Sábado de Gloria [Holy Saturday]'
        self[easter(year) + rd(weekday=SU(-1))] = 'Domingo de Resurrección [Easter Sunday]'
        if self.observed and date(year, APR, 14):
            self[date(year, APR, 14)] = 'Día de las Américas [America Day]'
        if self.observed and date(year, MAY, 1):
            self[date(year, MAY, 1)] = 'Día del Trabajo [Labour Day]'
        may_first = date(int(year), 5, 1)
        weekday_seq = may_first.weekday()
        mom_day = 14 - weekday_seq
        if self.observed and date(year, MAY, mom_day):
            str_day = "Día de la madre [Mother's Day] (Observed)"
            self[date(year, MAY, mom_day)] = str_day
        if self.observed and date(year, SEP, 10):
            name = 'Día del niño [Children day] (Observed)'
            self[date(year, SEP, 10)] = name
        if self.observed and date(year, SEP, 15):
            name = 'Día de la Independencia [Independence Day]'
            self[date(year, SEP, 15)] = name
        if self.observed and date(year, SEP, 17):
            name = "Día del Maestro [Teacher's day] (Observed)"
            self[date(year, SEP, 17)] = name
        if year <= 2014:
            if self.observed and date(year, OCT, 3):
                self[date(year, OCT, 3)] = "Día de Morazán [Morazan's Day]"
            if self.observed and date(year, OCT, 12):
                self[date(year, OCT, 12)] = 'Día de la Raza [Columbus Day]'
            if self.observed and date(year, OCT, 21):
                str_day = 'Día de las Fuerzas Armadas [Army Day]'
                self[date(year, OCT, 21)] = str_day
        else:
            if self.observed and date(year, OCT, 3):
                name = 'Semana Morazánica [Morazan Weekend]'
                self[date(year, OCT, 3)] = name
            if self.observed and date(year, OCT, 4):
                name = 'Semana Morazánica [Morazan Weekend]'
                self[date(year, OCT, 4)] = name
            if self.observed and date(year, OCT, 5):
                name = 'Semana Morazánica [Morazan Weekend]'
                self[date(year, OCT, 5)] = name
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'


class HN(Honduras):
    pass


class HND(Honduras):
    pass