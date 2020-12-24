# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/austria.py
# Compiled at: 2020-02-11 16:03:33
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, MO
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class Austria(HolidayBase):
    PROVINCES = [
     '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def __init__(self, **kwargs):
        self.country = 'AT'
        self.prov = kwargs.pop('prov', kwargs.pop('state', '9'))
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Neujahr'
        self[date(year, JAN, 6)] = 'Heilige Drei Könige'
        self[easter(year) + rd(weekday=MO)] = 'Ostermontag'
        self[date(year, MAY, 1)] = 'Staatsfeiertag'
        self[easter(year) + rd(days=39)] = 'Christi Himmelfahrt'
        self[easter(year) + rd(days=50)] = 'Pfingstmontag'
        self[easter(year) + rd(days=60)] = 'Fronleichnam'
        self[date(year, AUG, 15)] = 'Mariä Himmelfahrt'
        if 1919 <= year <= 1934:
            self[date(year, NOV, 12)] = 'Nationalfeiertag'
        if year >= 1967:
            self[date(year, OCT, 26)] = 'Nationalfeiertag'
        self[date(year, NOV, 1)] = 'Allerheiligen'
        self[date(year, DEC, 8)] = 'Mariä Empfängnis'
        self[date(year, DEC, 25)] = 'Christtag'
        self[date(year, DEC, 26)] = 'Stefanitag'


class AT(Austria):
    pass


class AUT(Austria):
    pass