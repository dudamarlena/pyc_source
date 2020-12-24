# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kracekumar/Dropbox/codes/python/python/procinfo/procinfo/patch.py
# Compiled at: 2012-08-08 09:01:24
import psutil
FACTOR = 1024.0
MEMORY_UNITS = ['B', 'KB', 'MB', 'GB', 'TB']

def return_human_readable(value, unit=0):
    if value < FACTOR:
        return {'value': round(value, 2), 'str': (' ').join([str(round(value, 2)), MEMORY_UNITS[unit]])}
    if value == FACTOR:
        temp = round(value / FACTOR, 2)
        return {'value': temp, 'str': (' ').join([str(temp), MEMORY_UNITS[unit]])}
    if value > FACTOR:
        return return_human_readable(value / FACTOR, unit + 1)


TOTAL_MEMORY = return_human_readable(psutil.TOTAL_PHYMEM)