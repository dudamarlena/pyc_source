# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/urls.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 288 bytes
from django.conf.urls import url, include
from rest_framework import routers
from ovp_organizations import views
router = routers.DefaultRouter()
router.register('organizations', views.OrganizationResourceViewSet, 'organization')
urlpatterns = [
 url('^', include(router.urls))]