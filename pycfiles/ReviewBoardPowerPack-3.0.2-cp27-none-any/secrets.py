# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/sshdb/secrets.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import logging
from django.conf import settings

def get_sshdb_secret_key():
    """Returns the Secret Key for encryption.

    If settings.SSHDB_SECRET_KEY is defined, this will be used as the
    secret key. Otherwise, the first 32 characters of settings.SECRET_KEY
    will be used.

    Both keys are accepted for backwards-compatibility reasons (as
    RBCommons and reviews.reviewboard.org use it). It also gives admins
    the option, if they choose, to keep these secrets separate.

    Only the first 32 characters are used because we encrypt with AES-256,
    which requires a 32 character encryption key.
    """
    key = getattr(settings, b'SSHDB_SECRET_KEY', None)
    if not key:
        key = settings.SECRET_KEY
    if not key or len(key) < 32:
        logging.error(b'Review Board Power Pack needs a settings.SSHDB_SECRET_KEY or settings.SECRET_KEY >= 32 bytes.')
        return
    else:
        return key[:32]


def has_valid_sshdb_secret_key():
    """Returns whether or not there's a valid secret key."""
    return get_sshdb_secret_key() is not None