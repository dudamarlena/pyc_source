# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/djangoflash/tests/testproj/urls.py
# Compiled at: 2011-01-28 16:01:34
from django.conf.urls.defaults import *
from django.conf import settings
urlpatterns = patterns('', (
 '', include('testproj.app.urls')), (
 '^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}))