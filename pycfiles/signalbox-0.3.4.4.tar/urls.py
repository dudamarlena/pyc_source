# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/twiliobox/urls.py
# Compiled at: 2014-08-27 19:26:12
from django.conf.urls import patterns, url
import views
urlpatterns = patterns('', url('^outbound/initialise/(?P<observation_token>[\\w-]+)/$', views.initialise_call, {}, 'initialise_call'), url('^outbound/call/reply/(?P<reply_token>[\\w-]+)/question/(?P<question_index>[\\d+])/$', views.play, {}, 'play'), url('^inbound/call/?$', views.answerphone, {}, 'answerphone'), url('^inbound/sms/$', views.sms_callback, {}, 'sms_callback'))