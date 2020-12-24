# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/kenya.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR, MO
from holidays.constants import JAN, MAY, JUN, OCT, DEC
from holidays.constants import SUN
from holidays.holiday_base import HolidayBase

class Kenya(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'KE'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "New Year's Day"
        self[date(year, MAY, 1)] = 'Labour Day'
        self[date(year, JUN, 1)] = 'Madaraka Day'
        self[date(year, OCT, 20)] = 'Mashujaa Day'
        self[date(year, DEC, 12)] = 'Jamhuri (Independence) Day'
        self[date(year, DEC, 25)] = 'Christmas Day'
        self[date(year, DEC, 26)] = 'Boxing Day'
        for k, v in list(self.items()):
            if self.observed and k.weekday() == SUN:
                self[k + rd(days=1)] = v + ' (Observed)'

        self[easter(year) - rd(weekday=FR(-1))] = 'Good Friday'
        self[easter(year) + rd(weekday=MO(+1))] = 'Easter Monday'


class KE(Kenya):
    pass


class KEN(Kenya):
    pass