# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/6z/y737zg156f53v6d096dlmv500000gn/T/pip-build-YeCYrE/user-behavior/user_behavior/urls.py
# Compiled at: 2016-11-17 22:38:22
from django.conf.urls import url, include
from rest_framework import routers
from .views import ApiInfoViewSet, UserBehaviorViewSet
router = routers.DefaultRouter(trailing_slash=False)
router.register('api_info', ApiInfoViewSet)
router.register('user_behavior', UserBehaviorViewSet)
url_patterns = [
 url('', include(router.urls))]