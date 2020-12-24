# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/sifr/util.py
# Compiled at: 2015-06-10 09:00:02
import datetime
from dateutil import parser
import six

def normalize_time(t):
    try:
        if isinstance(t, datetime.datetime):
            return t
        if isinstance(t, datetime.date):
            return datetime.datetime(t.year, t.month, t.day)
        if isinstance(t, (int, float)):
            return datetime.datetime.fromtimestamp(t)
        if isinstance(t, six.string_types):
            return parser.parse(t)
        raise TypeError
    except:
        raise TypeError('time must be represented as either a timestamp (int,float), a datetime.(datetime/date) object, or an iso-8601 formatted string. Not %s' % t.__class__.__name__)