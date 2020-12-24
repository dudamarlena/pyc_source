# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/django-smart-proxy/lib/python3.3/site-packages/smart_proxy/urls.py
# Compiled at: 2014-11-26 21:04:56
# Size of source mod 2**32: 246 bytes
from django.conf.urls import include, patterns, url
from .views import SmartProxyView
urlpatterns = patterns('', url('^(?P<proxy_id>[^/]+)/', SmartProxyView.as_view(), name='django-smart-proxy'))