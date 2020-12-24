# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/serializers/json.py
# Compiled at: 2019-02-14 00:35:17
"""
Serialize data to/from JSON
"""
from __future__ import absolute_import, unicode_literals
import datetime, decimal, json, sys, uuid
from django.core.serializers.base import DeserializationError
from django.core.serializers.python import Deserializer as PythonDeserializer, Serializer as PythonSerializer
from django.utils import six
from django.utils.deprecation import CallableBool
from django.utils.duration import duration_iso_string
from django.utils.functional import Promise
from django.utils.timezone import is_aware

class Serializer(PythonSerializer):
    """
    Convert a queryset to JSON.
    """
    internal_use_only = False

    def _init_options(self):
        if json.__version__.split(b'.') >= [b'2', b'1', b'3']:
            self.options.update({b'use_decimal': False})
        self._current = None
        self.json_kwargs = self.options.copy()
        self.json_kwargs.pop(b'stream', None)
        self.json_kwargs.pop(b'fields', None)
        if self.options.get(b'indent'):
            self.json_kwargs[b'separators'] = (',', ': ')
        self.json_kwargs.setdefault(b'cls', DjangoJSONEncoder)
        return

    def start_serialization(self):
        self._init_options()
        self.stream.write(b'[')

    def end_serialization(self):
        if self.options.get(b'indent'):
            self.stream.write(b'\n')
        self.stream.write(b']')
        if self.options.get(b'indent'):
            self.stream.write(b'\n')

    def end_object(self, obj):
        indent = self.options.get(b'indent')
        if not self.first:
            self.stream.write(b',')
            if not indent:
                self.stream.write(b' ')
        if indent:
            self.stream.write(b'\n')
        json.dump(self.get_dump_object(obj), self.stream, **self.json_kwargs)
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
        stream_or_string = stream_or_string.decode(b'utf-8')
    try:
        objects = json.loads(stream_or_string)
        for obj in PythonDeserializer(objects, **options):
            yield obj

    except GeneratorExit:
        raise
    except Exception as e:
        six.reraise(DeserializationError, DeserializationError(e), sys.exc_info()[2])


class DjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types and UUIDs.
    """

    def default(self, o):
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith(b'+00:00'):
                r = r[:-6] + b'Z'
            return r
        if isinstance(o, datetime.date):
            return o.isoformat()
        else:
            if isinstance(o, datetime.time):
                if is_aware(o):
                    raise ValueError(b"JSON can't represent timezone-aware times.")
                r = o.isoformat()
                if o.microsecond:
                    r = r[:12]
                return r
            if isinstance(o, datetime.timedelta):
                return duration_iso_string(o)
            if isinstance(o, decimal.Decimal):
                return str(o)
            if isinstance(o, uuid.UUID):
                return str(o)
            if isinstance(o, Promise):
                return six.text_type(o)
            if isinstance(o, CallableBool):
                return bool(o)
            return super(DjangoJSONEncoder, self).default(o)