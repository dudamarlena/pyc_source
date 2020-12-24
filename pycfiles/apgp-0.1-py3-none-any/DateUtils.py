# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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