# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/python_dev/zabbix_dashboard/graphs/templatetags/pass_period.py
# Compiled at: 2014-10-03 06:55:37
from django import template
register = template.Library()

@register.filter
def get_img_period(obj, period):
    return obj.get_b64_img(period)