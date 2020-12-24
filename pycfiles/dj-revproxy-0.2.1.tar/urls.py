# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benoitc/work/dj-pages/src/dj-revproxy/example/testproxy/../testproxy/urls.py
# Compiled at: 2010-11-09 10:19:01
from django.conf.urls.defaults import *
import revproxy
urlpatterns = patterns('', (
 '^proxy/', include(revproxy.site_proxy.urls)), (
 '^gunicorn(?P<path>.*)', 'revproxy.proxy_request',
 {'destination': 'http://gunicorn.org'}), (
 '(?P<path>.*)', 'revproxy.proxy_request',
 {'destination': 'http://friendpaste.com'}))