# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/craig.williams/.virtualenvs/test-trans/lib/python2.7/site-packages/mezzanine_smartling/urls.py
# Compiled at: 2015-09-17 12:57:56
from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
 url('^smartling_callback/$', 'mezzanine_smartling.views.smartling_callback', name='smartling_callback')]