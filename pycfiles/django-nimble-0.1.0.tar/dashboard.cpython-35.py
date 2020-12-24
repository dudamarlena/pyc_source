# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\django\django-nimble\nimble\views\dashboard.py
# Compiled at: 2016-11-19 14:34:52
# Size of source mod 2**32: 460 bytes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'nimble/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = 'Dashboard Test'
        return context