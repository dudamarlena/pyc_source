# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matt/Development/django-sms-gateway/sms/urls.py
# Compiled at: 2012-11-23 01:47:54
from django.conf.urls.defaults import patterns, url
import views
urlpatterns = patterns('', url('^status_postback/$', views.update_delivery_status, name='status_postback'), url('^reply_postback/$', views.handle_reply, name='reply_postback'), url('^status/([0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12})/$', views.get_message_set_status, name='messageset-status'))