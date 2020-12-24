# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ikeda/.virtualenvs/rsyslog-monitor/django_spine/django-spine/examples/django_spine/spineapp/urls.py
# Compiled at: 2012-07-17 10:44:29
from django.conf.urls import patterns, url
import views
urlpatterns = patterns('', url('^examples', views.index, name='spineapp_index'), url('^examples/new', views.new, name='spineapp_new'), url('^examples/edit', views.edit, name='spineapp_edit'), url('^examples/show', views.show, name='spineapp_show'))