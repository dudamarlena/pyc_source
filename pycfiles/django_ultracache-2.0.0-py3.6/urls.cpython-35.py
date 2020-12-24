# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/tests/urls.py
# Compiled at: 2019-05-29 04:46:58
# Size of source mod 2**32: 1032 bytes
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from ultracache.tests import views, viewsets
router = DefaultRouter()
router.register('dummies', viewsets.DummyViewSet)
urlpatterns = [
 url('^api/', include(router.urls)),
 url('^render-view/$', views.RenderView.as_view(), name='render-view'),
 url('^method-cached-view/$', views.MethodCachedView.as_view(), name='method-cached-view'),
 url('^class-cached-view/$', views.ClassCachedView.as_view(), name='class-cached-view'),
 url('^cached-header-view/$', views.CachedHeaderView.as_view(), name='cached-header-view'),
 url('^bustable-cached-view/$', views.BustableCachedView.as_view(), name='bustable-cached-view'),
 url('^non-bustable-cached-view/$', views.NonBustableCachedView.as_view(), name='non-bustable-cached-view')]