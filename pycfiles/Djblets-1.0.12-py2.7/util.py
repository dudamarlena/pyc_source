# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/auth/util.py
# Compiled at: 2019-06-12 01:17:17
"""Basic utility functions for authentication.

This contains some validation functions that may be useful for forms.
"""
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext as _
try:
    from django.forms import utils as form_utils
except ImportError:
    from django.forms import util as form_utils

def validate_test_cookie(form, request):
    """Validate that the test cookie was properly set in a prior request.

    If the test cookie was not set, the given form's ``submit`` field will
    be set with an error saying that cookies must be enabled.

    Args:
        form (Form):
            The form using the validator.

        request (HttpRequest):
            The HTTP request containing the test cookie.
    """
    if not request.session.test_cookie_worked():
        form.errors[b'submit'] = forms.util.ErrorList([
         _(b'Cookies must be enabled.')])


def validate_old_password(form, user, field_name=b'password'):
    """Validate that the password given on a form was valid.

    This is intended for Password Change forms, and will check that the
    specified password in the form matches the user's current password.

    Args:
        form (Form):
            The form using the validator and containing the field.

        user (User):
            The user whose password is being changed.

        field_name (unicode):
            The name of the password field.
    """
    if not form.errors.get(field_name) and not user.check_password(form.data.get(field_name)):
        form.errors[field_name] = form_utils.ErrorList([
         _(b'Incorrect password.')])