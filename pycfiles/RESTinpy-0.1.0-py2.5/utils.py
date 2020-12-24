# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/RESTinpy/utils.py
# Compiled at: 2009-04-22 07:30:36
import re, simplejson
from datetime import datetime, date
__jsdateregexp__ = re.compile('"\\*\\*(new Date\\([0-9,]+\\))"')

class __JSONDateEncoder__(simplejson.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        return simplejson.JSONEncoder.default(self, obj)


def dumps(obj, ensure_ascii=True):
    """ A (simple)json wrapper that can wrap up python datetime and date
    objects into Javascript date objects.
    @param obj: the python object (possibly containing dates or datetimes) for
        (simple)json to serialize into JSON
    @param ensure_ascii: If ensure_ascii is false (default: True), then some 
        chunks written to fp may be unicode instances, subject to normal Python 
        str to unicode coercion rules.

    @returns: JSON version of the passed object
    """
    return __jsdateregexp__.sub('\\1', simplejson.dumps(obj, ensure_ascii=ensure_ascii, cls=__JSONDateEncoder__))