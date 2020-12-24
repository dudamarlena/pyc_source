# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dal/dbapi/config_cx_Oracle.py
# Compiled at: 2007-06-15 17:41:24
import cx_Oracle, datetime

def convertdt(moddt, field_desc, pref=None):
    """convert Oracle DateTime to Python datetime"""
    year = moddt.year
    month = moddt.month
    day = moddt.day
    hour = moddt.hour
    minute = moddt.minute
    sec = moddt.second
    msec = moddt.fsecond
    pydt = datetime.datetime(year, month, day, hour, minute, sec, msec)
    return pydt