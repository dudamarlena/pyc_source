# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fanfei/Documents/Code/dj-sso-server/example/djssoserverapp/djssoserverapp/urls.py
# Compiled at: 2015-03-09 19:19:05
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', url('^$', 'djssoserverapp.views.home', name='home'), url('^sso/', include('djssoserver.urls')), url('^login/$', 'django.contrib.auth.views.login', name='login'), url('^logout/$', 'django.contrib.auth.views.logout', name='logout'), url('^admin/', include(admin.site.urls)))