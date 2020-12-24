# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/aghoo/Aghoo/province/api/urls.py
# Compiled at: 2018-01-09 01:46:23
from django.conf.urls import include, url
from province.api.views import ProvinceListAPIView, ProvinceCreateAPIView, ProvinceDetailAPIView, CityAutocomplete
urlpatterns = [
 url('^$', ProvinceListAPIView.as_view(), name='list'),
 url('^create/$', ProvinceCreateAPIView.as_view(), name='create'),
 url('^city/autocomplete/$', CityAutocomplete.as_view(), name='city-autocomplete'),
 url('^(?P<id>\\d+)/$', ProvinceDetailAPIView.as_view(), name='detail'),
 url('^(?P<province_id>\\d+)/city/', include('province.api.urls-city', namespace='city-api')),
 url('^(?P<province_id>\\d+)/shahrak/', include('province.api.urls-shahrak', namespace='shahrak-api'))]