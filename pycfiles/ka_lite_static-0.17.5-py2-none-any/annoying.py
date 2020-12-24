# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-annoying/annoying/templatetags/annoying.py
# Compiled at: 2018-07-11 18:15:31
import django
from django import template
from smart_if import smart_if
register = template.Library()
try:
    if int(django.get_version()[-5:]) < 11806:
        register.tag('if', smart_if)
except ValueError:
    pass