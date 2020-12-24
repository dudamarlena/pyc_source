# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/skylar/pinax/projects/NASA/apps/events/urls.py
# Compiled at: 2009-08-18 18:19:39
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
urlpatterns = patterns('', url('^$', view='events.views.all', name='events_all'), url('^archive/$', view='events.views.archive', name='events_archive'), url('^(?P<id>\\d+)/(?P<slug>[-\\w]+)/$', view='events.views.detail', name='events_detail'), url('^delete/(?P<id>\\d+)/', view='events.views.delete', name='events_delete'), url('add/relation/(?P<event_id>\\d+)/(?P<user_id>\\d+)/$', view='events.views.add_relation', name='events_add_relation'), url('add/(?P<app_label>[-\\w]+)/(?P<model_name>[-\\w]+)/(?P<id>\\d+)/$', view='events.views.add', name='events_add'), url('change/(?P<id>\\d+)/', view='events.views.change', name='events_change'), url('for_day/(?P<year>\\d{4})/(?P<month>\\d{2})/(?P<day>\\d{2})/$', view='events.views.for_day', name='events_for_day'), url('for/(?P<username>[-\\w]+)/$', view='events.views.for_user', name='events_for_user'), url('you_watch/$', view='events.views.you_watch', name='events_you_watch'), url('for/(?P<app_label>[-\\w]+)/(?P<model_name>[-\\w]+)/(?P<id>\\d+)/$', view='events.views.for_instance', name='events_for_instance'))