# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erik/src/django/archivis2/source/permissions_widget/templatetags/permissions_widget_tags.py
# Compiled at: 2015-01-29 09:03:01
from django import template
from django.utils.translation import ugettext
register = template.Library()

@register.filter
def get_item(d, key):
    return d.get(key, None)


@register.filter(name='translate')
def translate(text):
    return ugettext(text)