# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/testing/urls.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.conf.urls import include, url
from djblets.extensions.tests import test_view_method
urlpatterns = [
 url(b'^$', test_view_method, name=b'test-url-name'),
 url(b'^admin/extensions/', include(b'djblets.extensions.urls'))]