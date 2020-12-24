# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_gizmos/tethys_gizmos/urls.py
# Compiled at: 2015-02-05 10:57:22
from django.conf.urls import patterns, url, include
ajax_urls = [
 url('^get-kml/$', 'tethys_gizmos.views.gizmo_showcase.get_kml', name='get_kml'),
 url('^swap-kml/$', 'tethys_gizmos.views.gizmo_showcase.swap_kml', name='swap_kml'),
 url('^swap-overlays/$', 'tethys_gizmos.views.gizmo_showcase.swap_overlays', name='swap_overlays'),
 url('^fetchclimate/single-request/$', 'tethys_gizmos.views.gizmos.fetchclimate.data_request_single', name='single_request')]
urlpatterns = patterns('', url('^$', 'tethys_gizmos.views.gizmo_showcase.index', name='showcase'), url('^editable-map/$', 'tethys_gizmos.views.gizmo_showcase.editable_map', name='editable_map'), url('^google-map/$', 'tethys_gizmos.views.gizmo_showcase.google_map', name='google_map'), url('^map-view', 'tethys_gizmos.views.gizmo_showcase.map_view', name='map_view'), url('^fetch-climate-map/$', 'tethys_gizmos.views.gizmo_showcase.fetchclimate_map', name='fetchclimate_map'), url('^ajax/', include(ajax_urls)))