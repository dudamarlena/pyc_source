# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/ukraine.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from dateutil.easter import easter, EASTER_ORTHODOX
from dateutil.relativedelta import relativedelta as rd
from holidays.constants import JAN, MAR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class Ukraine(HolidayBase):
    """
    http://zakon1.rada.gov.ua/laws/show/322-08/paran454#n454
    """

    def __init__(self, **kwargs):
        self.country = 'UA'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year < 1918:
            return
        if year >= 1898:
            self[date(year, JAN, 1)] = 'Новий рік'
        if year >= 1991:
            self[date(year, JAN, 7)] = 'Різдво Христове (православне)'
        if year > 1965:
            self[date(year, MAR, 8)] = 'Міжнародний жіночий день'
        if year >= 1991:
            self[easter(year, method=EASTER_ORTHODOX)] = 'Пасха (Великдень)'
        if year >= 1991:
            self[easter(year, method=EASTER_ORTHODOX) + rd(days=49)] = 'Трійця'
        if year > 2017:
            name = 'День праці'
        elif 1917 < year <= 2017:
            name = 'День міжнародної солідарності трудящих'
        self[date(year, MAY, 1)] = name
        if 1928 < year < 2018:
            self[date(year, MAY, 2)] = 'День міжнародної солідарності трудящих'
        name = 'День перемоги'
        if year >= 1965:
            self[date(year, MAY, 9)] = name
        if 1945 <= year < 1947:
            self[date(year, MAY, 9)] = name
            self[date(year, SEP, 3)] = 'День перемоги над Японією'
        if year >= 1997:
            self[date(year, JUN, 28)] = 'День Конституції України'
        name = 'День незалежності України'
        if year > 1991:
            self[date(year, AUG, 24)] = name
        elif year == 1991:
            self[date(year, JUL, 16)] = name
        if year >= 2015:
            self[date(year, OCT, 14)] = 'День захисника України'
        name = 'День Конституції СРСР'
        if 1981 <= year < 1991:
            self[date(year, OCT, 7)] = name
        elif 1937 <= year < 1981:
            self[date(year, DEC, 5)] = name
        if 1917 < year < 2000:
            if year <= 1991:
                name = 'Річниця Великої Жовтневої соціалістичної революції'
            else:
                name = 'Річниця жовтневого перевороту'
            self[date(year, NOV, 7)] = name
            self[date(year, NOV, 8)] = name
        if year >= 2017:
            self[date(year, DEC, 25)] = 'Різдво Христове (католицьке)'
        if 1917 <= year < 1951:
            self[date(year, JAN, 22)] = "День пам'яті 9 січня 1905 року"
        if 1917 < year < 1929:
            self[date(year, MAR, 18)] = 'День паризької комуни'


class UA(Ukraine):
    pass


class UKR(Ukraine):
    pass