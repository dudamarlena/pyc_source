# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\django\hris\adminlte\templatetags\assets.py
# Compiled at: 2017-05-17 00:17:55
# Size of source mod 2**32: 389 bytes
from django import template
from django.utils.safestring import mark_safe
from adminlte.Assets import Assets
register = template.Library()

@register.simple_tag(takes_context=True)
def css(context):
    CSS = Assets('css')
    return mark_safe(CSS.render())


@register.simple_tag(takes_context=True)
def js(context):
    JS = Assets('js')
    return mark_safe(JS.render())