# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/accounts/auth.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1300 bytes
from hashlib import sha256
import bcrypt
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from callisto_core.accounts.models import Account

def index(src, length=8):
    """Computes an index suitable for fast lookups on a user record."""
    base = f"{src}//{settings.INDEXING_KEY}"
    cipher = sha256(base.encode('utf-8')).hexdigest()
    return cipher[0:length]


class EncryptedBackend:
    __doc__ = 'Authenticates against encrypted credentials stored in the DB.'

    def authenticate(self, request, username, password):
        username = sha256(username.encode('utf-8')).hexdigest()
        username_index = index(username)
        for user in Account.objects.filter(username_index=username_index):
            if not user or not bcrypt.checkpw(username.encode('utf-8'), user.encrypted_username.encode('utf-8')):
                return
            else:
                if not check_password(password, user.user.password):
                    return
                return self.get_user(user.user.id)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return