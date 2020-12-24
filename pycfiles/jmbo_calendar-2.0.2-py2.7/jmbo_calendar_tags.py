# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_calendar/templatetags/jmbo_calendar_tags.py
# Compiled at: 2016-03-08 06:26:36
from django import template
register = template.Library()

@register.filter(name='join_titles')
def join_titles(value, delimiter=', '):
    return delimiter.join([ v.title for v in value ])