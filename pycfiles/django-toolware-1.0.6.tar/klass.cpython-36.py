# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-o463eux1/django-toolware/toolware/templatetags/klass.py
# Compiled at: 2018-06-21 10:53:48
# Size of source mod 2**32: 335 bytes
from django import template
register = template.Library()

@register.filter
def class_name(instance):
    return instance.__class__.__name__


@register.filter
def app_name(instance):
    return instance._meta.app_label


@register.filter
def model_name(instance):
    return '{}.{}'.format(app_name(instance), class_name(instance))