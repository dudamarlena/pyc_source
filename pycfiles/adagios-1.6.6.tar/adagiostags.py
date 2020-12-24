# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/adagios/adagios/../adagios/status/templatetags/adagiostags.py
# Compiled at: 2018-05-16 10:07:32
import math
from datetime import datetime, timedelta
from django import template
from django.utils.timesince import timesince
from django.utils.translation import ugettext as _
register = template.Library()

@register.filter('timestamp')
def timestamp(value):
    try:
        return datetime.fromtimestamp(value)
    except AttributeError:
        return ''


@register.filter('duration')
def duration(value):
    """ Used as a filter, returns a human-readable duration.
    'value' must be in seconds.
    """
    zero = datetime.min
    return timesince(zero, zero + timedelta(0, value))


@register.filter('hash')
def hash(h, key):
    return h[key]