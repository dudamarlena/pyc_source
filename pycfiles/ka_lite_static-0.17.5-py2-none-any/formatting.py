# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/utils/formatting.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
import email, datetime, time
from django.utils import dateformat
from tastypie.utils.timezone import make_aware, make_naive, aware_datetime
try:
    from dateutil.parser import parse as mk_datetime
except ImportError:

    def mk_datetime(string):
        return make_aware(datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate(string))))


def format_datetime(dt):
    """
    RFC 2822 datetime formatter
    """
    return dateformat.format(make_naive(dt), b'r')


def format_date(d):
    """
    RFC 2822 date formatter
    """
    dt = aware_datetime(d.year, d.month, d.day, 0, 0, 0)
    return dateformat.format(dt, b'j M Y')


def format_time(t):
    """
    RFC 2822 time formatter
    """
    dt = aware_datetime(2000, 1, 1, t.hour, t.minute, t.second)
    return dateformat.format(dt, b'H:i:s O')