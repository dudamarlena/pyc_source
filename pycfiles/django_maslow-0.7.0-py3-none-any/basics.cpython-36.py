# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/canary/Development/django-maslow/maslow/templatetags/basics.py
# Compiled at: 2016-06-12 03:41:44
# Size of source mod 2**32: 977 bytes
from django.utils.safestring import mark_safe
from django.template import Library
import json
register = Library()

def jsonify(querydict, key):
    return json.dumps(mark_safe(list(querydict.values_list(key, flat=True))))


def listify(querydict, key):
    return mark_safe(list(querydict.values_list(key, flat=True)))


@register.filter
def subtract(value, arg):
    try:
        return value - arg
    except:
        return 0


@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except:
        return 0


@register.filter
def divide(value, arg):
    try:
        return value / arg
    except:
        return 0


register.filter('jsonify', jsonify)
register.filter('listify', listify)
jsonify.is_safe = True
register.filter('subtract', subtract)
register.filter('multiply', multiply)
register.filter('divide', divide)