# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/g_datetime.py
# Compiled at: 2009-09-20 07:28:11
import datetime

def ISO2datetime(s):
    dp, tp = s.split('T')
    y, mo, d = dp.split('-')
    h, mi, s = tp.split(':')
    fs = float(s)
    return datetime.datetime(int(y), int(mo), int(d), int(h), int(mi), int(fs), int(1000000 * (fs - int(fs))))


def timedelta2float(tdel):
    return 86400.0 * tdel.days + tdel.seconds + 1e-06 * tdel.microseconds