# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/templatetags/bee_django_exam_filter.py
# Compiled at: 2018-11-23 00:44:17
__author__ = 'zhangyue'
from datetime import datetime
from django import template
from django.shortcuts import get_object_or_404, reverse
from bee_django_exam.utils import get_user_name, get_user_exam_record
from bee_django_exam.exports import get_user_icon
register = template.Library()

@register.filter
def get_difference_abs(a, b):
    return abs(a - b)


@register.filter
def get_record_user_name(user):
    if not user:
        return None
    else:
        return get_user_name(user.id)


@register.filter
def get_icon(user_id):
    return get_user_icon(user_id)


@register.simple_tag
def get_user_exam_record_link(user):
    record = get_user_exam_record(user, -1)
    if record:
        return reverse('bee_django_exam:user_exam_notice', kwargs={'user_record_id': record.id})
    else:
        return ''