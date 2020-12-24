# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/templatetags/bee_django_user_filter.py
# Compiled at: 2020-01-06 03:52:53
__author__ = 'zhangyue'
from datetime import datetime
from django import template
from django.contrib.auth.models import User, Group, Permission
from bee_django_user.exports import get_user_leave_status
register = template.Library()

@register.filter
def get_difference_abs(a, b):
    return abs(a - b)


@register.filter
def has_permission(group, permission_name):
    try:
        if group.permissions.get(codename=permission_name):
            return True
        else:
            return False

    except:
        return False


@register.filter
def has_manage(user):
    try:
        if user.userprofile.has_group('管理员') or user.userprofile.has_group('客服') or user.userprofile.has_group('助教'):
            return True
    except:
        return False

    return False


@register.simple_tag
def get_leave_status(user):
    status = get_user_leave_status(user)
    if status:
        return '请假中'


@register.simple_tag
def get_user_live_detail(user, time):
    try:
        from bee_django_course.models import UserLive
        if time == '本日':
            scope = 'day'
            offset = 0
        elif time == '昨日':
            scope = 'day'
            offset = -1
        elif time == '本周':
            scope = 'week'
            offset = 0
        elif time == '上周':
            scope = 'week'
            offset = -1
        elif time == '本月':
            scope = 'month'
            offset = 0
        elif time == '上月':
            scope = 'month'
            offset = -1
        else:
            return (0, 0, 0)
        return UserLive.get_user_live_detail([user], scope=scope, offset=offset)
    except Exception as e:
        return (0, 0, 0)


@register.filter
def get_class_coin(class_id):
    try:
        from bee_django_coin.models import OtherCoinCount
        record = OtherCoinCount.objects.get(coin_type__identity='user_class', coin_content_id=class_id)
        return record.count
    except:
        return

    return


@register.simple_tag
def get_group_has_permission(group_id, codename):
    group = Group.objects.get(id=group_id)
    has_permission = False
    if group.permissions.filter(codename=codename).exists():
        has_permission = True
    return has_permission