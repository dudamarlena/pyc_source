# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../django-classnames-tag/django_classnames_tag/templatetags/classnames.py
# Compiled at: 2015-06-25 17:56:49
from django.template import Library
register = Library()

@register.simple_tag
def classnames(**kwargs):
    return (' ').join(key for key, value in kwargs.items() if value)


@register.filter
def gte(value, arg):
    return value >= arg


@register.filter
def gt(value, arg):
    return value > arg


@register.filter
def lte(value, arg):
    return value <= arg


@register.filter
def lt(value, arg):
    return value < arg


@register.filter
def eq(value, arg):
    return value == arg