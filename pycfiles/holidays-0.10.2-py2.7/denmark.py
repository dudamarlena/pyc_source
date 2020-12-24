# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/denmark.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, SU, TH, FR, MO
from holidays.constants import JAN, DEC
from holidays.holiday_base import HolidayBase

class Denmark(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'DK'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nytårsdag'
        self[easter(year) + rd(weekday=SU(-2))] = 'Palmesøndag'
        self[easter(year) + rd(weekday=TH(-1))] = 'Skærtorsdag'
        self[easter(year) + rd(weekday=FR(-1))] = 'Langfredag'
        self[easter(year)] = 'Påskedag'
        self[easter(year) + rd(weekday=MO)] = 'Anden påskedag'
        self[easter(year) + rd(weekday=FR(+4))] = 'Store bededag'
        self[easter(year) + rd(days=39)] = 'Kristi himmelfartsdag'
        self[easter(year) + rd(days=49)] = 'Pinsedag'
        self[easter(year) + rd(days=50)] = 'Anden pinsedag'
        self[date(year, DEC, 25)] = 'Juledag'
        self[date(year, DEC, 26)] = 'Anden juledag'


class DK(Denmark):
    pass


class DNK(Denmark):
    pass