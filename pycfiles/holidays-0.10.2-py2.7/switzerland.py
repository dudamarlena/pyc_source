# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/switzerland.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR, TH, MO, SU
from holidays.constants import JAN, MAR, APR, MAY, JUN, AUG, SEP, NOV, DEC
from holidays.holiday_base import HolidayBase

class Switzerland(HolidayBase):
    PROVINCES = [
     'AG', 'AR', 'AI', 'BL', 'BS', 'BE', 'FR', 'GE', 'GL',
     'GR', 'JU', 'LU', 'NE', 'NW', 'OW', 'SG', 'SH', 'SZ',
     'SO', 'TG', 'TI', 'UR', 'VD', 'VS', 'ZG', 'ZH']

    def __init__(self, **kwargs):
        self.country = 'CH'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Neujahrestag'
        if self.prov in ('AG', 'BE', 'FR', 'GE', 'GL', 'GR', 'JU', 'LU', 'NE', 'OW',
                         'SH', 'SO', 'TG', 'VD', 'ZG', 'ZH'):
            self[date(year, JAN, 2)] = 'Berchtoldstag'
        if self.prov in ('SZ', 'TI', 'UR'):
            self[date(year, JAN, 6)] = 'Heilige Drei Könige'
        if self.prov == 'NE':
            self[date(year, MAR, 1)] = 'Jahrestag der Ausrufung der Republik'
        if self.prov in ('NW', 'SZ', 'TI', 'UR', 'VS'):
            self[date(year, MAR, 19)] = 'Josefstag'
        if self.prov == 'GL' and year >= 1835:
            if date(year, APR, 1) + rd(weekday=FR) != easter(year) - rd(days=2):
                self[date(year, APR, 1) + rd(weekday=TH)] = 'Näfelser Fahrt'
            else:
                self[date(year, APR, 8) + rd(weekday=TH)] = 'Näfelser Fahrt'
        self[easter(year)] = 'Ostern'
        if self.prov != 'VS':
            self[easter(year) - rd(days=2)] = 'Karfreitag'
            self[easter(year) + rd(weekday=MO)] = 'Ostermontag'
        if self.prov in ('BL', 'BS', 'JU', 'NE', 'SH', 'SO', 'TG', 'TI', 'ZH'):
            self[date(year, MAY, 1)] = 'Tag der Arbeit'
        self[easter(year) + rd(days=39)] = 'Auffahrt'
        self[easter(year) + rd(days=49)] = 'Pfingsten'
        self[easter(year) + rd(days=50)] = 'Pfingstmontag'
        if self.prov in ('AI', 'JU', 'LU', 'NW', 'OW', 'SZ', 'TI', 'UR', 'VS', 'ZG'):
            self[easter(year) + rd(days=60)] = 'Fronleichnam'
        if self.prov == 'JU':
            self[date(year, JUN, 23)] = 'Fest der Unabhängigkeit'
        if self.prov == 'TI':
            self[date(year, JUN, 29)] = 'Peter und Paul'
        if year >= 1291:
            self[date(year, AUG, 1)] = 'Nationalfeiertag'
        if self.prov in ('AI', 'JU', 'LU', 'NW', 'OW', 'SZ', 'TI', 'UR', 'VS', 'ZG'):
            self[date(year, AUG, 15)] = 'Mariä Himmelfahrt'
        if self.prov == 'VD':
            dt = date(year, SEP, 1) + rd(weekday=SU(+3)) + rd(weekday=MO)
            self[dt] = 'Lundi du Jeûne'
        if self.prov == 'OW':
            self[date(year, SEP, 25)] = 'Bruder Klaus'
        if self.prov in ('AI', 'GL', 'JU', 'LU', 'NW', 'OW', 'SG', 'SZ', 'TI', 'UR',
                         'VS', 'ZG'):
            self[date(year, NOV, 1)] = 'Allerheiligen'
        if self.prov in ('AI', 'LU', 'NW', 'OW', 'SZ', 'TI', 'UR', 'VS', 'ZG'):
            self[date(year, DEC, 8)] = 'Mariä Empfängnis'
        if self.prov == 'GE':
            self[date(year, DEC, 12)] = 'Escalade de Genève'
        self[date(year, DEC, 25)] = 'Weihnachten'
        if self.prov in ('AG', 'AR', 'AI', 'BL', 'BS', 'BE', 'FR', 'GL', 'GR', 'LU',
                         'NE', 'NW', 'OW', 'SG', 'SH', 'SZ', 'SO', 'TG', 'TI', 'UR',
                         'ZG', 'ZH'):
            self[date(year, DEC, 26)] = 'Stephanstag'
        if self.prov == 'GE':
            self[date(year, DEC, 31)] = 'Wiederherstellung der Republik'


class CH(Switzerland):
    pass


class CHE(Switzerland):
    pass