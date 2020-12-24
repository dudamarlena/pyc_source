# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/financespy/account.py
# Compiled at: 2019-06-26 14:52:36
# Size of source mod 2**32: 427 bytes
import datetime, financespy.time_factory as time_factory
_current_year = datetime.datetime.now().year

class Account:

    def __init__(self, backend):
        self.timef = time_factory.TimeFactory(backend)

    def day(self, day, month, year=_current_year):
        return self.timef.month(month, year).day(day)

    def month(self, month, year=_current_year):
        return self.timef.month(month, year)