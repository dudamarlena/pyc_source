# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/DarkSector/Code/django-associations/demo/associations/templatetags/detailed_tags.py
# Compiled at: 2014-01-19 02:49:16
__author__ = 'DarkSector'
from django import template
register = template.Library()

@register.filter
def cut(value, arg):
    return value.replace(arg, '')


@register.filter
def replacewithappname(value, app_name):
    replaced_app_name = '/' + app_name + '/'
    return value.replace('^', replaced_app_name)


@register.filter
def cleanpattern(value):
    return value.replace('?P', '')