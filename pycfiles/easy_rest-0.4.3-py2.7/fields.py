# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/fields.py
# Compiled at: 2014-08-29 20:42:38
from rest_framework.fields import Field, WritableField
__author__ = 'mikhailturilin'

class PrimaryKeyReadOnlyField(Field):

    def to_native(self, value):
        return value and value.pk


class MetaField(Field):

    def __init__(self, label=None, help_text=None):
        super(MetaField, self).__init__('*', label, help_text)

    def to_native(self, obj):
        return {'app': type(obj)._meta.app_label, 
           'model': type(obj)._meta.model_name}


def enum_value(value):
    return value and value.value


class RestEnumField(WritableField):

    def __init__(self, enum=None, source=None, label=None, help_text=None, read_only=False, write_only=False, required=None, error_messages=None, widget=None, default=None, blank=None):
        self.enum = enum
        if not enum:
            read_only = True
        super(RestEnumField, self).__init__(source, label, help_text, read_only, write_only, required, [], error_messages, widget, default, blank)

    def to_native(self, value):
        return enum_value(value)

    def from_native(self, value):
        if not self.enum or value is None or value == '':
            return
        for m in self.enum:
            if value == m:
                return value
            if value == m.value or str(value) == str(m.value) or str(value) == str(m):
                return m

        raise ValueError('Unknown Enum value %s' % value)
        return