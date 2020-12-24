# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kebl2765/Projects/django-conneg/django_conneg/utils.py
# Compiled at: 2014-10-28 11:46:48
# Size of source mod 2**32: 322 bytes
try:
    from pytz import utc
except ImportError:
    import datetime

    class _UTC(datetime.tzinfo):

        def utcoffset(self, dt):
            return datetime.timedelta(0)

        def dst(self, dt):
            return datetime.timedelta(0)

        def tzname(self, dt):
            return 'UTC'


    utc = _UTC()