# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\helper\python.py
# Compiled at: 2016-06-21 11:50:46
import sys, time

def python_3():
    return sys.version_info[0] == 3


def xrange(start, stop, step):
    while start < stop:
        yield start
        start += step


def delta_ms(start):
    return (time.time() - start) * 1000