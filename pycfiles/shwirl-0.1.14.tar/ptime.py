# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/util/ptime.py
# Compiled at: 2016-11-03 01:40:19
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