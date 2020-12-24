# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cyberj/src/python/vtenv2.6/lib/python2.6/site-packages/signature/utils.py
# Compiled at: 2011-06-14 07:22:27
import datetime
from django import forms
from django.core.serializers.pyyaml import Serializer as DjangoYAMLEncoder
from django.core.serializers.pyyaml import DjangoSafeDumper
from django.core import serializers
from django.db import models
from django.forms import fields
from StringIO import StringIO
from django.db import models
from django.utils.encoding import smart_str, smart_unicode
from django.utils import datetime_safe
import yaml
from hashlib import sha512

class SMIMESerializer(DjangoYAMLEncoder):
    """
    Serializer for signatures
    """

    def serialize(self, queryset, **options):
        """
        Serialize a queryset.
        """
        self.options = options
        self.stream = options.get('stream', StringIO())
        self.selected_fields = options.get('fields')
        self.use_natural_keys = options.get('use_natural_keys', False)
        self.start_serialization()
        for obj in queryset:
            self.start_object(obj)
            for field in obj._meta.local_fields:
                if field.serialize:
                    if field.rel is None:
                        if self.selected_fields is None or field.attname in self.selected_fields:
                            self.handle_field(obj, field)
                    elif self.selected_fields is None or field.attname[:-3] in self.selected_fields:
                        self.handle_fk_field(obj, field)

            for field in obj._meta.many_to_many:
                if field.serialize:
                    if self.selected_fields is None or field.attname in self.selected_fields:
                        self.handle_m2m_field(obj, field)

            self.end_object(obj)

        self.end_serialization()
        return self.getvalue()

    def handle_field(self, obj, field):
        if isinstance(field, models.TimeField) and getattr(obj, field.name) is not None:
            self._current[field.name] = str(getattr(obj, field.name))
        elif isinstance(field, models.FileField) and getattr(obj, field.name) is not None:
            f = getattr(obj, field.name).open()
            if not f:
                f = open(getattr(obj, field.name).name, 'rb')
            f.seek(0)
            sha = sha512()
            data = f.read(512)
            while len(data):
                sha.update(data)
                data = f.read(512)

            self._current[field.name] = str(sha.hexdigest())
        else:
            super(SMIMESerializer, self).handle_field(obj, field)
        return

    def handle_fk_field(self, obj, field):
        related = getattr(obj, field.name)
        if related is not None:
            if self.use_natural_keys and hasattr(related, 'natural_key'):
                related = related.natural_key()
            elif field.rel.field_name == related._meta.pk.name:
                related = related._get_pk_val()
            else:
                related = smart_unicode(getattr(related, field.rel.field_name), strings_only=True)
        self._current[field.name] = related
        return

    def end_serialization(self):
        self.options.pop('stream', None)
        self.options.pop('fields', None)
        self.options.pop('use_natural_keys', None)
        yaml.dump(self.objects, self.stream, Dumper=DjangoSafeDumper, **self.options)
        return


def serialize(obj, use_natural_keys=False):
    """
    """
    data = [
     obj]
    serializer = SMIMESerializer()
    serialized = serializer.serialize(data, use_natural_keys=use_natural_keys)
    return serialized