# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cache_headers/tests/urls.py
# Compiled at: 2017-11-17 03:42:00
from django.conf.urls import include, url
from django.views.generic import TemplateView
from cache_headers.tests import views
urlpatterns = [
 url('^mylogin/$', views.mylogin, name='mylogin'),
 url('^mylogout/$', views.mylogout, name='mylogout'),
 url('^all-users/$', TemplateView.as_view(template_name='tests/view.html'), name='all-users'),
 url('^anonymous-only/$', TemplateView.as_view(template_name='tests/view.html'), name='anonymous-only'),
 url('^anonymous-and-authenticated/$', TemplateView.as_view(template_name='tests/view.html'), name='anonymous-and-authenticated'),
 url('^per-user/$', TemplateView.as_view(template_name='tests/view.html'), name='per-user'),
 url('^custom-policy/$', TemplateView.as_view(template_name='tests/view.html'), name='custom-policy'),
 url('^home/$', TemplateView.as_view(template_name='tests/view.html'), name='home')]