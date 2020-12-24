# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/european_central_bank.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, MAY, DEC
from holidays.holiday_base import HolidayBase

class EuropeanCentralBank(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'EU'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "New Year's Day"
        e = easter(year)
        self[e - rd(days=2)] = 'Good Friday'
        self[e + rd(days=1)] = 'Easter Monday'
        self[date(year, MAY, 1)] = '1 May (Labour Day)'
        self[date(year, DEC, 25)] = 'Christmas Day'
        self[date(year, DEC, 26)] = '26 December'


class ECB(EuropeanCentralBank):
    pass


class TAR(EuropeanCentralBank):
    pass