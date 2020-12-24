# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/DateUtils.py
# Compiled at: 2011-01-12 10:20:04
from datetime import date, timedelta

class DateUtils(object):
    """
    This class stores some useful functions operating with dates
    """

    def __init__(self):
        pass

    @staticmethod
    def getDateStrFromDay(day, startYear):
        """
        Takes a day and start year and add the number of days to the start date
        and return the string representation. 
        """
        startDate = date(startYear, 1, 1)
        tDelta = timedelta(days=day)
        endDate = startDate + tDelta
        return endDate.strftime('%d/%m/%y')

    @staticmethod
    def getDayDelta(endDate, startYear):
        """
        Take a day
        """
        startYear = date(startYear, 1, 1)
        delta = endDate - startYear
        return delta.days