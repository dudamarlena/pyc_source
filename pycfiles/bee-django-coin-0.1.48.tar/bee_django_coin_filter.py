# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/templatetags/bee_django_coin_filter.py
# Compiled at: 2018-10-18 03:19:02
__author__ = 'zhangyue'
from django import template
from django.conf import settings
from bee_django_coin.exports import filter_local_datetime, get_user_coin
from bee_django_coin.utils import get_user_name
register = template.Library()

@register.filter
def local_datetime(_datetime):
    return filter_local_datetime(_datetime)


@register.filter
def get_difference_abs(a, b):
    return abs(a - b)


@register.filter
def get_coin(user):
    coin = get_user_coin(user)
    return coin


@register.filter
def get_name_detail(user, show_detail=True):
    if not user:
        return ''
    user_name = get_user_name(user)
    if not show_detail:
        return user_name
    if settings.USER_DETAIL_EX_LINK:
        link = "<a href='" + settings.USER_DETAIL_EX_LINK + user.id.__str__() + "/'>" + user_name + '</a>'
    else:
        link = user_name
    return link


@register.filter
def get_created_by_user_name(user):
    if not user:
        return settings.COIN_DEFAULT_NAME
    return get_name_detail(user, False)