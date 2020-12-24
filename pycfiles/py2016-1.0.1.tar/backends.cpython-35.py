# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/1T/home/Projects/django-email-as-username/emailusernames/backends.py
# Compiled at: 2015-10-23 08:44:12
# Size of source mod 2**32: 859 bytes
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from emailusernames.utils import get_user

class EmailAuthBackend(ModelBackend):
    """EmailAuthBackend"""

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