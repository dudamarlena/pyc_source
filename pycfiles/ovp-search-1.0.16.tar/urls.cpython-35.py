# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-search/ovp_search/urls.py
# Compiled at: 2017-05-08 18:10:05
# Size of source mod 2**32: 902 bytes
from django.conf.urls import url, include
from rest_framework import routers
from ovp_search import views
project_search = routers.SimpleRouter()
project_search.register('projects', views.ProjectSearchResource, 'search-projects')
organization_search = routers.SimpleRouter()
organization_search.register('organizations', views.OrganizationSearchResource, 'search-organizations')
user_search = routers.SimpleRouter()
user_search.register('users', views.UserSearchResource, 'search-users')
urlpatterns = [
 url('^search/', include(project_search.urls)),
 url('^search/', include(organization_search.urls)),
 url('^search/', include(user_search.urls)),
 url('^search/country-cities/(?P<country>[^/]+)/', views.query_country_deprecated, name='search-query-country'),
 url('^search/available-cities/(?P<country>[^/]+)/', views.available_country_cities, name='available-country-cities')]