# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/sentry_tracpost/urls.py
# Compiled at: 2012-08-16 11:18:15
from django.conf.urls.defaults import *
from sentry_tracpost.plugin import start
uuid_re = '\\b[A-F0-9]{8}(?:-[A-F0-9]{4}){3}-[A-Z0-9]{12}\\b|$'
urlpatterns = patterns('', url('^tracpost/(?P<group_id>\\d+)/$', 'start', name='send_message'))