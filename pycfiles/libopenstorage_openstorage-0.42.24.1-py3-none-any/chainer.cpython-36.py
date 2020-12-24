# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/keyring/keyring/backends/chainer.py
# Compiled at: 2020-01-10 16:25:34
# Size of source mod 2**32: 1972 bytes
"""
Keyring Chainer - iterates over other viable backends to
discover passwords in each.
"""
from .. import backend
from ..util import properties

class ChainerBackend(backend.KeyringBackend):
    __doc__ = '\n    >>> ChainerBackend()\n    <keyring.backends.chainer.ChainerBackend object at ...>\n    '
    viable = True

    @properties.ClassProperty
    @classmethod
    def priority(cls):
        """
        High-priority if there are backends to chain, otherwise 0.
        """
        return 10 * (len(cls.backends) > 1)

    @properties.ClassProperty
    @classmethod
    def backends(cls):
        """
        Discover all keyrings for chaining.
        """
        allowed = (keyring for keyring in filter(backend._limit, backend.get_all_keyring()) if not isinstance(keyring, ChainerBackend) if keyring.priority > 0)
        return sorted(allowed, key=(backend.by_priority), reverse=True)

    def get_password(self, service, username):
        for keyring in self.backends:
            password = keyring.get_password(service, username)
            if password is not None:
                return password

    def set_password(self, service, username, password):
        for keyring in self.backends:
            try:
                return keyring.set_password(service, username, password)
            except NotImplementedError:
                pass

    def delete_password(self, service, username):
        for keyring in self.backends:
            try:
                return keyring.delete_password(service, username)
            except NotImplementedError:
                pass

    def get_credential(self, service, username):
        for keyring in self.backends:
            credential = keyring.get_credential(service, username)
            if credential is not None:
                return credential