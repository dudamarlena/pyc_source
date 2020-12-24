# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/downloads/urls.py
# Compiled at: 2015-04-29 07:49:41
from django.conf.urls import patterns, url
from downloads.views import ObjectList, download_request
urlpatterns = patterns('', url('^$', ObjectList.as_view(), name='downloads'), url('^(?P<slug>[\\w-]+)/$', download_request, name='download-request'))