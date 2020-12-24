# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/admin/authenticator.py
# Compiled at: 2020-03-13 06:18:10
# Size of source mod 2**32: 3758 bytes
"""Admin for django_fido authenticator."""
from __future__ import unicode_literals
from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django_fido.forms import Fido2RegistrationForm
from django_fido.models import Authenticator
from django_fido.views import Fido2RegistrationRequestView, Fido2RegistrationView

class Fido2RegistrationAdminForm(Fido2RegistrationForm):
    __doc__ = 'Registration form with user selection.'
    user = forms.ModelChoiceField(queryset=(get_user_model().objects.all()))
    field_order = ('user', 'label')


class Fido2RegistrationRequestAdminView(PermissionRequiredMixin, Fido2RegistrationRequestView):
    __doc__ = 'Registration request view with user selection.'
    permission_required = 'django_fido.add_authenticator'

    def get_user(self):
        """Get user based on POST request."""
        user_id = get_user_model()._meta.pk.to_python(self.request.GET.get('user'))
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            raise Http404('User does not exist')


class AuthenticatorAddView(PermissionRequiredMixin, Fido2RegistrationView):
    __doc__ = 'Authenticator add view.'
    permission_required = 'django_fido.add_authenticator'
    form_class = Fido2RegistrationAdminForm
    template_name = 'django_fido/add_authenticator.html'
    fido2_request_url = reverse_lazy('admin:django_fido_registration_request')
    extra_context = None

    def form_valid(self, form: forms.Form) -> HttpResponse:
        """Complete the FIDO token registration."""
        try:
            self.complete_registration(form)
        except ValidationError as error:
            try:
                form.add_error(None, error)
                return self.form_invalid(form)
            finally:
                error = None
                del error

        authenticator = Authenticator.objects.create(user=(form.cleaned_data['user']),
          attestation=(form.cleaned_data['attestation']),
          label=(form.cleaned_data.get('label')))
        return HttpResponseRedirect(reverse('admin:django_fido_authenticator_change', args=(authenticator.pk,)))

    def get_context_data(self, **kwargs):
        context = (super().get_context_data)(**kwargs)
        if self.extra_context:
            context.update(self.extra_context)
        return context


class AuthenticatorAdmin(admin.ModelAdmin):
    __doc__ = 'Authenticator admin.'
    list_display = ('label', 'user', 'create_datetime')
    readonly_fields = ('user', 'credential_id_data', 'attestation_data', 'counter')
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
         url('^registration/request/$',
           (self.admin_site.admin_view(Fido2RegistrationRequestAdminView.as_view())),
           name='django_fido_registration_request')]
        return my_urls + urls

    def add_view(self, request, form_url='', extra_context=None):
        """Customize authenticator add view."""
        context = {**(self.admin_site.each_context(request)), **{'opts':self.model._meta, 
         'add':True, 
         'has_view_permission':True}}
        context.update(extra_context or {})
        return AuthenticatorAddView.as_view(extra_context=context)(request)