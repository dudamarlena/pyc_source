# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\users\ma_k\appdata\local\temp\pip-build-s8wja0\httplog\httplog\urls.py
# Compiled at: 2016-11-28 21:21:16
from django.conf.urls import url, include
from rest_framework import routers
from .views import HttpLogViewSet
router = routers.DefaultRouter(trailing_slash=False)
router.register('httplog', HttpLogViewSet)
url_patterns = [
 url('api/v2/', include(router.urls))]