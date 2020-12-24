# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/urls/main.py
# Compiled at: 2019-10-28 01:57:23
# Size of source mod 2**32: 632 bytes
from rest_framework import routers
from irekua_rest_api import views
main_router = routers.DefaultRouter()
main_router.register('annotations', views.AnnotationViewSet)
main_router.register('collections', views.CollectionViewSet)
main_router.register('devices', views.DeviceViewSet)
main_router.register('items', views.ItemViewSet)
main_router.register('sampling_events', views.SamplingEventViewSet)
main_router.register('sites', views.SiteViewSet)
main_router.register('terms', views.TermTypeViewSet)
main_router.register('users', views.UserViewSet)