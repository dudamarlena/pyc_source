# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\GitHub\django-encrypted-cookie-session-py3\encrypted_cookies\crypto.py
# Compiled at: 2015-10-17 09:18:47
# Size of source mod 2**32: 979 bytes
import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from cryptography import fernet

def encrypt(plaintext_bytes):
    """
    Returns an encrypted version of plaintext_bytes.

    The encrypted value is a URL-encoded base 64 value.
    """
    return configure_fernet().encrypt(plaintext_bytes)


def decrypt(encrypted_bytes):
    """
    Returns a decrypted version of encrypted_bytes.
    """
    return configure_fernet().decrypt(encrypted_bytes)


def configure_fernet():
    keys = list(getattr(settings, 'ENCRYPTED_COOKIE_KEYS', None) or [])
    if not len(keys):
        raise ImproperlyConfigured('The ENCRYPTED_COOKIE_KEYS settings cannot be empty.')
    return fernet.MultiFernet([fernet.Fernet(k) for k in keys])