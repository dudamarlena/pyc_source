# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zoocli/utils.py
# Compiled at: 2015-05-16 08:02:18
# Size of source mod 2**32: 151 bytes
import datetime

def timestamp_to_date(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime('%Y-%m-%d %H:%M:%S')