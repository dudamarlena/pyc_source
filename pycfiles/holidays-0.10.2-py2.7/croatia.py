# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/croatia.py
# Compiled at: 2020-02-10 15:45:14
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, MAY, JUN, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class Croatia(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'HR'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nova Godina'
        self[date(year, JAN, 6)] = 'Sveta tri kralja'
        easter_date = easter(year)
        self[easter_date] = 'Uskrs'
        self[easter_date + rd(days=1)] = 'Uskrsni ponedjeljak'
        self[easter_date + rd(days=60)] = 'Tijelovo'
        self[date(year, MAY, 1)] = 'Međunarodni praznik rada'
        self[date(year, JUN, 22)] = 'Dan antifašističke borbe'
        if year < 2020:
            self[date(year, JUN, 25)] = 'Dan državnosti'
        self[date(year, AUG, 5)] = 'Dan pobjede i domovinske zahvalnosti'
        self[date(year, AUG, 15)] = 'Velika Gospa'
        self[date(year, OCT, 8)] = 'Dan neovisnosti'
        self[date(year, NOV, 1)] = 'Svi sveti'
        if year >= 2020:
            self[date(year, NOV, 18)] = 'Dan sjećanja'
        self[date(year, DEC, 25)] = 'Božić'
        self[date(year, DEC, 26)] = 'Sveti Stjepan'


class HR(Croatia):
    pass


class HRV(Croatia):
    pass