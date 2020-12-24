# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/parkners_new/avishan/templatetags/avishan_tags.py
# Compiled at: 2020-03-01 03:58:14
# Size of source mod 2**32: 767 bytes
from django import template
from django.db import models
from avishan.models import AvishanModel
register = template.Library()

@register.filter
def translator(value: str) -> str:
    data = {'phone':'شماره همراه', 
     'email':'ایمیل'}
    try:
        return data[value.lower()]
    except KeyError:
        return value


@register.filter
def leading_zeros(value, desired_digits):
    """
    Given an integer, returns a string representation, padded with [desired_digits] zeros.
    """
    num_zeros = int(desired_digits) - len(str(value))
    padded_value = []
    while num_zeros >= 1:
        padded_value.append('0')
        num_zeros = num_zeros - 1

    padded_value.append(str(value))
    return ''.join(padded_value)