# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/70/_7dmwj6x12q099dhb0z0p7p80000gn/T/pycharm-packaging/djangorestframework/rest_framework/utils/representation.py
# Compiled at: 2018-05-14 04:48:23
# Size of source mod 2**32: 3094 bytes
"""
Helper functions for creating user-friendly representations
of serializer classes and serializer fields.
"""
from __future__ import unicode_literals
import re
from django.db import models
from django.utils.encoding import force_text
from django.utils.functional import Promise
from rest_framework.compat import unicode_repr

def manager_repr(value):
    model = value.model
    opts = model._meta
    names_and_managers = [(manager.name, manager) for manager in opts.managers]
    for manager_name, manager_instance in names_and_managers:
        if manager_instance == value:
            return '%s.%s.all()' % (model._meta.object_name, manager_name)

    return repr(value)


def smart_repr(value):
    if isinstance(value, models.Manager):
        return manager_repr(value)
    else:
        if isinstance(value, Promise):
            if value._delegate_text:
                value = force_text(value)
        value = unicode_repr(value)
        if value.startswith("u'"):
            if value.endswith("'"):
                return value[1:]
        value = re.sub(' at 0x[0-9A-Fa-f]{4,32}>', '>', value)
        return value


def field_repr(field, force_many=False):
    kwargs = field._kwargs
    if force_many:
        kwargs = kwargs.copy()
        kwargs['many'] = True
        kwargs.pop('child', None)
    else:
        arg_string = ', '.join([smart_repr(val) for val in field._args])
        kwarg_string = ', '.join(['%s=%s' % (key, smart_repr(val)) for key, val in sorted(kwargs.items())])
        if arg_string:
            if kwarg_string:
                arg_string += ', '
        if force_many:
            class_name = force_many.__class__.__name__
        else:
            class_name = field.__class__.__name__
    return '%s(%s%s)' % (class_name, arg_string, kwarg_string)


def serializer_repr(serializer, indent, force_many=None):
    ret = field_repr(serializer, force_many) + ':'
    indent_str = '    ' * indent
    if force_many:
        fields = force_many.fields
    else:
        fields = serializer.fields
    for field_name, field in fields.items():
        ret += '\n' + indent_str + field_name + ' = '
        if hasattr(field, 'fields'):
            ret += serializer_repr(field, indent + 1)
        else:
            if hasattr(field, 'child'):
                ret += list_repr(field, indent + 1)
            else:
                if hasattr(field, 'child_relation'):
                    ret += field_repr((field.child_relation), force_many=(field.child_relation))
                else:
                    ret += field_repr(field)

    if serializer.validators:
        ret += '\n' + indent_str + 'class Meta:'
        ret += '\n' + indent_str + '    validators = ' + smart_repr(serializer.validators)
    return ret


def list_repr(serializer, indent):
    child = serializer.child
    if hasattr(child, 'fields'):
        return serializer_repr(serializer, indent, force_many=child)
    else:
        return field_repr(serializer)