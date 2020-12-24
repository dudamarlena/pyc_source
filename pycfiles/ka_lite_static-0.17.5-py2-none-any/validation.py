# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/validation.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelForm
from django.forms.models import model_to_dict

class Validation(object):
    """
    A basic validation stub that does no validation.
    """

    def __init__(self, **kwargs):
        pass

    def is_valid(self, bundle, request=None):
        """
        Performs a check on the data within the bundle (and optionally the
        request) to ensure it is valid.

        Should return a dictionary of error messages. If the dictionary has
        zero items, the data is considered valid. If there are errors, keys
        in the dictionary should be field names and the values should be a list
        of errors, even if there is only one.
        """
        return {}


class FormValidation(Validation):
    """
    A validation class that uses a Django ``Form`` to validate the data.

    This class **DOES NOT** alter the data sent, only verifies it. If you
    want to alter the data, please use the ``CleanedDataFormValidation`` class
    instead.

    This class requires a ``form_class`` argument, which should be a Django
    ``Form`` (or ``ModelForm``, though ``save`` will never be called) class.
    This form will be used to validate the data in ``bundle.data``.
    """

    def __init__(self, **kwargs):
        if b'form_class' not in kwargs:
            raise ImproperlyConfigured(b"You must provide a 'form_class' to 'FormValidation' classes.")
        self.form_class = kwargs.pop(b'form_class')
        super(FormValidation, self).__init__(**kwargs)

    def form_args(self, bundle):
        data = bundle.data
        if data is None:
            data = {}
        kwargs = {b'data': {}}
        if hasattr(bundle.obj, b'pk'):
            if issubclass(self.form_class, ModelForm):
                kwargs[b'instance'] = bundle.obj
            kwargs[b'data'] = model_to_dict(bundle.obj)
        kwargs[b'data'].update(data)
        return kwargs

    def is_valid(self, bundle, request=None):
        """
        Performs a check on ``bundle.data``to ensure it is valid.

        If the form is valid, an empty list (all valid) will be returned. If
        not, a list of errors will be returned.
        """
        form = self.form_class(**self.form_args(bundle))
        if form.is_valid():
            return {}
        return form.errors


class CleanedDataFormValidation(FormValidation):
    """
    A validation class that uses a Django ``Form`` to validate the data.

    This class **ALTERS** data sent by the user!!!

    This class requires a ``form_class`` argument, which should be a Django
    ``Form`` (or ``ModelForm``, though ``save`` will never be called) class.
    This form will be used to validate the data in ``bundle.data``.
    """

    def is_valid(self, bundle, request=None):
        """
        Checks ``bundle.data``to ensure it is valid & replaces it with the
        cleaned results.

        If the form is valid, an empty list (all valid) will be returned. If
        not, a list of errors will be returned.
        """
        form = self.form_class(**self.form_args(bundle))
        if form.is_valid():
            bundle.data = form.cleaned_data
            return {}
        return form.errors