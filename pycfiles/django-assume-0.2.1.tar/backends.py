# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bryan/.virtualenvs/egather/lib/python2.6/site-packages/assume/backends.py
# Compiled at: 2010-11-16 05:26:25
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class AssumableModelBackend(ModelBackend):
    """
    Custom authentication backend that allows authentication without a
    password.

    IMPORTANT: This backend assumes that the credentials have already been
    verified if a password is not passed to authenticate(), so all calls to
    that method should be done very carefully.
    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if password == None:
                return user
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return

        return


class AssumableEmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows logging in using either username
    or email address, and allows authentication without a password.

    IMPORTANT: This backend assumes that the credentials have already been
    verified if a password is not passed to authenticate(), so all calls to
    that method should be done very carefully.
    """

    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if password == None:
                return user
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return

        return