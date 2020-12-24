# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-o463eux1/django-toolware/toolware/templatetags/rounder.py
# Compiled at: 2018-06-21 10:53:48
# Size of source mod 2**32: 776 bytes
import re
from django import template
from django.template import Node, TemplateSyntaxError
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def roundplus(number):
    """
    given an number, this fuction rounds the number as the following examples:
    87 -> 87, 100 -> 100+, 188 -> 100+, 999 -> 900+, 1001 -> 1000+, ...etc
    """
    num = str(number)
    if not num.isdigit():
        return num
    else:
        num = str(number)
        digits = len(num)
        rounded = '100+'
        if digits < 3:
            rounded = num
        else:
            if digits == 3:
                rounded = num[0] + '00+'
            else:
                if digits == 4:
                    rounded = num[0] + 'K+'
                else:
                    if digits == 5:
                        rounded = num[:1] + 'K+'
                    else:
                        rounded = '100K+'
        return rounded