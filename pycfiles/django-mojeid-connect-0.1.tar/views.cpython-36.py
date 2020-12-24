# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/Git/django-mojeid-connect/django_mojeid_connect/views.py
# Compiled at: 2018-07-09 09:50:29
# Size of source mod 2**32: 663 bytes
"""Views for django_mojeid_connect."""
from __future__ import unicode_literals
from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy
from django.views.generic import CreateView

class CreateUser(CreateView):
    __doc__ = 'View for creating and pairing user to mojeID.'
    model = get_user_model()
    fields = ['username']
    template_name = 'create_user.html'
    success_url = reverse_lazy('oidc_authentication_init')

    def form_valid(self, form):
        response = super(CreateUser, self).form_valid(form)
        login(self.request, self.object)
        return response