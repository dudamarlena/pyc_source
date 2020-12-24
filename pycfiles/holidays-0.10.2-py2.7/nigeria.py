# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/nigeria.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from holidays.constants import JAN, MAY, JUN, OCT, DEC
from holidays.holiday_base import HolidayBase

class Nigeria(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'NG'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "New Year's day"
        self[date(year, MAY, 1)] = "Worker's day"
        self[date(year, MAY, 27)] = "Children's day"
        self[date(year, JUN, 12)] = 'Democracy day'
        self[date(year, OCT, 1)] = 'Independence day'
        self[date(year, DEC, 25)] = 'Christmas day'
        self[date(year, DEC, 26)] = 'Boxing day'


class NG(Nigeria):
    pass


class NGA(Nigeria):
    pass