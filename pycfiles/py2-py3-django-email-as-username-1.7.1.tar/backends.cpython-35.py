# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/1T/home/Projects/django-email-as-username/emailusernames/backends.py
# Compiled at: 2015-10-23 08:44:12
# Size of source mod 2**32: 859 bytes
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from emailusernames.utils import get_user

class EmailAuthBackend(ModelBackend):
    __doc__ = 'Allow users to log in with their email address'

    def authenticate(self, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get('username')
        try:
            user = get_user(email)
            if user.check_password(password):
                user.backend = '%s.%s' % (self.__module__, self.__class__.__name__)
                return user
        except User.DoesNotExist:
            return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return