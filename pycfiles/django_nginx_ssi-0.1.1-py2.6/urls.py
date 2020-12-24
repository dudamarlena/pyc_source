# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ssi/urls.py
# Compiled at: 2011-01-25 14:23:28
from django.conf.urls.defaults import *
from ssi.views import render_from_cache
urlpatterns = patterns('', (
 '^(.*)/$', render_from_cache, {}, 'nginxssi'))