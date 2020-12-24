# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dnavarro/repos/django-leads/leads/views.py
# Compiled at: 2014-02-26 09:41:22
# Size of source mod 2**32: 623 bytes
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, TemplateView
from .utils import get_register_model, get_register_form_class

class IndexView(CreateView):
    __doc__ = '\n    This view renders the main page\n    '
    template_name = 'leads/index.html'
    model = get_register_model()
    form_class = get_register_form_class()

    def get_success_url(self):
        return reverse('leads:thanks_register')


class ThanksView(TemplateView):
    __doc__ = '\n    Page that loads when someone registers successfully\n    '
    template_name = 'leads/thanks_register.html'