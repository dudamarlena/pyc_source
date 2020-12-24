# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/guidjango/urls.py
# Compiled at: 2007-11-06 15:28:25
from django.conf.urls.defaults import *
urlpatterns = patterns('', ('^test/$', 'views.display'), ('^test/asc/(\\d+)/$', 'views.sortAsc'), ('^test/desc/(\\d+)/$',
                                                                                                   'views.sortDesc'))