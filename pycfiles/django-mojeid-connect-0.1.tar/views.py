# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: django_mojeid_connect/views.py
# Compiled at: 2018-07-09 09:50:29
"""Views for django_mojeid_connect."""
from __future__ import unicode_literals
from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy
from django.views.generic import CreateView

class CreateUser(CreateView):
    """View for creating and pairing user to mojeID."""
    model = get_user_model()
    fields = [b'username']
    template_name = b'create_user.html'
    success_url = reverse_lazy(b'oidc_authentication_init')

    def form_valid(self, form):
        """Log user in and initiate pairing."""
        response = super(CreateUser, self).form_valid(form)
        login(self.request, self.object)
        return response