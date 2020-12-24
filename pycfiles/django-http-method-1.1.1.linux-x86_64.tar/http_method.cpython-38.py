# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/django_http_method/templatetags/http_method.py
# Compiled at: 2020-05-04 11:30:43
# Size of source mod 2**32: 1044 bytes
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def http_get():
    return mark_safe('<input type="hidden" name="_method" value="GET" \\>')


@register.simple_tag
def http_post():
    return mark_safe('<input type="hidden" name="_method" value="POST" \\>')


@register.simple_tag
def http_head():
    return mark_safe('<input type="hidden" name="_method" value="HEAD" \\>')


@register.simple_tag
def http_put():
    return mark_safe('<input type="hidden" name="_method" value="PUT" \\>')


@register.simple_tag
def http_delete():
    return mark_safe('<input type="hidden" name="_method" value="DELETE" \\>')


@register.simple_tag
def http_patch():
    return mark_safe('<input type="hidden" name="_method" value="PATCH" \\>')


@register.simple_tag
def http_options():
    return mark_safe('<input type="hidden" name="_method" value="OPTIONS" \\>')


@register.simple_tag
def http_trace():
    return mark_safe('<input type="hidden" name="_method" value="TRACE" \\>')