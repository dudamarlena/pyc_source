# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/quebert/common.py
# Compiled at: 2009-08-21 14:12:20
from datetime import datetime
DEFAULT_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

def parse_date(d, f=DEFAULT_DATE_FORMAT):
    return datetime.strptime(d, f)


def serialize_date(d, f=DEFAULT_DATE_FORMAT):
    return datetime.strftime(d, f)


def now():
    return datetime.utcnow()


def now_serialized():
    return serialize_date(now())