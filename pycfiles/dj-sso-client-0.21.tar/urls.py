# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fanfei/Documents/Code/dj-sso-client/example/ssoclient/ssoclient/urls.py
# Compiled at: 2015-03-11 17:56:24
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
urlpatterns = patterns('', url('^$', 'ssoclient.views.home', name='home'), url('^accounts/login/$', 'djssoclient.views.viewLogin'), url('^accounts/logout/$', auth_views.logout, {'next_page': '/'}), url('^myssoclient/', include('djssoclient.urls')))