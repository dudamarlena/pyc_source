# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Jesus\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_exportadb\djmicrosip_exportadb\urls.py
# Compiled at: 2015-01-21 16:25:00
from django.conf.urls import patterns, url
from .views import index
urlpatterns = patterns('', (
 '^$', index))