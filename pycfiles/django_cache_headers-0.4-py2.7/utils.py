# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-cache-headers/cache_headers/utils.py
# Compiled at: 2017-03-22 04:19:49


def httpdate(dt):
    """Return a string representation of a date according to RFC 1123
    (HTTP/1.1).

    The supplied date must be in UTC.
    """
    weekday = [
     'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][dt.weekday()]
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
     'Oct', 'Nov', 'Dec'][(dt.month - 1)]
    return '%s, %02d %s %04d %02d:%02d:%02d GMT' % (weekday, dt.day, month,
     dt.year, dt.hour, dt.minute, dt.second)