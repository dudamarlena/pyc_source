# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/models/dateutil_constants.py
# Compiled at: 2014-08-27 19:26:12
YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY = range(7)
FREQ_MAP = {'YEARLY': YEARLY, 'MONTHLY': MONTHLY, 
   'WEEKLY': WEEKLY, 
   'DAILY': DAILY, 
   'HOURLY': HOURLY, 
   'MINUTELY': MINUTELY, 
   'SECONDLY': SECONDLY}
MO, TU, WE, TH, FR, SA, SU = range(7)
WEEKDAY_MAP = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}
WEEKDAY_TUPLES = [ (v, k) for k, v in WEEKDAY_MAP.items() ]
WEEKDAY_TUPLES = sorted(WEEKDAY_TUPLES)
WEEKDAY_TUPLES = [ (k, k) for j, k in WEEKDAY_TUPLES ]