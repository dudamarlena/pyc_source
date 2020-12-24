# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\templatetags\nav.py
# Compiled at: 2020-01-08 02:37:40
# Size of source mod 2**32: 380 bytes
from django import template
from django_press.models import Page
register = template.Library()

@register.inclusion_tag('django_press/nav/main.html', takes_context=True)
def nav(context, core, **kwargs):
    nav_pages = Page.objects.filter(in_nav=True, publish=True).all()
    return {**{'nav_pages':nav_pages, 
     'core':core}, **kwargs}