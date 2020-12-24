# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/ptime.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 891 bytes
__doc__ = '\nptime.py -  Precision time function made os-independent (should have been taken care of by python)\nCopyright 2010  Luke Campagnola\nDistributed under MIT/X11 license. See license.txt for more infomation.\n'
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