# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atlas/urls.py
# Compiled at: 2015-04-27 14:27:53
from django.conf.urls import patterns, url, include
from tastypie.api import Api
from atlas.api import CountryResource, RegionResource, CityResource
from atlas import views
v1_api = Api(api_name='v1')
v1_api.register(CountryResource())
v1_api.register(RegionResource())
v1_api.register(CityResource())
urlpatterns = patterns('', (
 '^atlas-api/',
 include(v1_api.urls)), url('^set-location/$', views.set_location, name='set-location'), url('^select-location/$', views.select_location, name='select-location'))