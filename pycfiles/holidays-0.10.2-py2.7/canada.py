# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/canada.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, MO, SU, FR
from holidays.constants import FRI, SAT, SUN, WEEKEND
from holidays.constants import JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class Canada(HolidayBase):
    PROVINCES = [
     'AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE',
     'QC', 'SK', 'YT']

    def __init__(self, **kwargs):
        self.country = 'CA'
        self.prov = kwargs.pop('prov', 'ON')
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year >= 1867:
            name = "New Year's Day"
            self[date(year, JAN, 1)] = name
            if self.observed and date(year, JAN, 1).weekday() == SUN:
                self[date(year, JAN, 1) + rd(days=+1)] = name + ' (Observed)'
            elif self.observed and date(year, JAN, 1).weekday() == SAT:
                expand = self.expand
                self.expand = False
                self[date(year, JAN, 1) + rd(days=-1)] = name + ' (Observed)'
                self.expand = expand
            if self.observed and date(year, DEC, 31).weekday() == FRI:
                self[date(year, DEC, 31)] = name + ' (Observed)'
        if self.prov in ('AB', 'SK', 'ON') and year >= 2008:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Family Day'
        elif self.prov in ('AB', 'SK') and year >= 2007:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Family Day'
        elif self.prov == 'AB' and year >= 1990:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Family Day'
        elif self.prov == 'NB' and year >= 2018:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Family Day'
        elif self.prov == 'BC':
            if year >= 2013 and year <= 2018:
                self[date(year, FEB, 1) + rd(weekday=MO(+2))] = 'Family Day'
            elif year > 2018:
                self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Family Day'
        elif self.prov == 'MB' and year >= 2008:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Louis Riel Day'
        elif self.prov == 'PE' and year >= 2010:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Islander Day'
        elif self.prov == 'PE' and year == 2009:
            self[date(year, FEB, 1) + rd(weekday=MO(+2))] = 'Islander Day'
        elif self.prov == 'NS' and year >= 2015:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Heritage Day'
        elif self.prov == 'YT':
            dt = date(year, MAR, 1) + rd(weekday=SU(-1)) + rd(weekday=FR(-1))
            self[dt] = 'Heritage Day'
        if self.prov == 'NL' and year >= 1900:
            dt = date(year, MAR, 17)
            dt1 = date(year, MAR, 17) + rd(weekday=MO(-1))
            dt2 = date(year, MAR, 17) + rd(weekday=MO(+1))
            if dt2 - dt <= dt - dt1:
                self[dt2] = "St. Patrick's Day"
            else:
                self[dt1] = "St. Patrick's Day"
        if self.prov != 'QC' and year >= 1867:
            self[easter(year) + rd(weekday=FR(-1))] = 'Good Friday'
        if self.prov == 'QC' and year >= 1867:
            self[easter(year) + rd(weekday=MO)] = 'Easter Monday'
        if self.prov == 'NL' and year == 2010:
            self[date(2010, 4, 19)] = "St. George's Day"
        elif self.prov == 'NL' and year >= 1990:
            dt = date(year, APR, 23)
            dt1 = dt + rd(weekday=MO(-1))
            dt2 = dt + rd(weekday=MO(+1))
            if dt2 - dt < dt - dt1:
                self[dt2] = "St. George's Day"
            else:
                self[dt1] = "St. George's Day"
        if self.prov not in ('NB', 'NS', 'PE', 'NL', 'QC') and year >= 1953:
            self[date(year, MAY, 24) + rd(weekday=MO(-1))] = 'Victoria Day'
        elif self.prov == 'QC' and year >= 1953:
            name = "National Patriots' Day"
            self[date(year, MAY, 24) + rd(weekday=MO(-1))] = name
        if self.prov == 'NT' and year >= 1996:
            self[date(year, JUN, 21)] = 'National Aboriginal Day'
        if self.prov == 'QC' and year >= 1925:
            self[date(year, JUN, 24)] = 'St. Jean Baptiste Day'
            if self.observed and date(year, JUN, 24).weekday() == SUN:
                self[date(year, JUN, 25)] = 'St. Jean Baptiste Day (Observed)'
        if self.prov == 'NL' and year >= 1997:
            dt = date(year, JUN, 24)
            dt1 = dt + rd(weekday=MO(-1))
            dt2 = dt + rd(weekday=MO(+1))
            if dt2 - dt <= dt - dt1:
                self[dt2] = 'Discovery Day'
            else:
                self[dt1] = 'Discovery Day'
        elif self.prov == 'YT' and year >= 1912:
            self[date(year, AUG, 1) + rd(weekday=MO(+3))] = 'Discovery Day'
        if self.prov != 'NL' and year >= 1867:
            if year >= 1983:
                name = 'Canada Day'
            else:
                name = 'Dominion Day'
            self[date(year, JUL, 1)] = name
            if year >= 1879 and self.observed and date(year, JUL, 1).weekday() in WEEKEND:
                self[date(year, JUL, 1) + rd(weekday=MO)] = name + ' (Observed)'
        elif year >= 1867:
            if year >= 1983:
                name = 'Memorial Day'
            else:
                name = 'Dominion Day'
            self[date(year, JUL, 1)] = name
            if year >= 1879 and self.observed and date(year, JUL, 1).weekday() in WEEKEND:
                self[date(year, JUL, 1) + rd(weekday=MO)] = name + ' (Observed)'
        if self.prov == 'NU' and year >= 2001:
            self[date(year, JUL, 9)] = 'Nunavut Day'
            if self.observed and date(year, JUL, 9).weekday() == SUN:
                self[date(year, JUL, 10)] = 'Nunavut Day (Observed)'
        elif self.prov == 'NU' and year == 2000:
            self[date(2000, 4, 1)] = 'Nunavut Day'
        if self.prov in ('ON', 'MB', 'NT') and year >= 1900:
            self[date(year, AUG, 1) + rd(weekday=MO)] = 'Civic Holiday'
        elif self.prov == 'AB' and year >= 1974:
            self[date(year, AUG, 1) + rd(weekday=MO)] = 'Heritage Day'
        elif self.prov == 'BC' and year >= 1974:
            self[date(year, AUG, 1) + rd(weekday=MO)] = 'British Columbia Day'
        elif self.prov == 'NB' and year >= 1900:
            self[date(year, AUG, 1) + rd(weekday=MO)] = 'New Brunswick Day'
        elif self.prov == 'SK' and year >= 1900:
            self[date(year, AUG, 1) + rd(weekday=MO)] = 'Saskatchewan Day'
        if year >= 1894:
            self[date(year, SEP, 1) + rd(weekday=MO)] = 'Labour Day'
        if self.prov not in ('NB', 'NS', 'PE', 'NL') and year >= 1931:
            if year == 1935:
                self[date(1935, 10, 25)] = 'Thanksgiving'
            else:
                self[date(year, OCT, 1) + rd(weekday=MO(+2))] = 'Thanksgiving'
        name = 'Remembrance Day'
        provinces = ('ON', 'QC', 'NS', 'NL', 'NT', 'PE', 'SK')
        if self.prov not in provinces and year >= 1931:
            self[date(year, NOV, 11)] = name
        elif self.prov in ('NS', 'NL', 'NT', 'PE', 'SK') and year >= 1931:
            self[date(year, NOV, 11)] = name
            if self.observed and date(year, NOV, 11).weekday() == SUN:
                name = name + ' (Observed)'
                self[date(year, NOV, 11) + rd(weekday=MO)] = name
        if year >= 1867:
            self[date(year, DEC, 25)] = 'Christmas Day'
            if self.observed and date(year, DEC, 25).weekday() == SAT:
                self[date(year, DEC, 24)] = 'Christmas Day (Observed)'
            elif self.observed and date(year, DEC, 25).weekday() == SUN:
                self[date(year, DEC, 26)] = 'Christmas Day (Observed)'
        if year >= 1867:
            name = 'Boxing Day'
            name_observed = name + ' (Observed)'
            if self.observed and date(year, DEC, 26).weekday() in WEEKEND:
                self[date(year, DEC, 26) + rd(weekday=MO)] = name_observed
            elif self.observed and date(year, DEC, 26).weekday() == 0:
                self[date(year, DEC, 27)] = name_observed
            else:
                self[date(year, DEC, 26)] = name


class CA(Canada):
    pass


class CAN(Canada):
    pass