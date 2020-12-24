# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/slovenia.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, FEB, APR, MAY, JUN, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class Slovenia(HolidayBase):
    """
    Contains all work-free public holidays in Slovenia.
    No holidays are returned before year 1991 when Slovenia became independent
    country. Before that Slovenia was part of Socialist federal republic of
    Yugoslavia.

    List of holidays (including those that are not work-free:
    https://en.wikipedia.org/wiki/Public_holidays_in_Slovenia
    """

    def __init__(self, **kwargs):
        self.country = 'SI'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year <= 1990:
            return
        if year > 1991:
            self[date(year, JAN, 1)] = 'novo leto'
            if year < 2013 or year > 2016:
                self[date(year, JAN, 2)] = 'novo leto'
            self[date(year, FEB, 8)] = 'Prešernov dan'
            easter_day = easter(year)
            self[easter_day + rd(days=1)] = 'Velikonočni ponedeljek'
            self[date(year, APR, 27)] = 'dan upora proti okupatorju'
            self[date(year, MAY, 1)] = 'praznik dela'
            self[date(year, MAY, 2)] = 'praznik dela'
            self[date(year, JUN, 25)] = 'dan državnosti'
            self[date(year, AUG, 15)] = 'Marijino vnebovzetje'
            self[date(year, OCT, 31)] = 'dan reformacije'
            self[date(year, NOV, 1)] = 'dan spomina na mrtve'
            self[date(year, DEC, 25)] = 'Božič'
            self[date(year, DEC, 26)] = 'dan samostojnosti in enotnosti'


class SI(Slovenia):
    pass


class SVN(Slovenia):
    pass