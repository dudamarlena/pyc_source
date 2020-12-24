# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/golm_admin/templatetags/golem_extras.py
# Compiled at: 2018-04-15 14:00:29
# Size of source mod 2**32: 416 bytes
from django import template
register = template.Library()

@register.filter(name='get')
def get(d, k):
    return d.get(k, None)


@register.filter(name='entity')
def entity(d, k):
    v = d.get(k, None) if d else None
    if v:
        if len(v):
            return v[0].get('value')


@register.filter(name='duration')
def duration(seconds):
    if not seconds:
        return ''
    else:
        return '{} ms'.format(int(seconds * 1000))