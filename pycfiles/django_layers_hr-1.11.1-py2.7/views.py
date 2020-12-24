# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/tests/views.py
# Compiled at: 2018-03-27 03:51:51
from django.views.generic.base import TemplateView
from layers.decorators import exclude_from_layers

class NormalView(TemplateView):
    template_name = 'tests/normal_view.html'


class WebOnlyView(TemplateView):
    template_name = 'tests/web_only_view.html'

    @exclude_from_layers(layers=('basic', ))
    def get(self, *args, **kwargs):
        return super(WebOnlyView, self).get(*args, **kwargs)