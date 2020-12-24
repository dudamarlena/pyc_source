# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/simiki/jinja_exts.py
# Compiled at: 2017-06-02 11:17:28
"""
Jinja2 custom filters and extensions
"""
import datetime, tzlocal
from simiki.compat import basestring
filters = [
 'rfc3339']

def rfc3339(dt_obj):
    """
    dt_obj: datetime object or string

    The filter use `datetime.datetime.isoformat()`, which is in ISO 8601
    format, not in RFC 3339 format, but they have a lot in common, so I used
    ISO 8601 format directly.
    """
    if isinstance(dt_obj, datetime.datetime):
        pass
    elif isinstance(dt_obj, basestring):
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'):
            try:
                dt_obj = datetime.datetime.strptime(dt_obj, fmt)
            except ValueError:
                pass
            else:
                break

        else:
            raise ValueError(('can not parse datetime {0}').format(dt_obj))

    else:
        raise ValueError(('{0} is not datetime object or string').format(dt_obj))
    if not dt_obj.tzinfo:
        tz = tzlocal.get_localzone()
        dt_obj = tz.localize(dt_obj)
    dt_obj = dt_obj.replace(microsecond=0)
    return dt_obj.isoformat()