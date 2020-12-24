# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/keyring/keyring/backends/null.py
# Compiled at: 2020-01-10 16:25:34
# Size of source mod 2**32: 344 bytes
from ..backend import KeyringBackend

class Keyring(KeyringBackend):
    __doc__ = "\n    Keyring that return None on every operation.\n\n    >>> kr = Keyring()\n    >>> kr.get_password('svc', 'user')\n    "
    priority = -1

    def get_password(self, service, username, password=None):
        pass

    set_password = delete_password = get_password