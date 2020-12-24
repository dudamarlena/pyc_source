# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/urls.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 531 bytes
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter, NestedDefaultRouter
from ovp_projects import views
router = routers.DefaultRouter()
router.register('projects', views.ProjectResourceViewSet, 'project')
applies = NestedDefaultRouter(router, 'projects', lookup='project')
applies.register('applies', views.ApplyResourceViewSet, 'project-applies')
urlpatterns = [
 url('^', include(router.urls)),
 url('^', include(applies.urls))]