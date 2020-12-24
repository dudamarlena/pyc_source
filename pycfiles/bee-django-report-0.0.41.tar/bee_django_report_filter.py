# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_report/templatetags/bee_django_report_filter.py
# Compiled at: 2019-10-18 03:16:38
__author__ = 'zhangyue'
from datetime import datetime
from django import template
from django.conf import settings
from django.contrib.auth import get_user_model
from bee_django_report.models import Report
from bee_django_report.utils import get_user_name
from bee_django_report.exports import get_class_name as exports_get_class_name
from bee_django_report.exports import get_section_name as exports_get_section_name
from bee_django_report.exports import filter_local_datetime
register = template.Library()
User = get_user_model()

@register.filter
def get_difference_abs(a, b):
    return abs(a - b)


@register.filter
def local_datetime(_datetime):
    return filter_local_datetime(_datetime)


@register.filter
def get_name_detail(user, show_detail=True):
    user_name = get_user_name(user)
    if not show_detail:
        return user_name
    if settings.USER_DETAIL_EX_LINK:
        link = "<a href='" + settings.USER_DETAIL_EX_LINK + user.id.__str__() + "/'>" + user_name + '</a>'
    else:
        link = user_name
    return link


@register.filter
def get_name_list_search(user, user_search_field):
    user_search_field = user_search_field.__str__()
    user_name = get_user_name(user)
    if settings.USER_LIST_EX_LINK:
        link = "<a href='" + settings.USER_LIST_EX_LINK + user_search_field + "'>" + user_name + '</a>'
    else:
        link = user_name
    return link


@register.filter
def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except:
        return

    return


@register.filter
def get_class_name(class_id):
    return exports_get_class_name(class_id)


@register.filter
def get_section_name(user_course_section_id):
    return exports_get_section_name(user_course_section_id)


@register.simple_tag
def get_user_current_course_section(user):
    user_course_section = Report.get_user_current_course_section(user)
    return user_course_section


@register.filter
def get_user_pass_section_count(user_course):
    return Report.get_user_pass_section_list(user_course).count()