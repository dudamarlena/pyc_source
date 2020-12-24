# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/urls.py
# Compiled at: 2019-04-19 21:07:17
# Size of source mod 2**32: 797 bytes
from django.conf.urls import include, url
from rest_framework import routers
from . import views
app_name = 'locations'
api = routers.SimpleRouter()
api.register('locations', (views.LocationsViewSet), base_name='locations')
api.register('locations-light', (views.LocationsLightViewSet), base_name='locations-light')
api.register('locations-types', (views.LocationTypesViewSet), base_name='locationtypes')
urlpatterns = [
 url('', include(api.urls)),
 url('^locations/pcode/(?P<p_code>\\w+)/$',
   (views.LocationsViewSet.as_view({'get': 'retrieve'})), name='locations_detail_pcode'),
 url('^cartodbtables/$', (views.CartoDBTablesView.as_view()), name='cartodbtables'),
 url('^autocomplete/$', (views.LocationQuerySetView.as_view()), name='locations_autocomplete')]