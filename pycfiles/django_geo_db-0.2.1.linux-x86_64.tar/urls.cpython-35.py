# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/urls.py
# Compiled at: 2018-03-10 21:43:50
# Size of source mod 2**32: 1618 bytes
from django_geo_db import views
from django.conf.urls import url
urlpatterns = [
 url('^geocoordinate/(?P<pk>\\d+)/$', views.GeoCoordinateDetails.as_view(), name='geocoordinate-detail'),
 url('^continent/(?P<pk>\\d+)/$', views.ContinentDetails.as_view(), name='continent-detail'),
 url('^country/(?P<pk>\\d+)/$', views.CountryDetails.as_view(), name='country-detail'),
 url('^state/(?P<pk>\\d+)/$', views.StateDetails.as_view(), name='state-detail'),
 url('^county/(?P<pk>\\d+)/$', views.CountyDetails.as_view(), name='county-detail'),
 url('^city/(?P<pk>\\d+)/$', views.CityDetails.as_view(), name='city-detail'),
 url('^zipcode/(?P<pk>\\d+)/$', views.ZipcodeDetails.as_view(), name='zipcode-detail'),
 url('^location/(?P<pk>[0-9]+)/$', views.LocationDetail.as_view(), name='location-detail'),
 url('^geocoordinate/', views.GeoCoordinateList.as_view(), name='geocoordinate-list'),
 url('^continent/', views.ContinentList.as_view(), name='continent-list'),
 url('^country/', views.CountryList.as_view(), name='country-list'),
 url('^county/', views.CountyList.as_view(), name='county-list'),
 url('^city/', views.CityList.as_view(), name='city-list'),
 url('^state/', views.StateList.as_view(), name='state-list'),
 url('^zipcode/', views.ZipcodeList.as_view(), name='zipcode-list'),
 url('^location/', views.LocationList.as_view(), name='location-list'),
 url('^location-map/$', views.LocationMap.as_view(), name='location-map'),
 url('^location-map-type/(?P<pk>[0-9]+)/$', views.LocationMapTypeDetail.as_view(), name='locationmaptype-detail')]