# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/api_tasty/validation.py
# Compiled at: 2020-02-26 14:47:57
# Size of source mod 2**32: 1468 bytes
from django.contrib.auth.models import User
from tastypie.validation import CleanedDataFormValidation

class TendenciValidation(CleanedDataFormValidation):
    __doc__ = 'Validation that makes use of a given Form.\n    The Form is assumed to be a ModelForm of a TendenciBaseModel subclass\n    '

    def is_valid(self, bundle, request=None):
        """Validate the bundle with the given form.
        Creator and Owner fields and defaulted to be the user of
        the apikey if they were not specified.
        """
        data = bundle.data
        if data is None:
            data = {}
        if request:
            user = User.objects.get(username=(request.GET.get('username')))
            if not data.get('creator', None):
                data['creator'] = user.pk
                data['creator_username'] = user.username
            if not data.get('owner', None):
                data['owner'] = user.pk
                data['owner_username'] = user.username
        form = self.form_class(data, instance=(bundle.obj), request=request)
        if form.is_valid():
            bundle.data = form.cleaned_data
            return {}
        return form.errors