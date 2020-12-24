# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/united_kingdom.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, MO, FR
from holidays.constants import JAN, MAR, APR, MAY, JUN, JUL, AUG, OCT, NOV, DEC
from holidays.constants import MON, TUE, WED, THU, FRI, SAT, SUN, WEEKEND
from holidays.holiday_base import HolidayBase

class UnitedKingdom(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'UK'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year >= 1974:
            name = "New Year's Day"
            self[date(year, JAN, 1)] = name
            if self.observed and date(year, JAN, 1).weekday() == SUN:
                self[date(year, JAN, 1) + rd(days=+1)] = name + ' (Observed)'
            elif self.observed and date(year, JAN, 1).weekday() == SAT:
                self[date(year, JAN, 1) + rd(days=+2)] = name + ' (Observed)'
        if self.country in ('UK', 'Scotland'):
            name = 'New Year Holiday'
            if self.country == 'UK':
                name += ' [Scotland]'
            self[date(year, JAN, 2)] = name
            if self.observed and date(year, JAN, 2).weekday() in WEEKEND:
                self[date(year, JAN, 2) + rd(days=+2)] = name + ' (Observed)'
            elif self.observed and date(year, JAN, 2).weekday() == MON:
                self[date(year, JAN, 2) + rd(days=+1)] = name + ' (Observed)'
        if self.country in ('UK', 'Northern Ireland', 'Ireland'):
            name = "St. Patrick's Day"
            if self.country == 'UK':
                name += ' [Northern Ireland]'
            self[date(year, MAR, 17)] = name
            if self.observed and date(year, MAR, 17).weekday() in WEEKEND:
                self[date(year, MAR, 17) + rd(weekday=MO)] = name + ' (Observed)'
        if self.country != 'Ireland':
            self[easter(year) + rd(weekday=FR(-1))] = 'Good Friday'
        if self.country != 'Scotland':
            name = 'Easter Monday'
            if self.country == 'UK':
                name += ' [England, Wales, Northern Ireland]'
            self[easter(year) + rd(weekday=MO)] = name
        if year >= 1978:
            name = 'May Day'
            if year == 2020 and self.country != 'Ireland':
                self[date(year, MAY, 8)] = name
            else:
                if year == 1995:
                    dt = date(year, MAY, 8)
                else:
                    dt = date(year, MAY, 1)
                if dt.weekday() == MON:
                    self[dt] = name
                elif dt.weekday() == TUE:
                    self[dt + rd(days=+6)] = name
                elif dt.weekday() == WED:
                    self[dt + rd(days=+5)] = name
                elif dt.weekday() == THU:
                    self[dt + rd(days=+4)] = name
                elif dt.weekday() == FRI:
                    self[dt + rd(days=+3)] = name
                elif dt.weekday() == SAT:
                    self[dt + rd(days=+2)] = name
                elif dt.weekday() == SUN:
                    self[dt + rd(days=+1)] = name
        if self.country != 'Ireland':
            name = 'Spring Bank Holiday'
            if year == 2012:
                self[date(year, JUN, 4)] = name
            elif year >= 1971:
                self[date(year, MAY, 31) + rd(weekday=MO(-1))] = name
        if self.country == 'Ireland':
            self[date(year, JUN, 1) + rd(weekday=MO)] = 'June Bank Holiday'
        if self.country == 'Isle of Man':
            self[date(year, JUN, 1) + rd(weekday=FR)] = 'TT Bank Holiday'
        if self.country == 'Isle of Man':
            self[date(year, JUL, 5)] = 'Tynwald Day'
        if self.country in ('UK', 'Northern Ireland'):
            name = 'Battle of the Boyne'
            if self.country == 'UK':
                name += ' [Northern Ireland]'
            self[date(year, JUL, 12)] = name
        if self.country in ('UK', 'Scotland', 'Ireland'):
            name = 'Summer Bank Holiday'
            if self.country == 'UK':
                name += ' [Scotland]'
            self[date(year, AUG, 1) + rd(weekday=MO)] = name
        if self.country not in ('Scotland', 'Ireland') and year >= 1971:
            name = 'Late Summer Bank Holiday'
            if self.country == 'UK':
                name += ' [England, Wales, Northern Ireland]'
            self[date(year, AUG, 31) + rd(weekday=MO(-1))] = name
        if self.country == 'Ireland':
            name = 'October Bank Holiday'
            self[date(year, OCT, 31) + rd(weekday=MO(-1))] = name
        if self.country in ('UK', 'Scotland'):
            name = "St. Andrew's Day"
            if self.country == 'UK':
                name += ' [Scotland]'
            self[date(year, NOV, 30)] = name
        name = 'Christmas Day'
        self[date(year, DEC, 25)] = name
        if self.observed and date(year, DEC, 25).weekday() == SAT:
            self[date(year, DEC, 27)] = name + ' (Observed)'
        elif self.observed and date(year, DEC, 25).weekday() == SUN:
            self[date(year, DEC, 27)] = name + ' (Observed)'
        name = 'Boxing Day'
        self[date(year, DEC, 26)] = name
        if self.observed and date(year, DEC, 26).weekday() == SAT:
            self[date(year, DEC, 28)] = name + ' (Observed)'
        elif self.observed and date(year, DEC, 26).weekday() == SUN:
            self[date(year, DEC, 28)] = name + ' (Observed)'
        if self.country != 'Ireland':
            if year == 1977:
                self[date(year, JUN, 7)] = 'Silver Jubilee of Elizabeth II'
            elif year == 1981:
                self[date(year, JUL, 29)] = 'Wedding of Charles and Diana'
            elif year == 1999:
                self[date(year, DEC, 31)] = 'Millennium Celebrations'
            elif year == 2002:
                self[date(year, JUN, 3)] = 'Golden Jubilee of Elizabeth II'
            elif year == 2011:
                self[date(year, APR, 29)] = 'Wedding of William and Catherine'
            elif year == 2012:
                self[date(year, JUN, 5)] = 'Diamond Jubilee of Elizabeth II'


class UK(UnitedKingdom):
    pass


class GB(UnitedKingdom):
    pass


class GBR(UnitedKingdom):
    pass


class England(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'England'
        HolidayBase.__init__(self, **kwargs)


class Wales(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'Wales'
        HolidayBase.__init__(self, **kwargs)


class Scotland(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'Scotland'
        HolidayBase.__init__(self, **kwargs)


class IsleOfMan(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'Isle of Man'
        HolidayBase.__init__(self, **kwargs)


class NorthernIreland(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'Northern Ireland'
        HolidayBase.__init__(self, **kwargs)