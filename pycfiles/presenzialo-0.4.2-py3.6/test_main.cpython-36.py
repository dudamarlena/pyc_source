# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/presenzialo/logs/test_main.py
# Compiled at: 2020-01-15 07:36:53
# Size of source mod 2**32: 1704 bytes
import re, datetime
from .daylog import DayLog
from .dayloglist import DayLogList

def main():
    print('\n>>> DayLog tests:')
    print('>>> Null DayLog')
    d = DayLog()
    print(d)
    print('>>> Today DayLog')
    d = DayLog(datetime.datetime.today(), ['09:03', '10:13'])
    print(d)
    print('>>> date()')
    print(d.date())
    print('>>> uptime()')
    print(d.uptime())
    print('>>> logins()')
    print(d.logins())
    print('>>> logouts()')
    print(d.logouts())
    time_start = datetime.time(10, 4)
    time_final = datetime.time(10, 5)
    dstart = datetime.datetime.combine(datetime.date.today(), time_start)
    dfinal = datetime.datetime.combine(datetime.date.today(), time_final)
    print('>>> starting time')
    print(dstart)
    print('>>> uptime from starting time')
    print(d.uptime(dstart))
    print('>>> ending time')
    print(dfinal)
    print(d.uptime(dstart, dfinal))
    d1 = DayLog(datetime.datetime.today(), ['09:03', '10:13'])
    d2 = DayLog(datetime.datetime.today(), ['11:03', '12:13'])
    print('>>> Sum')
    print('>>> d1')
    print(d1)
    print('>>> d2')
    print(d2)
    s = d1 + d2
    print('>>> d1 + d2')
    print(s)
    print('\n>>> DayLogList tests:')
    print('>>> DayLogList null')
    l = DayLogList()
    print(l)
    print('>>> d1')
    d1 = DayLog(datetime.datetime(2014, 12, 3), ['09:03', '10:13'])
    print(d1)
    print('>>> d2')
    d2 = DayLog(datetime.datetime(2014, 12, 4), ['11:03', '15:13'])
    print(d2)
    l.append(d1)
    l.append(d2)
    print('>>> d1 + d2')
    print(l)


if __name__ == '__main__':
    main()