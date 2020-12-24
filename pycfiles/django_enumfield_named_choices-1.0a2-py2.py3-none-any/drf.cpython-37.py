# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /pmc/Work/kolotev/0git/.github/django-enumfield-named-choices/django_enumfield_named_choices/contrib/drf.py
# Compiled at: 2019-08-22 14:25:46
# Size of source mod 2**32: 1284 bytes
import django.utils.translation as _
from rest_framework import serializers

class EnumField(serializers.ChoiceField):
    default_error_messages = {'invalid_choice': _('"{input}" is not a valid choice.')}

    def __init__(self, enum, **kwargs):
        self.enum = enum
        choices = ((self.get_choice_value(enum_value), enum_value.label) for _, enum_value in enum.choices())
        (super().__init__)(choices, **kwargs)

    def get_choice_value(self, enum_value):
        return enum_value.value

    def to_internal_value(self, data):
        if isinstance(data, str):
            if data.isdigit():
                data = int(data)
        try:
            value = self.enum.get(data).value
        except AttributeError:
            if not self.required:
                raise serializers.SkipField()
            self.fail('invalid_choice', input=data)

        return value

    def to_representation(self, value):
        enum_value = self.enum.get(value)
        if enum_value:
            return self.get_choice_value(enum_value)


class NamedEnumField(EnumField):

    class Meta:
        swagger_schema_fields = {'type': 'string'}

    def get_choice_value(self, enum_value):
        return enum_value.name.lower()