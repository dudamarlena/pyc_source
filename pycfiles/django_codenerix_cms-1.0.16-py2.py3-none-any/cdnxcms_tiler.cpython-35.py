# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_cms/templatetags/cdnxcms_tiler.py
# Compiled at: 2017-11-28 07:16:52
# Size of source mod 2**32: 1175 bytes
import json
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag(takes_context=True)
def cdnx_tiler(context, field):
    res = ''
    if 'tiles' in context:
        tiles = json.loads(context['tiles'])
        if field in tiles:
            res = tiles[field]['value']
    return mark_safe(res)


@register.simple_tag(takes_context=True)
def cdnx_tiler_type(context, json_tiler_type):
    return ''