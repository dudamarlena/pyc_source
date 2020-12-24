# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/vietnam.py
# Compiled at: 2020-03-28 19:45:16
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta as rd, FR, SA, MO
from holidays.constants import JAN, APR, MAY, SEP
from holidays.constants import SAT, SUN
from holidays.holiday_base import HolidayBase
from korean_lunar_calendar import KoreanLunarCalendar

class Vietnam(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'VN'
        HolidayBase.__init__(self, **kwargs)
        self.korean_cal = KoreanLunarCalendar()

    def _populate(self, year):
        name = "International New Year's Day"
        first_date = date(year, JAN, 1)
        self[first_date] = name
        if self.observed:
            self[first_date] = name
            if first_date.weekday() == SAT:
                self[first_date + rd(days=+2)] = name + ' observed'
            elif first_date.weekday() == SUN:
                self[first_date + rd(days=+1)] = name + ' observed'
        name = ['Vietnamese New Year',
         'The second day of Tet Holiday',
         'The third day of Tet Holiday',
         'The forth day of Tet Holiday',
         'The fifth day of Tet Holiday',
         "Vietnamese New Year's Eve"]
        dt = self.get_solar_date(year, 1, 1)
        new_year_date = date(dt.year, dt.month, dt.day)
        if self.observed:
            for i in range(-1, 5, 1):
                tet_day = new_year_date + rd(days=+i)
                self[tet_day] = name[i]

        if year >= 2007:
            name = 'Hung Kings Commemoration Day'
            dt = self.get_solar_date(year, 3, 10)
            king_hung_date = date(dt.year, dt.month, dt.day)
            self[king_hung_date] = name
        name = 'Liberation Day/Reunification Day'
        libration_date = date(year, APR, 30)
        self[libration_date] = name
        name = 'International Labor Day'
        labor_date = date(year, MAY, 1)
        self[labor_date] = name
        name = 'Independence Day'
        independence_date = date(year, SEP, 2)
        self[independence_date] = name

    def get_solar_date(self, year, month, day):
        self.korean_cal.setLunarDate(year, month, day, False)
        return date(self.korean_cal.solarYear, self.korean_cal.solarMonth, self.korean_cal.solarDay)


class VN(Vietnam):
    pass


class VNM(Vietnam):
    pass