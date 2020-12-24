# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/blastplus/templatetags/extras.py
# Compiled at: 2020-01-27 10:34:51
# Size of source mod 2**32: 233 bytes
"""
Module extending django's functionality
"""
from django import template
register = template.Library()

@register.filter
def get_at_index(l, index):
    """Filter in template, returns object at index.   """
    return l[index]