# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/sphirewallapi/utils.py
# Compiled at: 2018-06-20 19:57:46
from datetime import date, timedelta

class DateHelper:

    @staticmethod
    def today():
        return date.today()

    @staticmethod
    def yesterday():
        return date.today() - timedelta(1)

    @staticmethod
    def week():
        return date.today() - timedelta(date.today().weekday())

    @staticmethod
    def month():
        return date.today().replace(day=1)