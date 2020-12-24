# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\protocols\SMB\utils.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 238 bytes
import enum, binascii, datetime, sys

def wintime2datetime(timeint):
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=(timeint / 10.0))


def dt2wt(dt):
    return int(dt.timestamp() * 10000000.0)