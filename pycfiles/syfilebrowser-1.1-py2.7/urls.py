# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syfilebrowser/urls.py
# Compiled at: 2016-04-18 13:43:03
from __future__ import unicode_literals
from django.conf.urls import *
urlpatterns = patterns(b'', url(b'^browse/$', b'syfilebrowser.views.browse', name=b'fb_browse'), url(b'^mkdir/', b'syfilebrowser.views.mkdir', name=b'fb_mkdir'), url(b'^upload/', b'syfilebrowser.views.upload', name=b'fb_upload'), url(b'^rename/$', b'syfilebrowser.views.rename', name=b'fb_rename'), url(b'^delete/$', b'syfilebrowser.views.delete', name=b'fb_delete'), url(b'^check_file/$', b'syfilebrowser.views._check_file', name=b'fb_check'), url(b'^upload_file/$', b'syfilebrowser.views._upload_file', name=b'fb_do_upload'))