# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/singapore.py
# Compiled at: 2020-01-30 17:23:45
from datetime import date, timedelta
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, SA, FR, MO
from holidays.constants import JAN, FEB, MAR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC
from holidays.constants import SUN
from holidays.holiday_base import HolidayBase
from holidays.utils import get_gre_date

class Singapore(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'SG'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):

        def storeholiday(self, hol_date, hol_name):
            """
            Function to store the holiday name in the appropriate
            date and to implement Section 4(2) of the Holidays Act:
            'if any day specified in the Schedule falls on a Sunday,
            the day next following not being itself a public holiday
            is declared a public holiday in Singapore.'
            """
            if hol_date.weekday() == SUN:
                self[hol_date] = hol_name + ' [Sunday]'
                self[hol_date + rd(days=+1)] = 'Monday following ' + hol_name
            else:
                self[hol_date] = hol_name

        storeholiday(self, date(year, JAN, 1), "New Year's Day")
        hol_date = self.get_lunar_n_y_date(year)
        self[hol_date] = 'Chinese New Year'
        storeholiday(self, hol_date + rd(days=+1), 'Chinese New Year')
        dates_obs = {2001: [(DEC, 16)], 2002: [(DEC, 6)], 2003: [
                (
                 NOV, 25)], 
           2004: [(NOV, 14)], 2005: [(NOV, 3)], 2006: [
                (
                 OCT, 24)], 
           2007: [(OCT, 13)], 2008: [(OCT, 1)], 2009: [
                (
                 SEP, 20)], 
           2010: [(SEP, 10)], 2011: [(AUG, 30)], 2012: [
                (
                 AUG, 19)], 
           2013: [(AUG, 8)], 2014: [(JUL, 28)], 2015: [
                (
                 JUL, 17)], 
           2016: [(JUL, 6)], 2017: [(JUN, 25)], 2018: [
                (
                 JUN, 15)], 
           2019: [(JUN, 5)], 2020: [(MAY, 24)]}
        if year in dates_obs:
            for date_obs in dates_obs[year]:
                hol_date = date(year, *date_obs)
                storeholiday(self, hol_date, 'Hari Raya Puasa')

        else:
            for date_obs in self.get_hrp_date(year):
                hol_date = date_obs
                storeholiday(self, hol_date, 'Hari Raya Puasa* (*estimated)')
                if year <= 1968:
                    storeholiday(self, hol_date + rd(days=+1), 'Second day of Hari Raya Puasa* (*estimated)')

            dates_obs = {2001: [(MAR, 6)], 2002: [(FEB, 23)], 2003: [
                    (
                     FEB, 12)], 
               2004: [(FEB, 1)], 2005: [(JAN, 21)], 2006: [
                    (
                     JAN, 10)], 
               2007: [(DEC, 20)], 2008: [(DEC, 8)], 2009: [
                    (
                     NOV, 27)], 
               2010: [(NOV, 17)], 2011: [(NOV, 6)], 2012: [
                    (
                     OCT, 26)], 
               2013: [(OCT, 15)], 2014: [(OCT, 5)], 2015: [
                    (
                     SEP, 24)], 
               2016: [(SEP, 12)], 2017: [(SEP, 1)], 2018: [
                    (
                     AUG, 22)], 
               2019: [(AUG, 11)], 2020: [(JUL, 31)]}
            if year in dates_obs:
                for date_obs in dates_obs[year]:
                    hol_date = date(year, *date_obs)
                    storeholiday(self, hol_date, 'Hari Raya Haji')

            else:
                for date_obs in self.get_hrh_date(year):
                    hol_date = date_obs
                    storeholiday(self, hol_date, 'Hari Raya Haji* (*estimated)')

        if year <= 1968:
            self[easter(year) + rd(weekday=SA(-1))] = 'Holy Saturday'
        self[easter(year) + rd(weekday=FR(-1))] = 'Good Friday'
        if year <= 1968:
            self[easter(year) + rd(weekday=MO(1))] = 'Easter Monday'
        storeholiday(self, date(year, MAY, 1), 'Labour Day')
        dates_obs = {2001: (MAY, 7), 2002: (MAY, 27), 2003: (
                MAY, 15), 
           2004: (JUN, 2), 2005: (MAY, 23), 2006: (
                MAY, 12), 
           2007: (MAY, 31), 2008: (MAY, 19), 2009: (
                MAY, 9), 
           2010: (MAY, 28), 2011: (MAY, 17), 2012: (
                MAY, 5), 
           2013: (MAY, 24), 2014: (MAY, 13), 2015: (
                JUN, 1), 
           2016: (MAY, 20), 2017: (MAY, 10), 2018: (
                MAY, 29), 
           2019: (MAY, 19), 2020: (MAY, 7)}
        if year in dates_obs:
            hol_date = date(year, *dates_obs[year])
            storeholiday(self, hol_date, 'Vesak Day')
        else:
            storeholiday(self, self.get_vesak_date(year), 'Vesak Day* (*estimated; ~10% chance +/- 1 day)')
        storeholiday(self, date(year, AUG, 9), 'National Day')
        dates_obs = {2001: (NOV, 14), 2002: (NOV, 3), 2003: (
                OCT, 23), 
           2004: (NOV, 11), 2005: (NOV, 1), 2006: (
                OCT, 21), 
           2007: (NOV, 8), 2008: (OCT, 27), 2009: (
                OCT, 17), 
           2010: (NOV, 5), 2011: (OCT, 26), 2012: (
                NOV, 13), 
           2013: (NOV, 2), 2014: (OCT, 22), 2015: (
                NOV, 10), 
           2016: (OCT, 29), 2017: (OCT, 18), 2018: (
                NOV, 6), 
           2019: (OCT, 27), 2020: (NOV, 14)}
        if year in dates_obs:
            hol_date = date(year, *dates_obs[year])
            storeholiday(self, hol_date, 'Deepavali')
        else:
            storeholiday(self, self.get_s_diwali_date(year), 'Deepavali* (*estimated; rarely on day after)')
        storeholiday(self, date(year, DEC, 25), 'Christmas Day')
        if year <= 1968:
            storeholiday(self, date(year, DEC, 26), 'Boxing Day')
        dates_obs = {2001: (NOV, 3), 2006: (MAY, 6), 2011: (
                MAY, 7), 
           2015: (SEP, 11)}
        if year in dates_obs:
            self[date(year, *dates_obs[year])] = 'Polling Day'
        if year == 2015:
            self[date(2015, AUG, 7)] = 'SG50 Public Holiday'

    g_lunar_month_days = [
     986788, 990538, 339092, 986262, 988470,
     273068, 985812, 988850, 143012, 986788,
     407114, 988746, 988310, 338262, 984410,
     985814, 136914, 990034, 473892, 990500,
     989770, 341146, 988332, 984428, 273258,
     986536, 990546, 146724, 990500, 399948,
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
    LUNAR_START_DATE, SOLAR_START_DATE = (1901, 1, 1), date(1901, 2, 19)
    LUNAR_END_DATE, SOLAR_END_DATE = (2099, 12, 30), date(2100, 2, 18)

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

    def get_lunar_n_y_date(self, year):
        span_days = 0
        for y in range(self.START_YEAR, year):
            span_days += self.lunar_year_days(y)

        return self.SOLAR_START_DATE + timedelta(span_days)

    def get_vesak_date(self, year):
        span_days = 0
        for y in range(self.START_YEAR, year):
            span_days += self.lunar_year_days(y)

        leap_month = self.get_leap_month(year)
        for m in range(1, 4 + (4 > leap_month)):
            span_days += self.lunar_month_days(year, m)

        span_days += 14
        return self.SOLAR_START_DATE + timedelta(span_days)

    def get_s_diwali_date(self, year):
        span_days = 0
        for y in range(self.START_YEAR, year):
            span_days += self.lunar_year_days(y)

        leap_month = self.get_leap_month(year)
        for m in range(1, 10 + (10 > leap_month)):
            span_days += self.lunar_month_days(year, m)

        span_days -= 2
        return self.SOLAR_START_DATE + timedelta(span_days)

    def get_hrp_date(self, year):
        return get_gre_date(year, 10, 1)

    def get_hrh_date(self, year):
        return get_gre_date(year, 12, 10)


class SG(Singapore):
    pass


class SGP(Singapore):
    pass