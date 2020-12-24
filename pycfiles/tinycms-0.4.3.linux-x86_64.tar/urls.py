# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms/urls.py
# Compiled at: 2014-10-19 03:59:21
from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *
urlpatterns = patterns('', url('^(?P<url>.*)$', show_page, name='tinycms_show_page'))