# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/templatetags/bee_django_crm_filter.py
# Compiled at: 2019-06-29 05:46:35
__author__ = 'zhangyue'
from datetime import datetime
from django import template
from bee_django_crm.utils import change_tz, LOCAL_TIMEZONE, get_referral_user_name_with_preuser, get_track_list, get_user_name
from bee_django_crm.utils import get_after_check_url as utils_get_after_check_url
from bee_django_crm.models import APPLICATION_QUESTION_INPUT_TYPE_CHOICES
from bee_django_crm.exports import filter_local_datetime
register = template.Library()

@register.filter
def get_referral_user_name(preuser, t=1):
    if t == 1:
        referral_user = preuser.referral_user1
    elif t == 2:
        referral_user = preuser.referral_user2
    else:
        referral_user = None
    if not referral_user:
        return
    else:
        return get_user_name(referral_user)


@register.filter
def get_preuser_track_list(preuser_id):
    return get_track_list(preuser_id)


@register.filter
def get_checked_user_name(user):
    return get_user_name(user)


@register.filter
def local_datetime(_datetime):
    return filter_local_datetime(_datetime)


@register.filter
def get_difference_abs(a, b):
    return abs(a - b)


@register.filter('get_html')
def get_html(application, id):
    if not application:
        return ''
    html = '<div>'
    question = application['question']
    is_required = question.is_required
    required_html = ''
    required_str = ''
    if is_required:
        required_html = 'required'
        required_str = "<span style='color:red'> ( 必填 ) </span>"
    question_name = question.name
    html += '<div>' + id.__str__() + ' . ' + question_name + required_str + '</div>'
    options = application['options']
    if question.input_type == APPLICATION_QUESTION_INPUT_TYPE_CHOICES[0][0]:
        html += "<div><input type='text' name='input_" + id.__str__() + "'" + required_html + ' ></div>'
    elif question.input_type == APPLICATION_QUESTION_INPUT_TYPE_CHOICES[1][0]:
        for option in options:
            html += "<input type='radio' name='input_" + id.__str__() + "' value='" + option.name + "'" + required_html + ' > ' + option.name + ' '

    elif question.input_type == APPLICATION_QUESTION_INPUT_TYPE_CHOICES[2][0]:
        html += "<select name='input_" + id.__str__() + "'>"
        for option in options:
            html += "<option  value='" + option.name + "'>" + option.name + '</option>'

        html += '</select>'
    elif question.input_type == APPLICATION_QUESTION_INPUT_TYPE_CHOICES[3][0]:
        for option in options:
            html += "<input type='checkbox' name='input_" + id.__str__() + "' value='" + option.name + "' bee_required=" + required_html + '> ' + option.name + '<br>'

    html += '</div>'
    return html


@register.filter('get_after_check_url')
def get_after_check_url(preuser_fee, user):
    if not user or not preuser_fee:
        return None
    url = utils_get_after_check_url(user, preuser_fee)
    if not url:
        return ''
    else:
        link = '<a href=' + url + '>后续操作</a>'
        return link