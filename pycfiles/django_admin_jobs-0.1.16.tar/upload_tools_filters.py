# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\dipap\Desktop\Projects\Orfium\project\earnings-dashboard\upload_tools\templatetags\upload_tools_filters.py
# Compiled at: 2017-12-07 07:41:03
from django import template
from earnings_dashboard_project.settings import FIREBASE
register = template.Library()

@register.filter
def from_firebase_settings(key):
    try:
        return FIREBASE[key]
    except KeyError:
        return ''