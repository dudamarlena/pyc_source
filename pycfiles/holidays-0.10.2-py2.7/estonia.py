# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/estonia.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, FEB, MAY, JUN, AUG, DEC
from holidays.holiday_base import HolidayBase

class Estonia(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'EE'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        e = easter(year)
        self[date(year, JAN, 1)] = 'uusaasta'
        self[date(year, FEB, 24)] = 'iseseisvuspäev'
        self[e - rd(days=2)] = 'suur reede'
        self[e] = 'ülestõusmispühade 1. püha'
        self[date(year, MAY, 1)] = 'kevadpüha'
        self[e + rd(days=49)] = 'nelipühade 1. püha'
        self[date(year, JUN, 23)] = 'võidupüha'
        self[date(year, JUN, 24)] = 'jaanipäev'
        self[date(year, AUG, 20)] = 'taasiseseisvumispäev'
        self[date(year, DEC, 24)] = 'jõululaupäev'
        self[date(year, DEC, 25)] = 'esimene jõulupüha'
        self[date(year, DEC, 26)] = 'teine jõulupüha'


class EE(Estonia):
    pass


class EST(Estonia):
    pass