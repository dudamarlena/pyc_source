# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zuul/projects/neoalchemy/lib/python3.5/site-packages/neoalchemy/types.py
# Compiled at: 2016-07-17 14:47:45
# Size of source mod 2**32: 584 bytes
import dateutil.parser, uuid

def parse_date(date_str):
    try:
        return dateutil.parser.parse(str(date_str))
    except:
        raise ValueError('Cannot parse %s as date.' % date_str.__class__.__name__)


def valid_uuid(id_):
    if id_ is None:
        return
    return str(uuid.UUID(str(id_)))


def isodate(date_):
    if date_ is None:
        return
    fmt = '%Y-%m-%d'
    return parse_date(date_).date().isoformat()


def isodatetime(datetime_):
    if datetime_ is None:
        return
    return parse_date(datetime_).isoformat()