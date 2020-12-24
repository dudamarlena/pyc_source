# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/xacce/addit/Projects/inventory/venv/local/lib/python2.7/site-packages/djxami/templatetags/djxami.py
# Compiled at: 2016-02-08 09:41:09
from django.shortcuts import render_to_response
from django.template import Library
from django.conf import settings
from django.utils.safestring import mark_safe
register = Library()

@register.inclusion_tag('djxami/init.html')
def djxami_init():
    return {'first_query_pause': getattr(settings, 'DJXAMI_FIRST_QUERY_PAUSE', 1000), 
       'queries_interval': getattr(settings, 'DJXAMI_QUERIES_INTERVAL', 5000), 
       'stream_interval': getattr(settings, 'DJXAMI_STREAM_INVETRAL', 1000)}