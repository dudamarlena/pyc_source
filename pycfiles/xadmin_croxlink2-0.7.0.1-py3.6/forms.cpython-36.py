# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/xadmin/forms.py
# Compiled at: 2018-01-28 08:42:20
# Size of source mod 2**32: 2564 bytes
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy, ugettext as _
from django.contrib.auth import get_user_model
ERROR_MESSAGE = ugettext_lazy('Please enter the correct username and password for a staff account. Note that both fields are case-sensitive.')

class AdminAuthenticationForm(AuthenticationForm):
    __doc__ = '\n    A custom authentication form used in the admin app.\n\n    '
    this_is_the_login_form = forms.BooleanField(widget=(forms.HiddenInput),
      initial=1,
      error_messages={'required': ugettext_lazy('Please log in again, because your session has expired.')})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE
        if username:
            if password:
                self.user_cache = authenticate(username=username,
                  password=password)
                if self.user_cache is None:
                    User = get_user_model()
                    try:
                        user = User.objects.get(username=username)
                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        pass
                    else:
                        if user.check_password(password):
                            message = _("This account '%s' is not authorized to login!") % user.username
                            raise forms.ValidationError(message)
                        if '@' in username:
                            try:
                                user = User.objects.get(email=username, is_staff=True,
                                  is_active=True)
                            except (User.DoesNotExist, User.MultipleObjectsReturned):
                                pass
                            else:
                                if user.check_password(password):
                                    message = _("Your e-mail address is not your username. Try '%s' instead.") % user.username
                                    raise forms.ValidationError(message)
                        raise forms.ValidationError(message)
        return self.cleaned_data