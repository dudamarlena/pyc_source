# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/serializers/pyyaml.py
# Compiled at: 2018-07-11 18:15:30
"""
YAML serializer.

Requires PyYaml (http://pyyaml.org/), but that's checked for in __init__.
"""
import decimal, yaml
from io import StringIO
from django.db import models
from django.core.serializers.base import DeserializationError
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer
from django.utils import six

class DjangoSafeDumper(yaml.SafeDumper):

    def represent_decimal(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', str(data))


DjangoSafeDumper.add_representer(decimal.Decimal, DjangoSafeDumper.represent_decimal)

class Serializer(PythonSerializer):
    """
    Convert a queryset to YAML.
    """
    internal_use_only = False

    def handle_field(self, obj, field):
        if isinstance(field, models.TimeField) and getattr(obj, field.name) is not None:
            self._current[field.name] = str(getattr(obj, field.name))
        else:
            super(Serializer, self).handle_field(obj, field)
        return

    def end_serialization(self):
        yaml.dump(self.objects, self.stream, Dumper=DjangoSafeDumper, **self.options)

    def getvalue(self):
        return super(PythonSerializer, self).getvalue()


def Deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of YAML data.
    """
    if isinstance(stream_or_string, bytes):
        stream_or_string = stream_or_string.decode('utf-8')
    if isinstance(stream_or_string, six.string_types):
        stream = StringIO(stream_or_string)
    else:
        stream = stream_or_string
    try:
        for obj in PythonDeserializer(yaml.safe_load(stream), **options):
            yield obj

    except GeneratorExit:
        raise
    except Exception as e:
        raise DeserializationError(e)