# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Data/Users/steven.skoczen/.virtualenvs/project_tomo/src/heroku-web-autoscale/heroku_web_autoscale/urls.py
# Compiled at: 2012-03-05 16:40:03
from django.conf.urls.defaults import patterns, url
from heroku_web_autoscale import views
urlpatterns = patterns('', url('heartbeat', views.heartbeat, name='heartbeat'))