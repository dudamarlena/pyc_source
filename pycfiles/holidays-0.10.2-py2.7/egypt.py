# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/egypt.py
# Compiled at: 2020-04-13 04:40:59
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import FRI, SAT
from holidays.constants import JAN, APR, MAY, JUN, JUL, OCT
from holidays.holiday_base import HolidayBase
from holidays.utils import get_gre_date
WEEKEND = (
 FRI, SAT)

class Egypt(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'EG'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        """
        # Function to store the holiday name in the appropriate
        # date and to shift the Public holiday in case it happens
        # on a Saturday(Weekend)
        # (NOT USED)
        def is_weekend(self, hol_date, hol_name):
            if hol_date.weekday() == FRI:
                self[hol_date] = hol_name + " [Friday]"
                self[hol_date + rd(days=+2)] = "Sunday following " + hol_name
            else:
                self[hol_date] = hol_name
        """
        self[date(year, JAN, 1)] = "New Year's Day - Bank Holiday"
        self[date(year, JAN, 7)] = 'Coptic Christmas'
        if year >= 2012:
            self[date(year, JAN, 25)] = 'Revolution Day - January 25'
        else:
            if year >= 2009:
                self[date(year, JAN, 25)] = 'Police Day'
            self[easter(year, 2)] = 'Coptic Easter Sunday'
            self[easter(year, 2) + rd(days=1)] = 'Sham El Nessim'
            if year > 1982:
                self[date(year, APR, 25)] = 'Sinai Liberation Day'
            self[date(year, MAY, 1)] = 'Labour Day'
            self[date(year, OCT, 6)] = 'Armed Forces Day'
            if year >= 2014:
                self[date(year, JUN, 30)] = '30 June Revolution Day'
            if year > 1952:
                self[date(year, JUL, 23)] = 'Revolution Day'
            for date_obs in get_gre_date(year, 10, 1):
                hol_date = date_obs
                self[hol_date] = 'Eid al-Fitr'
                self[hol_date + rd(days=1)] = 'Eid al-Fitr Holiday'
                self[hol_date + rd(days=2)] = 'Eid al-Fitr Holiday'

            for date_obs in get_gre_date(year, 12, 9):
                hol_date = date_obs
                self[hol_date] = 'Arafat Day'
                self[hol_date + rd(days=1)] = 'Eid al-Adha'
                self[hol_date + rd(days=2)] = 'Eid al-Adha Holiday'
                self[hol_date + rd(days=3)] = 'Eid al-Adha Holiday'

            for date_obs in get_gre_date(year, 1, 1):
                hol_date = date_obs
                self[hol_date] = 'Islamic New Year'

            for date_obs in get_gre_date(year, 3, 12):
                hol_date = date_obs
                self[hol_date] = "Prophet Muhammad's Birthday"


class EG(Egypt):
    pass


class EGY(Egypt):
    pass