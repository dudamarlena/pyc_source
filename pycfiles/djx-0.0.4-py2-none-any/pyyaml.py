# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/serializers/pyyaml.py
# Compiled at: 2019-02-14 00:35:17
"""
YAML serializer.

Requires PyYaml (http://pyyaml.org/), but that's checked for in __init__.
"""
import collections, decimal, sys
from io import StringIO
import yaml
from django.core.serializers.base import DeserializationError
from django.core.serializers.python import Deserializer as PythonDeserializer, Serializer as PythonSerializer
from django.db import models
from django.utils import six
try:
    from yaml import CSafeLoader as SafeLoader
    from yaml import CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeLoader, SafeDumper

class DjangoSafeDumper(SafeDumper):

    def represent_decimal(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', str(data))

    def represent_ordered_dict(self, data):
        return self.represent_mapping('tag:yaml.org,2002:map', data.items())


DjangoSafeDumper.add_representer(decimal.Decimal, DjangoSafeDumper.represent_decimal)
DjangoSafeDumper.add_representer(collections.OrderedDict, DjangoSafeDumper.represent_ordered_dict)

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
        for obj in PythonDeserializer(yaml.load(stream, Loader=SafeLoader), **options):
            yield obj

    except GeneratorExit:
        raise
    except Exception as e:
        six.reraise(DeserializationError, DeserializationError(e), sys.exc_info()[2])