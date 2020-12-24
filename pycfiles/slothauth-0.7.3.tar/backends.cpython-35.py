# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/backends.py
# Compiled at: 2016-03-10 19:24:34
# Size of source mod 2**32: 1385 bytes
from django.contrib.auth import get_user_model
Account = get_user_model()

class PasswordlessAuthentication(object):

    def authenticate(self, email=None, username=None, password=None, passwordless_key=None, one_time_authentication_key=None, force=False, **kwargs):
        if username:
            email = username
        user = None
        if email and password:
            user = Account.objects.filter(email__iexact=email).last()
            if user and not user.check_password(password):
                user = None
        else:
            if passwordless_key:
                user = Account.objects.filter(passwordless_key=passwordless_key).last()
                if user and not user.is_passwordless and not force:
                    user = None
            elif one_time_authentication_key:
                user = Account.objects.filter(one_time_authentication_key=one_time_authentication_key).last()
        if user:
            user.one_time_authentication_key = Account._meta.get_field('one_time_authentication_key').generate_unique(instance=user, sender=Account)
            user.save()
        return user

    def get_user(self, user_id):
        return Account.objects.filter(id=user_id).last()