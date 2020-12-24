# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/templatetags/bee_django_mission_filter.py
# Compiled at: 2018-11-30 03:07:58
__author__ = 'zhangyue'
from datetime import datetime
from django import template
from bee_django_mission.exports import filter_local_datetime
register = template.Library()

@register.filter
def get_difference_abs(a, b):
    return abs(a - b)


@register.filter
def multiple(a, b):
    return a * b


@register.filter
def get_int(a):
    return int(a)


@register.filter
def local_datetime(_datetime):
    return filter_local_datetime(_datetime)


@register.simple_tag
def get_mission_progress(user_mission):
    return user_mission.get_user_mission_progress()