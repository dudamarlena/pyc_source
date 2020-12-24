# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/luxembourg.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, MO
from holidays.constants import JAN, MAY, JUN, AUG, NOV, DEC
from holidays.holiday_base import HolidayBase

class Luxembourg(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'LU'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Neijoerschdag'
        self[easter(year) + rd(weekday=MO)] = 'Ouschterméindeg'
        self[date(year, MAY, 1)] = 'Dag vun der Aarbecht'
        if year >= 2019:
            self[date(year, MAY, 9)] = 'Europadag'
        self[easter(year) + rd(days=39)] = 'Christi Himmelfaart'
        self[easter(year) + rd(days=50)] = 'Péngschtméindeg'
        self[date(year, JUN, 23)] = 'Nationalfeierdag'
        self[date(year, AUG, 15)] = 'Léiffrawëschdag'
        self[date(year, NOV, 1)] = 'Allerhellgen'
        self[date(year, DEC, 25)] = 'Chrëschtdag'
        self[date(year, DEC, 26)] = 'Stiefesdag'


class LU(Luxembourg):
    pass


class LUX(Luxembourg):
    pass