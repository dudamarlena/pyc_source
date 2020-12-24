# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/countries/urls.py
# Compiled at: 2016-12-06 13:52:51
# Size of source mod 2**32: 931 bytes
from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views
from . import apis
app_name = 'countries'
API_PREFIX = '^countries/api/v(?P<version>[^/]+)'
urlpatterns = [
 url('countries/$', views.index, name='index')]
urlpatterns += [
 url(API_PREFIX + '/flag/code/$', apis.flag_code, name='api_flag_code'),
 url(API_PREFIX + '/get-country$', apis.get_country, name='api_get_country'),
 url(API_PREFIX + '/get-regions$', apis.get_regions, name='api_get_regions'),
 url(API_PREFIX + '/get-provinces$', apis.get_provinces, name='api_get_provinces'),
 url(API_PREFIX + '/get-communes$', apis.get_communes, name='api_get_communes')]
urlpatterns += [
 url(API_PREFIX + '/get-user-addresses$', apis.get_user_addresses, name='api_get_user_addresses'),
 url(API_PREFIX + '/create-user-address$', apis.create_user_address, name='api_create_user_address')]