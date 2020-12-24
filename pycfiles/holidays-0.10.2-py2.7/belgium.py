# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/belgium.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, MAY, JUL, AUG, NOV, DEC
from holidays.holiday_base import HolidayBase

class Belgium(HolidayBase):
    """
    https://www.belgium.be/nl/over_belgie/land/belgie_in_een_notendop/feestdagen
    https://nl.wikipedia.org/wiki/Feestdagen_in_Belgi%C3%AB
    """

    def __init__(self, **kwargs):
        self.country = 'BE'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nieuwjaarsdag'
        easter_date = easter(year)
        self[easter_date] = 'Pasen'
        self[easter_date + rd(days=1)] = 'Paasmaandag'
        self[easter_date + rd(days=39)] = 'O.L.H. Hemelvaart'
        self[easter_date + rd(days=49)] = 'Pinksteren'
        self[easter_date + rd(days=50)] = 'Pinkstermaandag'
        self[date(year, MAY, 1)] = 'Dag van de Arbeid'
        self[date(year, JUL, 21)] = 'Nationale feestdag'
        self[date(year, AUG, 15)] = 'O.L.V. Hemelvaart'
        self[date(year, NOV, 1)] = 'Allerheiligen'
        self[date(year, NOV, 11)] = 'Wapenstilstand'
        self[date(year, DEC, 25)] = 'Kerstmis'


class BE(Belgium):
    pass


class BEL(Belgium):
    pass