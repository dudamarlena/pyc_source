# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ssh_ldap_pubkey/exceptions.py
# Compiled at: 2019-08-20 19:18:36
# Size of source mod 2**32: 503 bytes


class Error(Exception):

    def __init__(self, msg, code=1):
        self.msg = msg
        self.code = code

    def __str__(self):
        return self.msg


class ConfigError(Error):
    pass


class InsufficientAccessError(Error):
    pass


class InvalidCredentialsError(Error):
    pass


class InvalidPubKeyError(Error):
    pass


class LDAPConnectionError(Error):
    pass


class NoPubKeyFoundError(Error):
    pass


class PubKeyAlreadyExistsError(Error):
    pass


class UserEntryNotFoundError(Error):
    pass