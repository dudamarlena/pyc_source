# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/serializers/python.py
# Compiled at: 2018-07-11 18:15:30
"""
A Python "serializer". Doesn't do much serializing per se -- just converts to
and from basic Python data types (lists, dicts, strings, etc.). Useful as a basis for
other serializers.
"""
from __future__ import unicode_literals
from django.conf import settings
from django.core.serializers import base
from django.db import models, DEFAULT_DB_ALIAS
from django.utils.encoding import smart_text, is_protected_type
from django.utils import six

class Serializer(base.Serializer):
    """
    Serializes a QuerySet to basic Python objects.
    """
    internal_use_only = True

    def start_serialization(self):
        self._current = None
        self.objects = []
        return

    def end_serialization(self):
        pass

    def start_object(self, obj):
        self._current = {}

    def end_object(self, obj):
        self.objects.append(self.get_dump_object(obj))
        self._current = None
        return

    def get_dump_object(self, obj):
        return {b'pk': smart_text(obj._get_pk_val(), strings_only=True), 
           b'model': smart_text(obj._meta), 
           b'fields': self._current}

    def handle_field(self, obj, field):
        value = field._get_val_from_obj(obj)
        if is_protected_type(value):
            self._current[field.name] = value
        else:
            self._current[field.name] = field.value_to_string(obj)

    def handle_fk_field(self, obj, field):
        if self.use_natural_keys and hasattr(field.rel.to, b'natural_key'):
            related = getattr(obj, field.name)
            if related:
                value = related.natural_key()
            else:
                value = None
        else:
            value = getattr(obj, field.get_attname())
        self._current[field.name] = value
        return

    def handle_m2m_field(self, obj, field):
        if field.rel.through._meta.auto_created:
            if self.use_natural_keys and hasattr(field.rel.to, b'natural_key'):
                m2m_value = lambda value: value.natural_key()
            else:
                m2m_value = lambda value: smart_text(value._get_pk_val(), strings_only=True)
            self._current[field.name] = [ m2m_value(related) for related in getattr(obj, field.name).iterator() ]

    def getvalue(self):
        return self.objects


def Deserializer(object_list, **options):
    """
    Deserialize simple Python objects back into Django ORM instances.

    It's expected that you pass the Python objects themselves (instead of a
    stream or a string) to the constructor
    """
    db = options.pop(b'using', DEFAULT_DB_ALIAS)
    ignore = options.pop(b'ignorenonexistent', False)
    models.get_apps()
    for d in object_list:
        Model = _get_model(d[b'model'])
        data = {Model._meta.pk.attname: Model._meta.pk.to_python(d[b'pk'])}
        m2m_data = {}
        model_fields = Model._meta.get_all_field_names()
        for field_name, field_value in six.iteritems(d[b'fields']):
            if ignore and field_name not in model_fields:
                continue
            if isinstance(field_value, str):
                field_value = smart_text(field_value, options.get(b'encoding', settings.DEFAULT_CHARSET), strings_only=True)
            field = Model._meta.get_field(field_name)
            if field.rel and isinstance(field.rel, models.ManyToManyRel):
                if hasattr(field.rel.to._default_manager, b'get_by_natural_key'):

                    def m2m_convert(value):
                        if hasattr(value, b'__iter__') and not isinstance(value, six.text_type):
                            return field.rel.to._default_manager.db_manager(db).get_by_natural_key(*value).pk
                        else:
                            return smart_text(field.rel.to._meta.pk.to_python(value))

                else:
                    m2m_convert = lambda v: smart_text(field.rel.to._meta.pk.to_python(v))
                m2m_data[field.name] = [ m2m_convert(pk) for pk in field_value ]
            elif field.rel and isinstance(field.rel, models.ManyToOneRel):
                if field_value is not None:
                    if hasattr(field.rel.to._default_manager, b'get_by_natural_key'):
                        if hasattr(field_value, b'__iter__') and not isinstance(field_value, six.text_type):
                            obj = field.rel.to._default_manager.db_manager(db).get_by_natural_key(*field_value)
                            value = getattr(obj, field.rel.field_name)
                            if field.rel.to._meta.pk.rel:
                                value = value.pk
                        else:
                            value = field.rel.to._meta.get_field(field.rel.field_name).to_python(field_value)
                        data[field.attname] = value
                    else:
                        data[field.attname] = field.rel.to._meta.get_field(field.rel.field_name).to_python(field_value)
                else:
                    data[field.attname] = None
            else:
                data[field.name] = field.to_python(field_value)

        yield base.DeserializedObject(Model(**data), m2m_data)

    return


def _get_model(model_identifier):
    """
    Helper to look up a model from an "app_label.module_name" string.
    """
    try:
        Model = models.get_model(*model_identifier.split(b'.'))
    except TypeError:
        Model = None

    if Model is None:
        raise base.DeserializationError(b"Invalid model identifier: '%s'" % model_identifier)
    return Model