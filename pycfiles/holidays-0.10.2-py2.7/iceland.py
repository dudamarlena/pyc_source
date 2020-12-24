# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/iceland.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR, TH, MO
from holidays.constants import JAN, APR, MAY, JUN, AUG, DEC
from holidays.holiday_base import HolidayBase

class Iceland(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'IS'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nýársdagur'
        self[easter(year) - rd(days=3)] = 'Skírdagur'
        self[easter(year) + rd(weekday=FR(-1))] = 'Föstudagurinn langi'
        self[easter(year)] = 'Páskadagur'
        self[easter(year) + rd(days=1)] = 'Annar í páskum'
        self[date(year, APR, 19) + rd(weekday=TH(+1))] = 'Sumardagurinn fyrsti'
        self[date(year, MAY, 1)] = 'Verkalýðsdagurinn'
        self[easter(year) + rd(days=39)] = 'Uppstigningardagur'
        self[easter(year) + rd(days=49)] = 'Hvítasunnudagur'
        self[easter(year) + rd(days=50)] = 'Annar í hvítasunnu'
        self[date(year, JUN, 17)] = 'Þjóðhátíðardagurinn'
        self[date(year, AUG, 1) + rd(weekday=MO(+1))] = 'Frídagur verslunarmanna'
        self[date(year, DEC, 24)] = 'Aðfangadagur'
        self[date(year, DEC, 25)] = 'Jóladagur'
        self[date(year, DEC, 26)] = 'Annar í jólum'
        self[date(year, DEC, 31)] = 'Gamlársdagur'


class IS(Iceland):
    pass


class ISL(Iceland):
    pass