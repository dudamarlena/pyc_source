# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jsonfield2/utils.py
# Compiled at: 2015-06-02 23:09:38
# Size of source mod 2**32: 1855 bytes
import datetime, decimal, types, json, uuid
from django.db.models.query import QuerySet
from django.utils import six, timezone
from django.utils.encoding import force_text
from django.utils.functional import Promise
from django.core.serializers.json import DjangoJSONEncoder

class JSONEncoder(DjangoJSONEncoder):

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        if isinstance(obj, datetime.timedelta):
            return six.text_type(total_seconds(obj))
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, uuid.UUID):
            return six.text_type(obj)
        if isinstance(obj, QuerySet):
            return tuple(obj)
        if hasattr(obj, 'tolist'):
            return obj.tolist()
        if hasattr(obj, '__getitem__'):
            try:
                return dict(obj)
            except:
                pass

        elif hasattr(obj, '__iter__'):
            return tuple(item for item in obj)
        return super(JSONEncoder, self).default(obj)


def default(o):
    if hasattr(o, 'to_json'):
        return o.to_json()
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, datetime.datetime):
        if o.tzinfo:
            return o.strftime('%Y-%m-%dT%H:%M:%S%z')
        return o.strftime('%Y-%m-%dT%H:%M:%S')
    if isinstance(o, datetime.date):
        return o.strftime('%Y-%m-%d')
    if isinstance(o, datetime.time):
        if o.tzinfo:
            return o.strftime('%H:%M:%S%z')
        return o.strftime('%H:%M:%S')
    if isinstance(o, set):
        return list(o)
    raise TypeError(repr(o) + ' is not JSON serializable')