# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rbmozui/admin_urls.py
# Compiled at: 2015-01-29 15:00:20
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from rbmozui.extension import RBMozUI
urlpatterns = patterns(b'rbmozui.views', url(b'^$', b'configure'))