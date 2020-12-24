# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/AutoPlanner/autoplanner/urls.py
# Compiled at: 2017-09-12 01:55:51
# Size of source mod 2**32: 1044 bytes
from django.conf.urls import url
from autoplanner import views
__author__ = 'Matthieu Gallet'
app_name = 'autoplanner'
urlpatterns = [
 url('^organization/(?P<organization_pk>\\d+)/$', (views.organization_index), name='organization_index'),
 url('^org/(?P<organization_pk>\\d+)\\.html', (views.organization), name='organization'),
 url('^org/start/(?P<organization_pk>\\d+)\\.html', (views.schedule_task), name='schedule_start'),
 url('^org/cancel/(?P<organization_pk>\\d+)\\.html', (views.cancel_schedule_task), name='cancel_schedule'),
 url('^org/ical/(?P<organization_pk>\\d+)/all/(?P<title>.*)\\.ics', (views.generate_ics), name='ical'),
 url('^org/ical/(?P<organization_pk>\\d+)/agent/(?P<agent_pk>\\d+)/(?P<title>.*)\\.ics', (views.generate_ics),
   name='ical'),
 url('^org/ical/(?P<organization_pk>\\d+)/cat/(?P<category_pk>\\d+)/(?P<title>.*)\\.ics', (views.generate_ics),
   name='ical'),
 url('^tasks/apply_schedule_run/(?P<schedule_run_pk>\\d+)\\.html', (views.apply_schedule_run), name='apply_schedule_run')]