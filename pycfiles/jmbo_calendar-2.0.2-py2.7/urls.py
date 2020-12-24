# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_calendar/urls.py
# Compiled at: 2016-03-10 02:18:44
from django.conf.urls import patterns, url
from jmbo import USE_GIS
from jmbo.views import ObjectDetail
from jmbo_calendar.views import ObjectList
if USE_GIS:
    from atlas.views import location_required
urlpatterns = patterns('', url('^events/$', USE_GIS and location_required(ObjectList.as_view()) or ObjectList.as_view(), name='events'), url('^event/(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='event_object_detail'))