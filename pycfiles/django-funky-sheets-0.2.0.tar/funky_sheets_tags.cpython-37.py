# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/trco/github/django-funky-sheets/funky_sheets/templatetags/funky_sheets_tags.py
# Compiled at: 2019-10-21 16:33:44
# Size of source mod 2**32: 223 bytes
from django import template
register = template.Library()

@register.filter
def widget_type(field):
    return field.field.widget.__class__.__name__


@register.filter
def int_list(field):
    return list(map(int, field))