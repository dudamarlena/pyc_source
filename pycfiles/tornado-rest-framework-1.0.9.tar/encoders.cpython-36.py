# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/70/_7dmwj6x12q099dhb0z0p7p80000gn/T/pycharm-packaging/djangorestframework/rest_framework/utils/encoders.py
# Compiled at: 2018-05-14 04:48:23
# Size of source mod 2**32: 2574 bytes
"""
Helper classes for parsers.
"""
from __future__ import absolute_import, unicode_literals
import datetime, decimal, json, uuid
from django.db.models.query import QuerySet
from django.utils import six, timezone
from django.utils.encoding import force_text
from django.utils.functional import Promise
from rest_framework.compat import coreapi

class JSONEncoder(json.JSONEncoder):
    __doc__ = '\n    JSONEncoder subclass that knows how to encode date/time/timedelta,\n    decimal types, generators and other basic python objects.\n    '

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        else:
            if isinstance(obj, datetime.datetime):
                representation = obj.isoformat()
                if representation.endswith('+00:00'):
                    representation = representation[:-6] + 'Z'
                return representation
            elif isinstance(obj, datetime.date):
                return obj.isoformat()
            elif isinstance(obj, datetime.time):
                if timezone:
                    if timezone.is_aware(obj):
                        raise ValueError("JSON can't represent timezone-aware times.")
                    representation = obj.isoformat()
                    return representation
                else:
                    if isinstance(obj, datetime.timedelta):
                        return six.text_type(obj.total_seconds())
                    else:
                        if isinstance(obj, decimal.Decimal):
                            return float(obj)
                        else:
                            if isinstance(obj, uuid.UUID):
                                return six.text_type(obj)
                            if isinstance(obj, QuerySet):
                                return tuple(obj)
                        if isinstance(obj, six.binary_type):
                            return obj.decode('utf-8')
                    if hasattr(obj, 'tolist'):
                        return obj.tolist()
                if coreapi is not None and isinstance(obj, (coreapi.Document, coreapi.Error)):
                    raise RuntimeError('Cannot return a coreapi object from a JSON view. You should be using a schema renderer instead for this view.')
            else:
                if hasattr(obj, '__getitem__'):
                    try:
                        return dict(obj)
                    except Exception:
                        pass

                elif hasattr(obj, '__iter__'):
                    return tuple(item for item in obj)
            return super(JSONEncoder, self).default(obj)