# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/00P/01-dajngo/3d/app/usuarios/tokens.py
# Compiled at: 2018-03-28 11:52:26
# Size of source mod 2**32: 422 bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.cliente.email_confirmed)


account_activation_token = AccountActivationTokenGenerator()