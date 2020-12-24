# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/genes/templatetags/gene_extras.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 491 bytes
from django import template
register = template.Library()

@register.simple_tag
def dictKeyLookup(the_dict, key):
    return the_dict.get(key, '0')


@register.filter
def adjust_for_pagination(page, current):
    if current - page in (-1, -2, 1, 2):
        return True
    return False


register.filter('dictKeyLookup', dictKeyLookup)
register.filter('adjust_for_pagination', adjust_for_pagination)