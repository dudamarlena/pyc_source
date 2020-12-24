# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kraken/Projects/websites/django-custard/custard/example/example/urls.py
# Compiled at: 2014-07-17 10:41:40
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', url('^admin/', include(admin.site.urls)))