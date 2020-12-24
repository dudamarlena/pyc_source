# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia/django/downloader/urls.py
# Compiled at: 2010-04-27 16:27:26
"""Urls for emencia.django.downloader"""
from django.conf.urls.defaults import *
from emencia.django.downloader.views import get_file, upload, upload_ok
urlpatterns = patterns('', url('^upload/(?P<slug>[-\\w]+)/$', upload_ok, name='upload_ok'), url('^(?P<slug>[-\\w]+)/$', get_file, name='get_file'), url('^$', upload, name='upload'))