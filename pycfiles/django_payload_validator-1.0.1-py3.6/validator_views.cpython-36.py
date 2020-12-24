# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/django_payload_validator/validator_views.py
# Compiled at: 2018-02-07 04:25:59
# Size of source mod 2**32: 1271 bytes
from django.views.generic import View

class BaseValidatorView(View):
    __doc__ = '\n    Override necessary methods to implement payload validation.\n    '
    required_class_attrs = ['payload_validator']

    def __init__(self, **kwargs):
        """
        Overriding django's base view to make sure that all necessary parameters are either set or provided.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

        self._check_attrs()

    def _check_attrs(self):
        for class_attr in self.required_class_attrs:
            if not self.hasattr(class_attr):
                raise '{class_attr} is a required property for {class_name}'.format(class_attr=class_attr,
                  class_name=(self.__class__.__name__))

    def post(self, request, *args, **kwargs):
        """
        Override post method to make calls to payload_validator.is_valid() of payload_validator instead of
        form.is_valid().
        :param request: WSGI Request
        :return: Json serialized object if validation passes
        errors as json if validation fails.
        """
        if self.payload_validator.is_valid():
            return self.payload_validator.json_valid()
        else:
            return self.payload_validator.json_invalid()