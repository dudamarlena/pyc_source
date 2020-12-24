# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wojciech/.pyenv/versions/3.7.3/lib/python3.7/site-packages/django_password_validators/password_history/password_validation.py
# Compiled at: 2016-03-01 04:14:54
# Size of source mod 2**32: 2216 bytes
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
import django.utils.translation as _
from django_password_validators.settings import get_password_hasher
from django_password_validators.password_history.models import PasswordHistory, UserPasswordHistoryConfig

class UniquePasswordsValidator(object):
    __doc__ = '\n    Validate whether the password was once used by the user.\n\n    The password is only checked for an existing user.\n    '

    def validate(self, password, user=None):
        if not user:
            return
        for user_config in UserPasswordHistoryConfig.objects.filter(user=user):
            password_hash = user_config.make_password_hash(password)
            try:
                PasswordHistory.objects.get(user_config=user_config,
                  password=password_hash)
                raise ValidationError((_('You can not use a password that is already used in this application.')),
                  code='password_used')
            except PasswordHistory.DoesNotExist:
                pass

    def password_changed(self, password, user=None):
        if not user:
            return
            user_config = UserPasswordHistoryConfig.objects.filter(user=user,
              iterations=(get_password_hasher().iterations)).first()
            if not user_config:
                user_config = UserPasswordHistoryConfig()
                user_config.user = user
                user_config.save()
        else:
            password_hash = user_config.make_password_hash(password)
            try:
                PasswordHistory.objects.get(user_config=user_config,
                  password=password_hash)
            except PasswordHistory.DoesNotExist:
                ols_password = PasswordHistory()
                ols_password.user_config = user_config
                ols_password.password = password_hash
                ols_password.save()

    def get_help_text(self):
        return _('Your new password can not be identical to any of the previously entered.')