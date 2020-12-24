# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/korea.py
# Compiled at: 2020-03-28 19:45:08
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta as rd, FR, SA, MO
from holidays.constants import JAN, MAR, APR, MAY, JUN, JUL, AUG, OCT, DEC
from holidays.constants import MON, TUE, WED, THU, FRI, SAT, SUN
from holidays.holiday_base import HolidayBase
from korean_lunar_calendar import KoreanLunarCalendar

class Korea(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'KR'
        HolidayBase.__init__(self, **kwargs)
        self.korean_cal = KoreanLunarCalendar()

    def _populate(self, year):
        alt_holiday = 'Alternative holiday of '
        name = "New Year's Day"
        first_date = date(year, JAN, 1)
        if self.observed:
            self[first_date] = name
            if first_date.weekday() == SUN:
                self[first_date + rd(days=+1)] = alt_holiday + self.first_lower(name)
                first_date = first_date + rd(days=+1)
            else:
                self[first_date] = name
        else:
            self[first_date] = name
        name = "Lunar New Year's Day"
        preceding_day_lunar = 'The day preceding of ' + name
        second_day_lunar = 'The second day of ' + name
        dt = self.get_solar_date(year, 1, 1)
        new_year_date = date(dt.year, dt.month, dt.day)
        if self.observed and year >= 2015:
            if new_year_date.weekday() in [TUE, WED, THU, FRI]:
                self[new_year_date + rd(days=-1)] = preceding_day_lunar
                self[new_year_date] = name
                self[new_year_date + rd(days=+1)] = second_day_lunar
            elif new_year_date.weekday() in [SAT, SUN, MON]:
                self[new_year_date + rd(days=-1)] = preceding_day_lunar
                self[new_year_date] = name
                self[new_year_date + rd(days=+1)] = second_day_lunar
                self[new_year_date + rd(days=+2)] = alt_holiday + name
        else:
            self[new_year_date + rd(days=-1)] = preceding_day_lunar
            self[new_year_date] = name
            self[new_year_date + rd(days=+1)] = second_day_lunar
        name = 'Independence Movement Day'
        independence_date = date(year, MAR, 1)
        if self.observed and year >= 2015:
            if independence_date.weekday() == SUN:
                self[independence_date] = name
                self[independence_date + rd(days=+1)] = alt_holiday + name
            else:
                self[independence_date] = name
        else:
            self[independence_date] = name
        name = 'Tree Planting Day'
        planting_date = date(year, APR, 5)
        if self.observed and year >= 1949 and year <= 2007 and year != 1960:
            self[planting_date] = name
        name = 'Birthday of the Buddha'
        dt = self.get_solar_date(year, 4, 8)
        buddha_date = date(dt.year, dt.month, dt.day)
        self[buddha_date] = name
        name = "Children's Day"
        childrens_date = date(year, MAY, 5)
        if year >= 1975:
            self[childrens_date] = name
            if self.observed and year >= 2015:
                if childrens_date.weekday() == SUN:
                    self[childrens_date + rd(days=+1)] = alt_holiday + name
                if childrens_date.weekday() == SAT:
                    self[childrens_date + rd(days=+2)] = alt_holiday + name
                if self[childrens_date] != name:
                    self[childrens_date + rd(days=+1)] = alt_holiday + name
        name = 'Labour Day'
        labour_date = date(year, MAY, 1)
        self[labour_date] = name
        name = 'Memorial Day'
        memorial_date = date(year, JUN, 6)
        self[memorial_date] = name
        name = 'Constitution Day'
        constitution_date = date(year, JUL, 17)
        if self.observed and year >= 1948 and year <= 2007:
            self[constitution_date] = name
        name = 'Liberation Day'
        libration_date = date(year, AUG, 15)
        if self.observed and year >= 1945:
            self[libration_date] = name
        name = 'Chuseok'
        preceding_day_chuseok = 'The day preceding of ' + name
        second_day_chuseok = 'The second day of ' + name
        dt = self.get_solar_date(year, 8, 15)
        new_year_date = date(dt.year, dt.month, dt.day)
        if self.observed and year >= 2014:
            if new_year_date.weekday() in [TUE, WED, THU, FRI]:
                self[new_year_date + rd(days=-1)] = preceding_day_chuseok
                self[new_year_date] = name
                self[new_year_date + rd(days=+1)] = second_day_chuseok
            elif new_year_date.weekday() in [SAT, SUN, MON]:
                self[new_year_date + rd(days=-1)] = preceding_day_chuseok
                self[new_year_date] = name
                self[new_year_date + rd(days=+1)] = second_day_chuseok
                self[new_year_date + rd(days=+2)] = alt_holiday + name
        else:
            self[new_year_date + rd(days=-1)] = preceding_day_chuseok
            self[new_year_date] = name
            self[new_year_date + rd(days=+1)] = second_day_chuseok
        name = 'National Foundation Day'
        foundation_date = date(year, OCT, 3)
        self[foundation_date] = name
        name = 'Hangeul Day'
        hangeul_date = date(year, OCT, 9)
        self[hangeul_date] = name
        name = 'Christmas Day'
        christmas_date = date(year, DEC, 25)
        self[christmas_date] = name

    def get_solar_date(self, year, month, day):
        self.korean_cal.setLunarDate(year, month, day, False)
        return date(self.korean_cal.solarYear, self.korean_cal.solarMonth, self.korean_cal.solarDay)

    def first_lower(self, s):
        return s[0].lower() + s[1:]


class KR(Korea):
    pass


class KOR(Korea):
    pass