# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/africa/work/python/djnago-unisender/unisender/tests/test_urlconf.py
# Compiled at: 2014-07-07 04:51:37
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', url('^admin/', include(admin.site.urls)))