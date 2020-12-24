# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/dates.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import calendar
from datetime import datetime
from django.db.models import DateField
from django.utils import six
from django.utils.timezone import utc

def http_date(timestamp):
    """
    A wrapper around Django's http_date that accepts DateFields and
    datetime objects directly.
    """
    from django.utils.http import http_date
    if isinstance(timestamp, (DateField, datetime)):
        return http_date(calendar.timegm(timestamp.timetuple()))
    else:
        if isinstance(timestamp, six.string_types):
            return timestamp
        return http_date(timestamp)


def get_latest_timestamp(timestamps):
    """
    Returns the latest timestamp in a list of timestamps.
    """
    latest = None
    for timestamp in timestamps:
        if latest is None or timestamp > latest:
            latest = timestamp

    return latest


def get_tz_aware_utcnow():
    """Returns a UTC aware datetime object"""
    return datetime.utcnow().replace(tzinfo=utc)