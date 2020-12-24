# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/feedview/templatetags/feedtags.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import calendar, datetime
from django import template
register = template.Library()

@register.filter
def feeddate(datetuple):
    """
    A filter that converts the date tuple provided from feedparser into
    a datetime object.
    """
    return datetime.datetime.utcfromtimestamp(calendar.timegm(datetuple))