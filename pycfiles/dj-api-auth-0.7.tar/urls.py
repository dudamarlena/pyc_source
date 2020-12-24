# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fanfei/Documents/Code/dj-api-auth/example/djapp/djapp/urls.py
# Compiled at: 2015-03-08 17:00:32
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', url('^$', 'djapp.views.index', name='home'), url('^api/', include('djapp.apiurls')), url('^admin/', include(admin.site.urls)))