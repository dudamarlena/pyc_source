# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_mailchimp_forms/forms.py
# Compiled at: 2010-11-29 14:27:26
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django_mailchimp_forms.utils import register_user

def chimpy_form_instance_wrapper(form, data=None):
    if 'email' not in form.fields:
        form.fields['email'] = forms.EmailField()
    if 'newsletter' not in form.fields:
        form.fields['newsletter'] = forms.BooleanField(initial=True, required=False, help_text=_("Get informed about transifex service notifications, like outages and new features. You can unsubscribe at any time from your account's profile."))
    data = data or {}
    if 'email' in data and 'email' not in form.data:
        form.data['email'] = data['email']
    if 'newsletter' in data and 'newsletter' not in form.data:
        form.data['newsletter'] = data['newsletter']
    old_clean_email = getattr(form, 'clean_email', lambda : form.cleaned_data['email'])

    def get_clean_email_method(form):

        def new_clean_email():
            email_value = old_clean_email()
            if 'newsletter' in form.data and not email_value:
                raise ValidationError('This field is required for newsletter subscription.')
            return email_value

        return new_clean_email

    form.clean_email = get_clean_email_method(form)

    def get_save_method(form):
        try:
            old_save_method = getattr(form, 'save')

            def new_save_method(*args, **kwargs):
                user = old_save_method(*args, **kwargs)
                if not user.email:
                    user.email = form.cleaned_data['email']
                    user.save()
                if form.cleaned_data['newsletter']:
                    register_user(user)
                return user

            return new_save_method
        except AttributeError as e:

            def not_implemented(*args, **kwargs):
                raise NotImplementedError("'save' method not implemented")

            return not_implemented

    form.save = get_save_method(form)
    return form


def chimpy_form_class_wrapper(form_class):

    class chimpy_form_class(form_class):

        def __init__(self, *args, **kwargs):
            super(chimpy_form_class, self).__init__(*args, **kwargs)
            if 'data' in kwargs:
                data = kwargs['data']
            else:
                try:
                    data = args[0]
                except IndexError as e:
                    data = None

            self = chimpy_form_instance_wrapper(self, data)
            return

    return chimpy_form_class


ChimpyForm = chimpy_form_class_wrapper(UserCreationForm)