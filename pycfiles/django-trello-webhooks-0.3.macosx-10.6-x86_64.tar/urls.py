# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-trello-webhooks/lib/python2.7/site-packages/trello_webhooks/urls.py
# Compiled at: 2014-11-26 17:25:12
from django.conf.urls import patterns, url
from trello_webhooks import views
urlpatterns = patterns(views, url('^(?P<auth_token>\\w+)/(?P<trello_model_id>\\w+)/$', views.api_callback, name='trello_callback_url'))