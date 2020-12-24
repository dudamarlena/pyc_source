# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/israel.py
# Compiled at: 2020-01-26 19:25:31
from convertdate import hebrew
from datetime import date
from dateutil.relativedelta import relativedelta as rd
from holidays.holiday_base import HolidayBase

class Israel(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'IL'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        is_leap_year = hebrew.leap(year + hebrew.HEBREW_YEAR_OFFSET)
        name = 'Passover I'
        year, month, day = hebrew.to_jd_gregorianyear(year, hebrew.NISAN, 14)
        passover_start_dt = date(year, month, day)
        self[passover_start_dt] = name + ' - Eve'
        self[passover_start_dt + rd(days=1)] = name
        name = 'Passover'
        for offset in range(2, 6):
            self[passover_start_dt + rd(days=offset)] = name + ' - Chol HaMoed'

        name = 'Passover VII'
        self[passover_start_dt + rd(days=6)] = name + ' - Eve'
        self[passover_start_dt + rd(days=7)] = name
        name = 'Memorial Day'
        year, month, day = hebrew.to_jd_gregorianyear(year, hebrew.IYYAR, 3)
        self[date(year, month, day) + rd(days=1)] = name
        observed_delta = 0
        if self.observed:
            day_in_week = date(year, month, day).weekday()
            if day_in_week in (2, 3):
                observed_delta = -(day_in_week - 1)
            elif 2004 <= year and day_in_week == 5:
                observed_delta = 1
            if observed_delta != 0:
                self[date(year, month, day) + rd(days=observed_delta + 1)] = name + ' (Observed)'
        name = 'Independence Day'
        year, month, day = hebrew.to_jd_gregorianyear(year, hebrew.IYYAR, 4)
        self[date(year, month, day) + rd(days=1)] = name
        if self.observed and observed_delta != 0:
            self[date(year, month, day) + rd(days=observed_delta + 1)] = name + ' (Observed)'
        name = "Lag B'Omer"
        year, month, day = hebrew.to_jd_gregorianyear(year, hebrew.IYYAR, 18)
        self[date(year, month, day)] = name
        name = 'Shavuot'
        year, month, day = hebrew.to_jd_gregorianyear(year, hebrew.SIVAN, 5)
        self[date(year, month, day)] = name + ' - Eve'
        self[date(year, month, day) + rd(days=1)] = name
        name = 'Rosh Hashanah'
        year, month, day = hebrew.to_jd_gregorianyear(year, hebrew.ELUL, 29)
        self[date(year, month, day)] = name + ' - Eve'
        self[date(year, month, day) + rd(days=1)] = name
        self[date(year, month, day) + rd(days=2)] = name
        name = 'Yom Kippur'
        year, month, day = hebrew.to_jd_gregorianyear(year, hebrew.TISHRI, 9)
        self[date(year, month, day)] = name + ' - Eve'
        self[date(year, month, day) + rd(days=1)] = name
        name = 'Sukkot I'
        year, month, day = hebrew.to_jd_gregorianyear(year, hebrew.TISHRI, 14)
        sukkot_start_dt = date(year, month, day)
        self[sukkot_start_dt] = name + ' - Eve'
        self[sukkot_start_dt + rd(days=1)] = name
        name = 'Sukkot'
        for offset in range(2, 7):
            self[sukkot_start_dt + rd(days=offset)] = name + ' - Chol HaMoed'

        name = 'Sukkot VII'
        self[sukkot_start_dt + rd(days=7)] = name + ' - Eve'
        self[sukkot_start_dt + rd(days=8)] = name
        name = 'Hanukkah'
        year, month, day = hebrew.to_jd_gregorianyear(year, hebrew.KISLEV, 25)
        for offset in range(8):
            self[date(year, month, day) + rd(days=offset)] = name

        name = 'Purim'
        heb_month = hebrew.VEADAR if is_leap_year else hebrew.ADAR
        year, month, day = hebrew.to_jd_gregorianyear(year, heb_month, 14)
        self[date(year, month, day)] = name
        self[date(year, month, day) - rd(days=1)] = name + ' - Eve'
        name = 'Shushan Purim'
        self[date(year, month, day) + rd(days=1)] = name


class IL(Israel):
    pass


class ISR(Israel):
    pass