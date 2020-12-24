# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intellisense/utils.py
# Compiled at: 2013-10-08 10:43:23
import json
from datetime import datetime
from dateutil.tz import tzlocal, tzutc

def is_naive(dt):
    """ Determines if a given datetime.datetime is naive. """
    return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None


def guess_timezone(dt):
    """ Attempts to convert a naive datetime to an aware datetime """
    if is_naive(dt):
        delta = datetime.now() - dt
        if delta.total_seconds() < 5:
            return dt.replace(tzinfo=tzlocal())
        return dt.replace(tzinfo=tzutc())
    return dt


class DatetimeSerializer(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)