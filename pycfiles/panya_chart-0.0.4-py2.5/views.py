# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/chart/views.py
# Compiled at: 2010-08-04 03:51:07
from panya.generic.views import GenericObjectDetail, GenericObjectList
from panya.view_modifiers import IntegerFieldRangeViewModifier
from chart.models import Chart
from panya.view_modifiers import IntegerFieldRangeViewModifier

class ObjectList(GenericObjectList):

    def get_extra_context(self, *args, **kwargs):
        extra_context = super(ObjectList, self).get_extra_context(*args, **kwargs)
        added_context = {'title': 'Charts'}
        if extra_context:
            extra_context.update(added_context)
        else:
            extra_context = added_context
        return extra_context

    def get_paginate_by(self):
        return 12

    def get_queryset(self):
        return Chart.permitted.all()


object_list = ObjectList()

class ObjectDetail(GenericObjectList):

    def get_queryset(self, *args, **kwargs):
        slug = kwargs['slug']
        return Chart.permitted.get(slug=slug).chartentries.all().order_by('current_position')

    def get_view_modifier(self, request, *args, **kwargs):
        return IntegerFieldRangeViewModifier(request=request, field_name='current_position', count=self.get_queryset(*args, **kwargs).count(), interval=10)


object_detail = ObjectDetail()