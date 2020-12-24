# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/dev_reactor/django-reactor/manifest/backends.py
# Compiled at: 2019-10-15 15:31:29
# Size of source mod 2**32: 1825 bytes
""" Manifest Backends
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core import validators

class AuthenticationBackend(ModelBackend):
    __doc__ = '\n    Custom backend to allow user login with entering\n    either an ``email`` or ``username``.\n\n    '

    def authenticate(self, request, identification, password=None, check_password=True):
        """
        Authenticates user by either email or username with password.

        :param identification:
            String containing email or username.

        :password:
            Optional string containing the password for the user.

        :param check_password:
            Boolean, default is ``True``. User will be authenticated
            without password if ``False``. This is only used for authenticate
            the user when visiting specific pages with a secret token.

        :return: The logged in :class:`User`.

        """
        user_model = get_user_model()
        try:
            validators.validate_email(identification)
            try:
                user = user_model.objects.get(email__iexact=identification)
            except user_model.DoesNotExist:
                return

        except validators.ValidationError:
            try:
                user = user_model.objects.get(username__iexact=identification)
            except user_model.DoesNotExist:
                return

        if check_password:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return