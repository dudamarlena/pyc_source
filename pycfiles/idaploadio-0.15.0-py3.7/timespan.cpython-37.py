# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/util/timespan.py
# Compiled at: 2020-04-13 02:37:12
# Size of source mod 2**32: 1016 bytes
import re
from datetime import timedelta

def parse_timespan(time_str):
    """
    Parse a string representing a time span and return the number of seconds.
    Valid formats are: 20, 20s, 3m, 2h, 1h20m, 3h30m10s, etc.
    """
    if not time_str:
        raise ValueError('Invalid time span format')
    else:
        if re.match('^\\d+$', time_str):
            return int(time_str)
        timespan_regex = re.compile('((?P<hours>\\d+?)h)?((?P<minutes>\\d+?)m)?((?P<seconds>\\d+?)s)?')
        parts = timespan_regex.match(time_str)
        if not parts:
            raise ValueError('Invalid time span format. Valid formats: 20, 20s, 3m, 2h, 1h20m, 3h30m10s, etc.')
        parts = parts.groupdict()
        time_params = {name:int(value) for name, value in parts.items() if value if value}
        assert time_params, 'Invalid time span format. Valid formats: 20, 20s, 3m, 2h, 1h20m, 3h30m10s, etc.'
    return int(timedelta(**time_params).total_seconds())