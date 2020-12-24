# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/examples/_django/urls.py
# Compiled at: 2013-12-04 14:19:17
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url

from pyws.adapters._django import serve
from server import server
from _django.test_form import test_form
urlpatterns = patterns('', url('^$', test_form), url('^api/(.*)', serve, {'server': server}))