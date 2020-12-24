# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\swapdate\swapdate.py
# Compiled at: 2016-10-17 16:51:56
import time
from datetime import datetime, timedelta

def get(format=''):
    format = format.upper()
    date = datetime.now()
    if format == 'U':
        return str(date.strftime('%m/%d/%y'))
    else:
        if format == 'UX':
            return str(date.strftime('%m/%d/%Y'))
        else:
            if format == 'S':
                return str(date.strftime('%y%m%d'))
            if format == 'SX':
                return str(date.strftime('%Y%m%d'))
            if format == 'W':
                return str(date.strftime('%a'))
            if format == 'WX':
                return str(date.strftime('%A'))
            if format == 'O':
                return str(date.strftime('%y/%m/%d'))
            if format == 'OX':
                return str(date.strftime('%Y/%m/%d'))
            if format == 'M':
                return str(date.strftime('%b'))
            if format == 'MX':
                return str(date.strftime('%B'))
            if format == 'E':
                return str(date.strftime('%d/%m/%y'))
            if format == 'EX':
                return str(date.strftime('%d/%m/%Y'))
            if format == 'T12':
                return str(date.strftime('%I:%M %p'))
            if format == 'T12X':
                return str(date.strftime('%I:%M:%S %p'))
            if format == 'T12XX':
                return str(date.strftime('%I:%M:%S:%f %p'))
            if format == 'T24X':
                return str(date.strftime('%H:%M:%S %p'))
            if format == 'T24XX':
                return str(date.strftime('%H:%M:%S:%f %p'))
            if format == 'T24':
                return str(date.strftime('%H:%M %p'))
            if format == 'N':
                return str(date.strftime('%d %b %Y'))
            if format == 'NX':
                return str(date.strftime('%d %B %Y'))
            if format == 'D':
                return str(date.strftime('%j'))
            if format == '':
                return str(date.strftime('%m/%d/%y %H:%M:%S'))
            return

        return