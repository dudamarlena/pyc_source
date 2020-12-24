# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cezar/pythonprojects/django_dms/django_dms/app/dms/templatetags/dms.py
# Compiled at: 2018-04-02 09:20:27
# Size of source mod 2**32: 1131 bytes
import math, numbers
from django import template
register = template.Library()

@register.filter
def longitude(value):
    if not isinstance(value, numbers.Number):
        return value
    if value > 180 or value < -180:
        return value
    if value > 0:
        side = 'E'
    else:
        if value < 0:
            side = 'W'
        else:
            side = ''
    return get_degree(value, side)


@register.filter
def latitude(value):
    if not isinstance(value, numbers.Number):
        return value
    if value > 90 or value < -90:
        return value
    if value > 0:
        side = 'N'
    else:
        if value < 0:
            side = 'S'
        else:
            side = ''
    return get_degree(value, side)


def get_degree(value, side):
    result = '{d}° {m}\' {s}" {side}'
    abs_value = math.fabs(value)
    degrees = math.trunc(abs_value)
    minutes = math.trunc(abs_value * 60 % 60)
    seconds = round(abs_value * 3600 % 60)
    if seconds >= 60:
        seconds = 0
        minutes += 1
    minutes = str(minutes).zfill(2)
    seconds = str(seconds).zfill(2)
    return result.format(side=side, d=degrees, m=minutes, s=seconds)