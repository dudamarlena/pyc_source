# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pjs/python-modules/webutils/djtools/auth_backends.py
# Compiled at: 2016-05-17 14:52:55
from django.conf import settings
from django.contrib.auth.models import User

class EmailBackend(object):
    supports_anonymous_user = False
    supports_inactive_user = False
    supports_object_permissions = False

    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email__iexact': username}
        else:
            kwargs = {'username__iexact': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return

        return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return

        return