# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/django_responsive_viewer/urls.py
# Compiled at: 2015-05-12 04:30:01
__author__ = 'tim'
from django.conf.urls import patterns, include, url
from .views import responsive_listing
urlpatterns = patterns('', url('^$', responsive_listing))