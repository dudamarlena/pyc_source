# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/accountingModules/myUtilities.py
# Compiled at: 2012-04-11 19:28:00
import os
from datetime import date
import time

def stringToDate(theDate, date_format):
    dateStr = time.strptime(theDate, date_format)
    return date(dateStr.tm_year, dateStr.tm_mon, dateStr.tm_mday)


def addMonthsToDate(theDate, duration):
    yyyy = theDate.year
    mm = theDate.month + duration
    while mm > 12:
        mm = mm - 12
        yyyy = yyyy + 1

    return date(yyyy, mm, 1)


def median(alist):
    srtd = sorted(alist)
    mid = len(alist) / 2
    if len(alist) % 2 == 0:
        return (srtd[(mid - 1)] + srtd[mid]) / 2.0
    else:
        return srtd[mid]