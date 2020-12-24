# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/paulmitchell-gears/git/peoplewise-enable/env/lib/python3.5/site-packages/serialization_spec/plugins.py
# Compiled at: 2019-11-18 04:56:35
# Size of source mod 2**32: 2129 bytes
from typing import Dict, Any
from django.db.models import Count
from .serialization import SerializationSpecPlugin
from .utils import extend_queryset

class SerializationSpecPluginModel(SerializationSpecPlugin):
    __doc__ = ' Derive from this if you want to apply model a function '
    kwargs = {}

    def __init__(self, relation):
        self.relation = relation

    def get_name(self):
        return '%s_%s' % (self.relation, self.name)

    def modify_queryset(self, queryset):
        return queryset.annotate(**{self.get_name(): self.model_function(self.relation, **self.kwargs)})

    def get_value(self, instance):
        return getattr(instance, self.get_name())


class CountOf(SerializationSpecPluginModel):
    name = 'count'
    model_function = Count
    kwargs = {'distinct': True}


class Exists(CountOf):

    def get_value(self, instance):
        return super().get_value(instance) > 0


class Requires(SerializationSpecPlugin):
    __doc__ = ' Use this for a property which needs some underlying fields to be loaded '

    def __init__(self, fields):
        self.fields = fields

    def modify_queryset(self, queryset):
        extend_queryset(queryset, self.fields)
        return queryset

    def get_value(self, instance):
        return getattr(instance, self.key)


class Transform(SerializationSpecPlugin):
    __doc__ = ' Derive from this if you want to transform underlying data '

    def modify_queryset(self, queryset):
        extend_queryset(queryset, {self.key})
        return queryset

    def get_value(self, instance):
        return self.transform(getattr(instance, self.key))

    def transform(self, value):
        raise NotImplementedError


class MethodCall(SerializationSpecPlugin):

    def __init__(self, name, required_fields=None):
        self.name = name
        self.required_fields = set(required_fields) or {}

    def modify_queryset(self, queryset):
        extend_queryset(queryset, self.required_fields)
        return queryset

    def get_value(self, instance):
        return getattr(instance, self.name)()