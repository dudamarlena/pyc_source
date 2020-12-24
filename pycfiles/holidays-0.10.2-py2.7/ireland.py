# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/ireland.py
# Compiled at: 2020-01-26 19:25:31
from holidays.holiday_base import HolidayBase
from .united_kingdom import UnitedKingdom

class Ireland(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'Ireland'
        HolidayBase.__init__(self, **kwargs)


class IE(Ireland):
    pass


class IRL(Ireland):
    pass