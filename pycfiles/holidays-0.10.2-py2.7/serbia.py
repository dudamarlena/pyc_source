# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/serbia.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter, EASTER_ORTHODOX
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, FEB, MAY, NOV
from holidays.constants import SUN, WEEKEND
from holidays.holiday_base import HolidayBase

class Serbia(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'RS'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        name = 'Нова година'
        self[date(year, JAN, 1)] = name
        self[date(year, JAN, 2)] = name
        if self.observed and date(year, JAN, 1).weekday() in WEEKEND:
            self[date(year, JAN, 3)] = name + ' (Observed)'
        name = 'Божић'
        self[date(year, JAN, 7)] = name
        name = 'Дан државности Србије'
        self[date(year, FEB, 15)] = name
        self[date(year, FEB, 16)] = name
        if self.observed and date(year, FEB, 15).weekday() in WEEKEND:
            self[date(year, FEB, 17)] = name + ' (Observed)'
        name = 'Празник рада'
        self[date(year, MAY, 1)] = name
        self[date(year, MAY, 2)] = name
        if self.observed and date(year, MAY, 1).weekday() in WEEKEND:
            self[date(year, MAY, 3)] = name + ' (Observed)'
        name = 'Дан примирја у Првом светском рату'
        self[date(year, NOV, 11)] = name
        if self.observed and date(year, NOV, 11).weekday() == SUN:
            self[date(year, NOV, 12)] = name + ' (Observed)'
        self[easter(year, method=EASTER_ORTHODOX) - rd(days=2)] = 'Велики петак'
        self[easter(year, method=EASTER_ORTHODOX) - rd(days=1)] = 'Велика субота'
        self[easter(year, method=EASTER_ORTHODOX)] = 'Васкрс'
        self[easter(year, method=EASTER_ORTHODOX) + rd(days=1)] = 'Други дан Васкрса'


class RS(Serbia):
    pass


class SRB(Serbia):
    pass