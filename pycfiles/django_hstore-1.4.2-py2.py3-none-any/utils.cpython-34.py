# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/utils.py
# Compiled at: 2015-06-28 18:40:53
# Size of source mod 2**32: 2608 bytes
from __future__ import unicode_literals, absolute_import
from decimal import Decimal
from datetime import date, time, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.utils import six

def acquire_reference(reference):
    try:
        model, identifier = reference.split(':')
        module, sep, attr = model.rpartition('.')
        model = getattr(__import__(module, fromlist=(attr,)), attr)
        return model.objects.get(pk=identifier)
    except ObjectDoesNotExist:
        return
    except Exception:
        raise ValueError


def identify_instance(instance):
    model = type(instance)
    return '%s.%s:%s' % (model.__module__, model.__name__, instance.pk)


def serialize_references(references):
    refs = {}
    if references is None or isinstance(references, six.string_types):
        return {}
    if isinstance(references, dict):
        for key, instance in references.items():
            if not isinstance(instance, six.string_types):
                refs[key] = identify_instance(instance)
            else:
                refs[key] = instance
        else:
            return refs

    else:
        return references


def unserialize_references(references):
    refs = {}
    if references is None:
        return refs
    for key, reference in references.items():
        if isinstance(reference, six.string_types):
            refs[key] = acquire_reference(reference)
        else:
            refs[key] = reference
    else:
        return refs


def get_cast_for_param(value_annot, key):
    if not isinstance(value_annot, dict):
        return ''
    else:
        if value_annot[key] in (True, False):
            return '::boolean'
        if issubclass(value_annot[key], datetime):
            return '::timestamp'
        if issubclass(value_annot[key], date):
            return '::date'
        if issubclass(value_annot[key], time):
            return '::time'
        if issubclass(value_annot[key], six.integer_types):
            return '::bigint'
        if issubclass(value_annot[key], float):
            return '::float8'
        if issubclass(value_annot[key], Decimal):
            return '::numeric'
        return ''


def get_value_annotations(param):
    get_type = --- This code section failed: ---

 L.  82         0  LOAD_GLOBAL              isinstance
                3  LOAD_FAST                'v'
                6  LOAD_GLOBAL              bool
                9  CALL_FUNCTION_2       2  '2 positional, 0 named'
               12  POP_JUMP_IF_FALSE    19  'to 19'
               15  LOAD_FAST                'v'
               18  RETURN_END_IF_LAMBDA
             19_0  COME_FROM            12  '12'
               19  LOAD_GLOBAL              type
               22  LOAD_FAST                'v'
               25  CALL_FUNCTION_1       1  '1 positional, 0 named'
               28  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
    return dict((key, get_type(subvalue)) for key, subvalue in six.iteritems(param))