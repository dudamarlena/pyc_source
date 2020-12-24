# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gthomas/dev/management-server/managementserver/django_sql_dashboards/templatetags/sql_dashboards_tags.py
# Compiled at: 2014-08-26 05:59:56
from django import template
from django.utils.numberformat import format
register = template.Library()

@register.filter
def floatdot(value, decimal_pos=4):
    return format(value, '.', decimal_pos)


floatdot.is_safe = True