# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/util/ptime.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 956 bytes
"""
ptime.py -  Precision time function made os-independent
(should have been taken care of by python)
"""
from __future__ import division
import sys, time as systime
START_TIME = None
time = None

def winTime():
    """Return the current time in seconds with high precision

    (Windows version, use Manager.time() to stay platform independent.)
    """
    return systime.clock() + START_TIME


def unixTime():
    """Return the current time in seconds with high precision

    (Unix version, use Manager.time() to stay platform independent.)
    """
    return systime.time()


if sys.platform.startswith('win'):
    cstart = systime.clock()
    START_TIME = systime.time() - cstart
    time = winTime
else:
    time = unixTime