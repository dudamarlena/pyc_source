# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/templatetags/bee_django_referral_filter.py
# Compiled at: 2019-08-23 06:04:51
__author__ = 'zhangyue'
from datetime import datetime
from django import template
from bee_django_referral.utils import get_user_name
from bee_django_referral.models import UserShareImage
register = template.Library()

@register.filter
def local_datetime(_datetime):
    return _datetime


@register.filter
def get_difference_abs(a, b):
    return abs(a - b)


@register.filter
def get_name(user):
    return get_user_name(user)


@register.filter
def get_user_qrcode_image_status(user_qrcode_image_id):
    try:
        user_image = UserShareImage.objects.get(id=user_qrcode_image_id)
        return user_image.status
    except:
        return

    return