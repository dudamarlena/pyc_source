# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/suxsync/util.py
# Compiled at: 2008-05-11 18:49:43
"""
Utility functions
"""
SECONDS_PER_DAY = 86400
MILLISECONDS_PER_SECOND = 1000.0

def timeDeltaToSeconds(aTimeDelta):
    seconds = aTimeDelta.days * SECONDS_PER_DAY
    seconds = seconds + aTimeDelta.seconds
    return float(seconds)