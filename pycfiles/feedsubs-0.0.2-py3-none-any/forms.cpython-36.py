# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/um/forms.py
# Compiled at: 2018-09-11 17:03:28
# Size of source mod 2**32: 1131 bytes
from django import forms
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from allauth.account.forms import SignupForm

class DeleteUserForm(forms.Form):
    username = forms.CharField(help_text='Confirm account deletion by entering your username')

    def __init__(self, current_username, *args, **kwargs):
        self._current_username = current_username
        (super().__init__)(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self._current_username != cleaned_data['username']:
            raise forms.ValidationError('Enter your current username')


class SignupFormWithToS(SignupForm):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        tos_page = reverse_lazy('django.contrib.flatpages.views.flatpage', kwargs={'url': '/terms-of-service'})
        label = mark_safe('I have read and I agree with the <a href="{}">Terms of Service</a>'.format(tos_page))
        self.fields['tos'] = forms.BooleanField(required=True, label=label)