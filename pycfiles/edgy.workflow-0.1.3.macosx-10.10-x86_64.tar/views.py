# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rd/Work/Edgy/workflow/.virtualenv-python/lib/python2.7/site-packages/edgy/workflow/ext/django_workflow/views.py
# Compiled at: 2016-02-21 07:40:44
from __future__ import absolute_import, print_function, unicode_literals
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseUpdateView

class TransitionView(SingleObjectTemplateResponseMixin, BaseUpdateView):

    def get_form_kwargs(self):
        form_kwargs = super(TransitionView, self).get_form_kwargs()
        form_kwargs[b'transition'] = self.transition
        return form_kwargs

    def dispatch(self, request, *args, **kwargs):
        self.transition = kwargs.pop(b'transition')
        return super(TransitionView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(TransitionView, self).get_context_data(**kwargs)
        context_data[b'transition'] = self.transition
        return context_data