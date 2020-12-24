# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/encoders.py
# Compiled at: 2018-12-26 05:23:19
from __future__ import absolute_import, unicode_literals
import datetime, decimal, json, uuid, six

class JSONEncoder(json.JSONEncoder):

    def is_aware(self, value):
        return value.utcoffset() is not None

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            representation = obj.isoformat()
            if representation.endswith(b'+00:00'):
                representation = representation[:-6] + b'Z'
            return representation
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, datetime.time):
            if self.is_aware(obj):
                raise ValueError(b"JSON can't represent timezone-aware times.")
            representation = obj.isoformat()
            return representation
        if isinstance(obj, datetime.timedelta):
            return six.text_type(obj.total_seconds())
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, uuid.UUID):
            return six.text_type(obj)
        if isinstance(obj, six.binary_type):
            return obj.decode(b'utf-8')
        if hasattr(obj, b'tolist'):
            return obj.tolist()
        if hasattr(obj, b'__getitem__'):
            try:
                return dict(obj)
            except Exception:
                pass

        elif hasattr(obj, b'__iter__'):
            return tuple(item for item in obj)
        return super(JSONEncoder, self).default(obj)