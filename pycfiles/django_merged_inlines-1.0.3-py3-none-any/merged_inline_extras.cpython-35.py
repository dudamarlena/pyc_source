# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/merged_inlines/templatetags/merged_inline_extras.py
# Compiled at: 2019-01-31 18:03:56
# Size of source mod 2**32: 215 bytes
from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def is_empty(prefix):
    return '__prefix__' in prefix