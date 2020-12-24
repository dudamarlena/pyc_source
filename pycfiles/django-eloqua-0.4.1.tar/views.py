# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svdgraaf/Projects/nl.focusmedia/lib/python2.7/site-packages/eloqua/views.py
# Compiled at: 2013-03-01 08:54:27
from django.views.generic.base import TemplateView
from .clients import EloquaLandingPagesClient

class LandingPageView(TemplateView):
    template_name = 'eloqua/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)
        e = EloquaLandingPagesClient()
        landing_page = e.get(kwargs['pk'])
        context['landing_page'] = landing_page
        return context