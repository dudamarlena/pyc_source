# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyzenobase/util.py
# Compiled at: 2015-09-24 11:30:19
# Size of source mod 2**32: 245 bytes
import pytz
from tzlocal import get_localzone

def fmt_datetime(dt, timezone=str(get_localzone())):
    tz = pytz.timezone(timezone)
    dt = dt.astimezone(tz) if dt.tzinfo else tz.localize(dt)
    return dt.strftime('%Y-%m-%dT%H:%M:%S.000%z')