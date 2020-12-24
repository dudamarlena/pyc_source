# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/AutoPlanner/autoplanner/root_urls.py
# Compiled at: 2017-07-10 01:55:15
# Size of source mod 2**32: 2087 bytes
from django.views.i18n import javascript_catalog
from django.views.static import serve
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from djangofloor.views import robots
from djangofloor.scripts import load_celery
from autoplanner import views
__author__ = 'Matthieu Gallet'
load_celery()
admin.autodiscover()
urlpatterns = [
 url('^accounts/', include('allauth.urls')),
 url('^jsi18n/$', javascript_catalog, {'packages': ('djangofloor', 'django.contrib.admin')}),
 url('^' + settings.MEDIA_URL[1:] + '(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
 url('^' + settings.STATIC_URL[1:] + '(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
 url('^robots\\.txt$', robots),
 url('^org/(?P<organization_pk>\\d+)\\.html', (views.organization), name='organization'),
 url('^org/start/(?P<organization_pk>\\d+)\\.html', (views.schedule_task), name='schedule_start'),
 url('^org/cancel/(?P<organization_pk>\\d+)\\.html', (views.cancel_schedule_task), name='cancel_schedule'),
 url('^org/ical/(?P<organization_pk>\\d+)/all/(?P<title>.*)\\.ics', (views.generate_ics), name='ical'),
 url('^org/ical/(?P<organization_pk>\\d+)/agent/(?P<agent_pk>\\d+)/(?P<title>.*)\\.ics', (views.generate_ics),
   name='ical'),
 url('^org/ical/(?P<organization_pk>\\d+)/cat/(?P<category_pk>\\d+)/(?P<title>.*)\\.ics', (views.generate_ics),
   name='ical'),
 url('^tasks/multiply/(?P<task_pk>\\d+)\\.html', (views.multiply_task), name='multiply_task'),
 url('^tasks/apply_schedule_run/(?P<schedule_run_pk>\\d+)\\.html', (views.apply_schedule_run), name='apply_schedule_run'),
 url('^chaining/', include('smart_selects.urls')),
 url('^', include(admin.site.urls))]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url('^__debug__/', include(debug_toolbar.urls))]