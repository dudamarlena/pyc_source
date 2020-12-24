# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luto/snotes20/osf.py/venv/lib/python3.4/site-packages/osf/timeutils.py
# Compiled at: 2015-08-23 11:29:24
# Size of source mod 2**32: 537 bytes
import math

def milliseconds_to_hhmmss(time):
    hundredths = str(math.floor(time % 1000)).zfill(3)
    time /= 1000
    seconds = str(math.floor(time % 60)).zfill(2)
    minutes = str(math.floor(time / 60 % 60)).zfill(2)
    hours = str(math.floor(time / 60 / 60 % 60)).zfill(2)
    return hours + ':' + minutes + ':' + seconds + '.' + hundredths


def hhmmss_to_milliseconds(hh, mm, ss, hundredths):
    val = (int(ss) + int(mm) * 60 + int(hh) * 60 * 60) * 1000
    if hundredths:
        val += int(hundredths)
    return val