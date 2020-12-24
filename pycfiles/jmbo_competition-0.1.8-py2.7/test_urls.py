# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/competition/test_urls.py
# Compiled at: 2013-09-27 03:42:43
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', (
 '^competition/', include('competition.urls')), (
 '^admin/', include(admin.site.urls)))