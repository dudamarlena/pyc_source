# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii-blog/kii_blog/tests/urls.py
# Compiled at: 2014-11-24 05:36:44
# Size of source mod 2**32: 224 bytes
from django.conf.urls import patterns, url, include
from django.contrib import admin
urlpatterns = patterns('', (
 '^admin/', include(admin.site.urls)), url('^accounts/', include('django.contrib.auth.urls')))