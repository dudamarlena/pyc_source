# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/action/appWine/redWine/templatetags/filters.py
# Compiled at: 2014-03-12 16:29:00
from django.template import Library
register = Library()

@register.filter
def get_range(value):
    return range(value)