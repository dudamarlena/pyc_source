# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\django\django-nimble\nimble\views\control_panel.py
# Compiled at: 2016-11-19 14:34:52
# Size of source mod 2**32: 1504 bytes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views import View
from nimble.forms.profile import ProfileForm
from nimble.forms.user import UserForm

class ControlPanelView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'nimble/control_panel.html'

    def get(self, request, *args, **kwargs):
        user_form = UserForm(initial={'first_name': self.request.user.first_name, 
         'last_name': self.request.user.last_name, 
         'email': self.request.user.email})
        profile_form = ProfileForm(initial={'theme': self.request.user.profile.theme})
        return render(request, self.template_name, {'user_form': user_form, 
         'profile_form': profile_form, 
         'view': self})

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            for key, value in user_form.cleaned_data.items():
                setattr(self.request.user, key, value)

            for key, value in profile_form.cleaned_data.items():
                setattr(self.request.user.profile, key, value)

            self.request.user.save()
            self.request.user.profile.save()
        return self.get(request, *args, **kwargs)