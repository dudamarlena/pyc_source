# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gint/Dokumenty/report/app/templado/templatetags/active.py
# Compiled at: 2015-02-23 07:14:16
from django import template
from django.core.urlresolvers import reverse
register = template.Library()

@register.simple_tag
def is_active(request, urls):
    if request.path in (reverse(url) for url in urls.split()):
        return 'active'
    return ''