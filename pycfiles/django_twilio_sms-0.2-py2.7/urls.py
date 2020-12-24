# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\django_twilio_sms\urls.py
# Compiled at: 2013-06-19 17:43:49
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from .views import sms_status_callback_view
urlpatterns = patterns(b'', url(b'^callback/sent/(?P<pk>\\d+)/$', sms_status_callback_view, name=b'sms_status_callback'))