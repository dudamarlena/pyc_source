# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/autocomplete_urls.py
# Compiled at: 2018-02-11 11:30:28
# Size of source mod 2**32: 987 bytes
from django_geo_db import autocomplete_views as views
from django.conf.urls import url
urlpatterns = [
 url('^autocomplete/named-location/$', views.NamedLocationAutocomplete.as_view(), name='named-location-autocomplete'),
 url('^autocomplete/location/$', views.LocationAutocomplete.as_view(), name='location-autocomplete'),
 url('^autocomplete/public-locations/$', views.PublicLocationsAutocomplete.as_view(), name='public-locations-autocomplete'),
 url('^autocomplete/zipcode/$', views.ZipcodeAutocomplete.as_view(), name='zipcode-autocomplete'),
 url('^autocomplete/county/$', views.CountyAutocomplete.as_view(), name='county-autocomplete'),
 url('^autocomplete/city/$', views.CityAutocomplete.as_view(), name='city-autocomplete'),
 url('^autocomplete/geocoordinate/$', views.GeoCoordinateAutocomplete.as_view(), name='geocoordinate-autocomplete')]