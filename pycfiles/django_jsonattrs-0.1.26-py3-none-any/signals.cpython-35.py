# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-jsonattrs/jsonattrs/signals.py
# Compiled at: 2018-06-01 06:45:54
# Size of source mod 2**32: 1427 bytes
import functools
from django.core.exceptions import FieldError
from .fields import JSONAttributes, JSONAttributeField

def attribute_model_pre_save(sender, **kwargs):
    kwargs['instance']._attr_field._pre_save_selector_check()


def fixup_instance(sender, **kwargs):
    """
    Cache JSONAttributes data on instance and vice versa for convenience.
    """
    instance = kwargs['instance']
    for model_field in instance._meta.fields:
        if not isinstance(model_field, JSONAttributeField):
            pass
        else:
            if hasattr(instance, '_attr_field'):
                raise FieldError('multiple JSONAttributeField fields: only one is allowed per model!')
            field_name = model_field.name
            attrs = getattr(instance, field_name)
            if not isinstance(attrs, JSONAttributes):
                setattr(instance, field_name, JSONAttributes(attrs))
                attrs = getattr(instance, field_name)
            attrs._instance = instance
            attrs._get_from_instance = functools.partial(getattr, instance, field_name)
            instance._attr_field = attrs

    if not hasattr(instance, '_attr_field'):
        raise FieldError('missing JSONAttributeField field in fixup_instance decorator')