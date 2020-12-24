# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\tokens\magic_token_generator.py
# Compiled at: 2020-01-28 13:32:35
# Size of source mod 2**32: 783 bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings

class MagicTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        """
        Make hash value with user attributes and timestamp  
        """
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=100, tzinfo=None)
        if hasattr(settings, 'AUTH_USER_MODEL'):
            if getattr(settings, 'AUTH_USER_MODEL') == 'CustomAuth.PhoneNumberUser':
                return str(user.pk) + str(user.cellphone) + str(user.password) + str(login_timestamp) + str(timestamp)
        return str(user.pk) + str(user.email) + str(user.password) + str(login_timestamp) + str(timestamp)