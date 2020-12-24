# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/ptime.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 891 bytes
"""
ptime.py -  Precision time function made os-independent (should have been taken care of by python)
Copyright 2010  Luke Campagnola
Distributed under MIT/X11 license. See license.txt for more infomation.
"""
import sys, time as systime
START_TIME = None
time = None

def winTime():
    """Return the current time in seconds with high precision (windows version, use Manager.time() to stay platform independent)."""
    return systime.clock() + START_TIME


def unixTime():
    """Return the current time in seconds with high precision (unix version, use Manager.time() to stay platform independent)."""
    return systime.time()


if sys.platform.startswith('win'):
    cstart = systime.clock()
    START_TIME = systime.time() - cstart
    time = winTime
else:
    time = unixTime