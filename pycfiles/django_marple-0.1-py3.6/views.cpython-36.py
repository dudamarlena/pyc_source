# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/marple/views.py
# Compiled at: 2018-07-01 03:00:43
# Size of source mod 2**32: 602 bytes
from django.views.generic import TemplateView
from django.conf import settings
from .models import MarpleItem
from .marple import Marple

class Index(TemplateView):
    template_name = 'marple/index.html'
    http_method_names = ['get']

    def get_context_data(self, *args, **kwargs):
        context = (super(Index, self).get_context_data)(*args, **kwargs)
        debug = getattr(settings, 'DEBUG', False)
        if debug:
            marple = Marple()
            marple.digest(force_update=True)
        items = MarpleItem.objects.all()
        context['items'] = items
        return context