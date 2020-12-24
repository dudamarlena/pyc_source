# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/views.py
# Compiled at: 2017-10-23 07:42:35
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from composer.models import Slot

class SlotView(DetailView):
    """The slot detail view is only applicable to slots with slot_name
    "content".
    """
    model = Slot

    def dispatch(self, request, *args, **kwargs):
        handler = super(SlotView, self).dispatch(request, *args, **kwargs)
        if handler.status_code != 405:
            return self.get(request, *args, **kwargs)
        else:
            return handler

    def get_object(self):
        url = self.request.path_info
        return get_object_or_404(Slot.permitted, url=self.request.path_info, slot_name='content')