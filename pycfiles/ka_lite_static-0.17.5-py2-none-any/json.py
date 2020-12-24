# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/serializers/json.py
# Compiled at: 2018-07-11 18:15:30
"""
Serialize data to/from JSON
"""
from __future__ import absolute_import
import datetime, decimal, json
from django.core.serializers.base import DeserializationError
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer
from django.utils import six
from django.utils.timezone import is_aware

class Serializer(PythonSerializer):
    """
    Convert a queryset to JSON.
    """
    internal_use_only = False

    def start_serialization(self):
        if json.__version__.split('.') >= ['2', '1', '3']:
            self.options.update({'use_decimal': False})
        self._current = None
        self.json_kwargs = self.options.copy()
        self.json_kwargs.pop('stream', None)
        self.json_kwargs.pop('fields', None)
        self.stream.write('[')
        return

    def end_serialization(self):
        if self.options.get('indent'):
            self.stream.write('\n')
        self.stream.write(']')
        if self.options.get('indent'):
            self.stream.write('\n')

    def end_object(self, obj):
        indent = self.options.get('indent')
        if not self.first:
            self.stream.write(',')
            if not indent:
                self.stream.write(' ')
        if indent:
            self.stream.write('\n')
        json.dump(self.get_dump_object(obj), self.stream, cls=DjangoJSONEncoder, **self.json_kwargs)
        self._current = None
        return

    def getvalue(self):
        return super(PythonSerializer, self).getvalue()


def Deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of JSON data.
    """
    if not isinstance(stream_or_string, (bytes, six.string_types)):
        stream_or_string = stream_or_string.read()
    if isinstance(stream_or_string, bytes):
        stream_or_string = stream_or_string.decode('utf-8')
    try:
        objects = json.loads(stream_or_string)
        for obj in PythonDeserializer(objects, **options):
            yield obj

    except GeneratorExit:
        raise
    except Exception as e:
        raise DeserializationError(e)


class DjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """

    def default(self, o):
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        if isinstance(o, datetime.date):
            return o.isoformat()
        else:
            if isinstance(o, datetime.time):
                if is_aware(o):
                    raise ValueError("JSON can't represent timezone-aware times.")
                r = o.isoformat()
                if o.microsecond:
                    r = r[:12]
                return r
            if isinstance(o, decimal.Decimal):
                return str(o)
            return super(DjangoJSONEncoder, self).default(o)


DateTimeAwareJSONEncoder = DjangoJSONEncoder