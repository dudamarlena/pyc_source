# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/wiki/templatetags/sanitize.py
# Compiled at: 2009-01-08 09:11:51
from django import template
from softwarefabrica.django.wiki.sanitize import sanitize_html
register = template.Library()

def sanitize_html_filter(value):
    return sanitize_html(value)


register.filter('santize', sanitize_html_filter)