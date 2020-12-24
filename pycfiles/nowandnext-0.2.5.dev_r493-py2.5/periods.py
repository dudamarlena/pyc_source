# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/calendar/periods.py
# Compiled at: 2009-05-11 19:02:39
"""
Some handy time-periods.
"""
import datetime
SECONDS_IN_A_MINUTE = 60
SECONDS_IN_AN_HOUR = SECONDS_IN_A_MINUTE * 60
SECONDS_IN_A_DAY = SECONDS_IN_AN_HOUR * 24
onesecond = datetime.timedelta(seconds=1)
oneminute = onesecond * SECONDS_IN_A_MINUTE
onehour = oneminute * SECONDS_IN_A_MINUTE
oneday = datetime.timedelta(days=1)
oneweek = oneday * 7