# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_calendar/views.py
# Compiled at: 2016-03-15 02:37:19
from django.utils.translation import ugettext as _
from jmbo import USE_GIS
from jmbo.views import ObjectList
from jmbo_calendar.models import Event

class ObjectList(ObjectList):

    def get_context_data(self, **kwargs):
        context = super(ObjectList, self).get_context_data(**kwargs)
        show_distance = False
        if USE_GIS:
            from django.contrib.gis.geos import Point
            show_distance = isinstance(self.request.session['location']['position'], Point)
        context['title'] = _('Events')
        context['show_distance'] = show_distance
        return context

    def get_queryset(self):
        qs = Event.coordinator.upcoming()
        qs = qs.filter(location__country=self.request.session['location']['city'].country_id)
        position = self.request.session['location']['position']
        if not isinstance(position, Point):
            position = self.request.session['location']['city'].coordinates
        qs = qs.distance(position).order_by('distance', 'start')
        return qs

    def get_paginate_by(self, *args, **kwargs):
        return 10