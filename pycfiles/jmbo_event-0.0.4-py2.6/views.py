# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/event/views.py
# Compiled at: 2012-05-07 06:37:42
from django.core.urlresolvers import reverse
from cal.models import EntryItem
from event.models import Event
from jmbo.generic.views import GenericObjectList, GenericObjectDetail
from jmbo.models import ModelBase
from jmbo.view_modifiers import DateFieldIntervalViewModifier

class ObjectList(GenericObjectList):

    def get_extra_context(self, *args, **kwargs):
        return {'title': 'Events'}

    def get_view_modifier(self, request, *args, **kwargs):
        return DateFieldIntervalViewModifier(request=request, field_name='start')

    def get_paginate_by(self, *args, **kwargs):
        return 7

    def get_queryset(self, *args, **kwargs):
        return EntryItem.permitted.by_model(Event).order_by('start')

    def get_template_name(self, *args, **kwargs):
        return 'event/event_entryitem_list.html'


object_list = ObjectList()

class ObjectDetail(GenericObjectDetail):

    def get_extra_context(self, *args, **kwargs):
        return {'title': 'Events'}

    def get_view_modifier(self, request, *args, **kwargs):
        return DateFieldIntervalViewModifier(request=request, field_name='start', base_url=reverse('event_entryitem_list'), ignore_defaults=True)

    def get_queryset(self, *args, **kwargs):
        return Event.permitted.all()


object_detail = ObjectDetail()