# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/keyring/keyring/backends/OS_X.py
# Compiled at: 2020-01-10 16:25:34
# Size of source mod 2**32: 2001 bytes
import platform, os
from ..backend import KeyringBackend
from ..errors import PasswordSetError
from ..errors import PasswordDeleteError
from ..errors import KeyringLocked
from ..errors import KeyringError
from ..util import properties
try:
    from . import _OS_X_API as api
except Exception:
    pass

class Keyring(KeyringBackend):
    __doc__ = 'macOS Keychain'
    keychain = os.environ.get('KEYCHAIN_PATH')

    @properties.ClassProperty
    @classmethod
    def priority(cls):
        """
        Preferred for all macOS environments.
        """
        if platform.system() != 'Darwin':
            raise RuntimeError('macOS required')
        return 5

    def set_password(self, service, username, password):
        if username is None:
            username = ''
        try:
            api.set_generic_password(self.keychain, service, username, password)
        except api.KeychainDenied as e:
            raise KeyringLocked("Can't store password on keychain: {}".format(e))
        except api.Error as e:
            raise PasswordSetError("Can't store password on keychain: {}".format(e))

    def get_password(self, service, username):
        if username is None:
            username = ''
        try:
            return api.find_generic_password(self.keychain, service, username)
        except api.NotFound:
            pass
        except api.KeychainDenied as e:
            raise KeyringLocked("Can't get password from keychain: {}".format(e))
        except api.Error as e:
            raise KeyringError("Can't get password from keychain: {}".format(e))

    def delete_password(self, service, username):
        if username is None:
            username = ''
        try:
            return api.delete_generic_password(self.keychain, service, username)
        except api.Error as e:
            raise PasswordDeleteError("Can't delete password in keychain: {}".format(e))