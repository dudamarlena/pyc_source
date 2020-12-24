# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/urls.py
# Compiled at: 2012-02-02 00:29:51
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', url('^admin/', include(admin.site.urls)), url('^', include('tests.blogs.urls')), url('^accounts/login/$', 'django.contrib.auth.views.login', name='login'), url('^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'))