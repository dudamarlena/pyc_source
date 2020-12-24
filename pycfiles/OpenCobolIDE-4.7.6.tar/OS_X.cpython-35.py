# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/backends/OS_X.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 1475 bytes
import platform
from ..backend import KeyringBackend
from ..errors import PasswordSetError
from ..errors import PasswordDeleteError
from ..util import properties
try:
    from . import _OS_X_API as api
except Exception:
    pass

class Keyring(KeyringBackend):
    __doc__ = 'Mac OS X Keychain'
    keychain = None

    @properties.ClassProperty
    @classmethod
    def priority(cls):
        """
        Preferred for all OS X environments.
        """
        if platform.system() != 'Darwin':
            raise RuntimeError('OS X required')
        return 5

    def set_password(self, service, username, password):
        if username is None:
            username = ''
        try:
            api.set_generic_password(self.keychain, service, username, password)
        except api.Error:
            raise PasswordSetError("Can't store password on keychain")

    def get_password(self, service, username):
        if username is None:
            username = ''
        try:
            return api.find_generic_password(self.keychain, service, username)
        except api.NotFound:
            pass

    def delete_password(self, service, username):
        if username is None:
            username = ''
        try:
            return api.delete_generic_password(self.keychain, service, username)
        except api.Error:
            raise PasswordDeleteError("Can't delete password in keychain")