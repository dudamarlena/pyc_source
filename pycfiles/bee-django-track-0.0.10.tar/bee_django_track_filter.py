# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_track/templatetags/bee_django_track_filter.py
# Compiled at: 2018-11-12 01:54:46
__author__ = 'zhangyue'
from django import template
from django.conf import settings
from django.shortcuts import reverse
from bee_django_track.utils import get_user_name
register = template.Library()

@register.filter
def get_difference_abs(a, b):
    return abs(a - b)


@register.filter
def get_name_detail(user, show_detail=True):
    if not user:
        return None
    else:
        user_name = get_user_name(user)
        if not show_detail:
            return user_name
        if settings.USER_DETAIL_EX_LINK:
            link = "<a href='" + settings.USER_DETAIL_EX_LINK + user.id.__str__() + "/'>" + user_name + '</a>'
        else:
            link = user_name
        return link


@register.simple_tag
def get_record_link(cookie_user, record):
    if record.content_type.identity == 'user_leave':
        return record.get_link
    if record.content_type.identity == 'crm_fee':
        if cookie_user.has_perm('bee_django_crm.view_crm_preuser_fee'):
            return record.get_link
    else:
        return record.get_link