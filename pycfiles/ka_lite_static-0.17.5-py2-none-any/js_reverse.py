# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-js-reverse/django_js_reverse/templatetags/js_reverse.py
# Compiled at: 2018-07-11 18:15:31
from django import template
from django_js_reverse.views import urls_js
register = template.Library()

@register.simple_tag(takes_context=True)
def js_reverse_inline(context):
    """
    Outputs a string of javascript that can generate URLs via the use
    of the names given to those URLs.
    """
    return urls_js(context.get('request'))