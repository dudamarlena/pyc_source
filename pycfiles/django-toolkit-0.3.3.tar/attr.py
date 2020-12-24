# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/templatetags/attr.py
# Compiled at: 2013-03-19 00:20:36
import re
from django import template
from django.conf import settings
numeric_test = re.compile('^\\d+$')
register = template.Library()

@register.filter(name='getattribute')
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    if callable(getattr(value, arg)):
        return str(getattr(value, arg)())
    else:
        if hasattr(value, str(arg)):
            return getattr(value, arg)
        if hasattr(value, 'has_key') and value.has_key(arg):
            return value[arg]
        if numeric_test.match(str(arg)) and len(value) > int(arg):
            return value[int(arg)]
        if arg in dir(value):
            return getattr(value, arg)()
        return settings.TEMPLATE_STRING_IF_INVALID