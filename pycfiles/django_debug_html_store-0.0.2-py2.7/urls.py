# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/django_debug_html_store/urls.py
# Compiled at: 2013-02-22 23:53:59
"""
django_debug_html_store urls module
"""
from django.conf.urls.defaults import *
urlpatterns = patterns('django_debug_html_store.views', url('^read_response/$', 'read_response'), url('^read_response/(?P<ip_addr>.+)/$', 'read_response'), url('^test/http_response/$', 'test_http_response'), url('^test/redirect_response/$', 'test_redirect_response'))