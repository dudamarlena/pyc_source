# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fanfei/Documents/Code/dj-mongo-reader/example/sampleapp/sampleapp/urls.py
# Compiled at: 2015-03-05 00:14:00
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', url('^$', 'sampleapp.views.readme', name='home'), url('^query/$', 'sampleapp.views.query'), url('^mongo/', include('djmongoreader.urls')), url('^admin/', include(admin.site.urls)))