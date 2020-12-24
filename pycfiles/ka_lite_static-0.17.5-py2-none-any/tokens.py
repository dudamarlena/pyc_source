# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/auth/tokens.py
# Compiled at: 2018-07-11 18:15:30
from datetime import date
from django.conf import settings
from django.utils.http import int_to_base36, base36_to_int
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils import six

class PasswordResetTokenGenerator(object):
    """
    Strategy object used to generate and check tokens for the password
    reset mechanism.
    """

    def make_token(self, user):
        """
        Returns a token that can be used once to do a password reset
        for the given user.
        """
        return self._make_token_with_timestamp(user, self._num_days(self._today()))

    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        try:
            ts_b36, hash = token.split('-')
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return False
        if self._num_days(self._today()) - ts > settings.PASSWORD_RESET_TIMEOUT_DAYS:
            return False
        return True

    def _make_token_with_timestamp(self, user, timestamp):
        ts_b36 = int_to_base36(timestamp)
        key_salt = 'django.contrib.auth.tokens.PasswordResetTokenGenerator'
        login_timestamp = user.last_login.replace(microsecond=0, tzinfo=None)
        value = six.text_type(user.pk) + user.password + six.text_type(login_timestamp) + six.text_type(timestamp)
        hash = salted_hmac(key_salt, value).hexdigest()[::2]
        return '%s-%s' % (ts_b36, hash)

    def _num_days(self, dt):
        return (dt - date(2001, 1, 1)).days

    def _today(self):
        return date.today()


default_token_generator = PasswordResetTokenGenerator()