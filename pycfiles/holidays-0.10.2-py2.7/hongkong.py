# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/hongkong.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date, datetime, timedelta
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR, SA, MO
from holidays.constants import JAN, APR, MAY, JUL, SEP, OCT, DEC
from holidays.constants import MON, TUE, WED, THU, FRI, SAT, SUN
from holidays.holiday_base import HolidayBase

class HongKong(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'HK'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        day_following = 'The day following '
        name = 'The first day of January'
        first_date = date(year, JAN, 1)
        if self.observed:
            if first_date.weekday() == SUN:
                self[first_date + rd(days=+1)] = day_following + self.first_lower(name)
                first_date = first_date + rd(days=+1)
            else:
                self[first_date] = name
        else:
            self[first_date] = name
        name = "Lunar New Year's Day"
        preceding_day_lunar = "The day preceding Lunar New Year's Day"
        second_day_lunar = 'The second day of Lunar New Year'
        third_day_lunar = 'The third day of Lunar New Year'
        fourth_day_lunar = 'The fourth day of Lunar New Year'
        dt = self.get_solar_date(year, 1, 1)
        new_year_date = date(dt.year, dt.month, dt.day)
        if self.observed:
            self[new_year_date] = name
            if new_year_date.weekday() in [MON, TUE, WED, THU]:
                self[new_year_date] = name
                self[new_year_date + rd(days=+1)] = second_day_lunar
                self[new_year_date + rd(days=+2)] = third_day_lunar
            elif new_year_date.weekday() == FRI:
                self[new_year_date] = name
                self[new_year_date + rd(days=+1)] = second_day_lunar
                self[new_year_date + rd(days=+3)] = fourth_day_lunar
            elif new_year_date.weekday() == SAT:
                self[new_year_date] = name
                self[new_year_date + rd(days=+2)] = third_day_lunar
                self[new_year_date + rd(days=+3)] = fourth_day_lunar
            elif new_year_date.weekday() == SUN:
                if year in (2006, 2007, 2010):
                    self[new_year_date + rd(days=-1)] = preceding_day_lunar
                    self[new_year_date + rd(days=+1)] = second_day_lunar
                    self[new_year_date + rd(days=+2)] = third_day_lunar
                else:
                    self[new_year_date + rd(days=+1)] = second_day_lunar
                    self[new_year_date + rd(days=+2)] = third_day_lunar
                    self[new_year_date + rd(days=+3)] = fourth_day_lunar
        else:
            self[new_year_date] = name
            self[new_year_date + rd(days=+1)] = second_day_lunar
            self[new_year_date + rd(days=+2)] = third_day_lunar
        name = 'Ching Ming Festival'
        if self.isLeapYear(year) or self.isLeapYear(year - 1) and year > 2008:
            ching_ming_date = date(year, APR, 4)
        else:
            ching_ming_date = date(year, APR, 5)
        if self.observed:
            if ching_ming_date.weekday() == SUN:
                self[ching_ming_date + rd(days=+1)] = day_following + name
                ching_ming_date = ching_ming_date + rd(days=+1)
            else:
                self[ching_ming_date] = name
        else:
            self[ching_ming_date] = name
        good_friday = 'Good Friday'
        easter_monday = 'Easter Monday'
        if self.observed:
            self[easter(year) + rd(weekday=FR(-1))] = good_friday
            self[easter(year) + rd(weekday=SA(-1))] = day_following + good_friday
            if ching_ming_date == easter(year) + rd(weekday=MO):
                self[easter(year) + rd(weekday=MO) + rd(days=+1)] = day_following + easter_monday
            else:
                self[easter(year) + rd(weekday=MO)] = easter_monday
        else:
            self[easter(year) + rd(weekday=FR(-1))] = good_friday
            self[easter(year) + rd(weekday=SA(-1))] = day_following + good_friday
            self[easter(year) + rd(weekday=MO)] = easter_monday
        name = 'Birthday of the Buddha'
        dt = self.get_solar_date(year, 4, 8)
        buddha_date = date(dt.year, dt.month, dt.day)
        if self.observed:
            if buddha_date.weekday() == SUN:
                self[buddha_date + rd(days=+1)] = day_following + name
            else:
                self[buddha_date] = name
        else:
            self[buddha_date] = name
        name = 'Labour Day'
        labour_date = date(year, MAY, 1)
        if self.observed:
            if labour_date.weekday() == SUN:
                self[labour_date + rd(days=+1)] = day_following + name
            else:
                self[labour_date] = name
        else:
            self[labour_date] = name
        name = 'Tuen Ng Festival'
        dt = self.get_solar_date(year, 5, 5)
        tuen_ng_date = date(dt.year, dt.month, dt.day)
        if self.observed:
            if tuen_ng_date.weekday() == SUN:
                self[tuen_ng_date + rd(days=+1)] = day_following + name
            else:
                self[tuen_ng_date] = name
        else:
            self[tuen_ng_date] = name
        name = 'Hong Kong Special Administrative Region Establishment Day'
        hksar_date = date(year, JUL, 1)
        if self.observed:
            if hksar_date.weekday() == SUN:
                self[hksar_date + rd(days=+1)] = day_following + name
            else:
                self[hksar_date] = name
        else:
            self[hksar_date] = name
        name = 'The 70th anniversary day of the victory of the Chinese ' + "people's war of resistance against Japanese aggression"
        if year == 2015:
            self[date(year, SEP, 3)] = name
        name = 'Chinese Mid-Autumn Festival'
        dt = self.get_solar_date(year, 8, 15)
        mid_autumn_date = date(dt.year, dt.month, dt.day)
        if self.observed:
            if mid_autumn_date.weekday() == SAT:
                self[mid_autumn_date] = name
            else:
                self[mid_autumn_date + rd(days=+1)] = day_following + 'the ' + name
            mid_autumn_date = mid_autumn_date + rd(days=+1)
        else:
            self[mid_autumn_date] = name
        name = 'National Day'
        national_date = date(year, OCT, 1)
        if self.observed:
            if national_date.weekday() == SUN or national_date == mid_autumn_date:
                self[national_date + rd(days=+1)] = day_following + name
            else:
                self[national_date] = name
        else:
            self[national_date] = name
        name = 'Chung Yeung Festival'
        dt = self.get_solar_date(year, 9, 9)
        chung_yeung_date = date(dt.year, dt.month, dt.day)
        if self.observed:
            if chung_yeung_date.weekday() == SUN:
                self[chung_yeung_date + rd(days=+1)] = day_following + name
            else:
                self[chung_yeung_date] = name
        else:
            self[chung_yeung_date] = name
        name = 'Christmas Day'
        first_after_christmas = 'The first weekday after ' + name
        second_after_christmas = 'The second weekday after ' + name
        christmas_date = date(year, DEC, 25)
        if self.observed:
            if christmas_date.weekday() == SUN:
                self[christmas_date] = name
                self[christmas_date + rd(days=+1)] = first_after_christmas
                self[christmas_date + rd(days=+2)] = second_after_christmas
            elif christmas_date.weekday() == SAT:
                self[christmas_date] = name
                self[christmas_date + rd(days=+2)] = first_after_christmas
            else:
                self[christmas_date] = name
                self[christmas_date + rd(days=+1)] = first_after_christmas
        else:
            self[christmas_date] = name
            self[christmas_date + rd(days=+1)] = day_following + name

    def isLeapYear(self, year):
        if year % 4 != 0:
            return False
        else:
            if year % 100 != 0:
                return True
            if year % 400 != 0:
                return False
            return True

    def first_lower(self, s):
        return s[0].lower() + s[1:]

    g_lunar_month_days = [
     986788, 990538, 339092, 986262, 988470,
     273068, 985812, 988850, 143012, 986788,
     407114, 988746, 988310, 338262, 984410,
     985814, 136914, 990034, 473892, 990500,
     989770, 341146, 988332, 984428, 273258, 986536, 990546, 146724, 990500, 399948,
     985686, 988334, 337260, 988852, 986536,
     204178, 986770, 470310, 988454, 985686,
     398518, 988506, 985812, 276138, 989000,
     988818, 144678, 988458, 469594, 985708,
     988506, 338772, 985956, 990026, 211604,
     989844, 529706, 988462, 985772, 398698,
     988586, 986532, 269642, 990538, 986260,
     203054, 988470, 469684, 985812, 988882,
     339620, 988836, 988746, 273558, 988310,
     534870, 984410, 985818, 399058, 990034,
     989988, 277066, 989770, 668826, 988332,
     984428, 396138, 986538, 990610, 343332,
     990500, 989772, 201900, 988334, 534956,
     984756, 986538, 339346, 986770, 986406,
     272982, 985686, 988342, 142004, 985812,
     472746, 989000, 988818, 341286, 988458,
     985690, 267610, 988522, 600916, 986020,
     990026, 408212, 989844, 989482, 272988,
     985772, 988522, 142180, 986532, 400722,
     986698, 986262, 334126, 989526, 985780,
     202156, 988882, 732836, 988836, 988746,
     406678, 988310, 985430, 330422, 985946,
     988884, 145060, 989988, 473674, 989770,
     988330, 338266, 985452, 985962, 203604,
     990610, 539940, 990500, 989772, 398508,
     988334, 985516, 265642, 986794, 986770,
     204070, 986406, 469590, 985686, 988342,
     338612, 985812, 988874, 274068, 988820,
     537898, 988458, 985690, 398682, 988522,
     985940, 268106, 990026, 989844, 211242,
     989484, 471708, 985772, 988522, 338788,
     986532, 990538, 269460, 986262, 530734,
     985430, 985782, 398764, 988884, 986788,
     273994, 988746, 988438, 141622]
    START_YEAR, END_YEAR = 1901, 1900 + len(g_lunar_month_days)
    LUNAR_START_DATE, SOLAR_START_DATE = (1901, 1, 1), datetime(1901, 2, 19)
    LUNAR_END_DATE, SOLAR_END_DATE = (2099, 12, 30), datetime(2100, 2, 18)

    def get_leap_month(self, lunar_year):
        return self.g_lunar_month_days[(lunar_year - self.START_YEAR)] >> 16 & 15

    def lunar_month_days(self, lunar_year, lunar_month):
        return 29 + (self.g_lunar_month_days[(lunar_year - self.START_YEAR)] >> lunar_month & 1)

    def lunar_year_days(self, year):
        days = 0
        months_day = self.g_lunar_month_days[(year - self.START_YEAR)]
        for i in range(1, 13 if self.get_leap_month(year) == 15 else 14):
            day = 29 + (months_day >> i & 1)
            days += day

        return days

    def get_solar_date(self, year, month, day):
        span_days = 0
        for y in range(self.START_YEAR, year):
            span_days += self.lunar_year_days(y)

        leap_month = self.get_leap_month(year)
        for m in range(1, month + (month > leap_month)):
            span_days += self.lunar_month_days(year, m)

        span_days += day - 1
        return self.SOLAR_START_DATE + timedelta(span_days)


class HK(HongKong):
    pass


class HKG(HongKong):
    pass