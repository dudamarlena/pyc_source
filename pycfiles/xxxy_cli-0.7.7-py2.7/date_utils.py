# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/date_utils.py
# Compiled at: 2018-12-27 05:19:41
from datetime import datetime
from russell.constants import LOCAL_TIMEZONE

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now(LOCAL_TIMEZONE)
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    else:
        if isinstance(time, datetime):
            diff = now - time
        else:
            if not time:
                diff = now - now
            second_diff = diff.seconds
            day_diff = diff.days
            if day_diff < 0:
                return ''
            if day_diff == 0:
                if second_diff < 10:
                    return 'just now'
                if second_diff < 60:
                    return str(second_diff) + ' seconds ago'
                if second_diff < 120:
                    return 'a minute ago'
                if second_diff < 3600:
                    return str(int(second_diff / 60)) + ' minutes ago'
                if second_diff < 7200:
                    return 'an hour ago'
                if second_diff < 86400:
                    return str(int(second_diff / 3600)) + ' hours ago'
            if day_diff == 1:
                return 'Yesterday'
            if day_diff < 7:
                return str(day_diff) + ' days ago'
            if day_diff < 31:
                return str(int(day_diff / 7)) + ' weeks ago'
        if day_diff < 365:
            return str(int(day_diff / 30)) + ' months ago'
    return str(int(day_diff / 365)) + ' years ago'