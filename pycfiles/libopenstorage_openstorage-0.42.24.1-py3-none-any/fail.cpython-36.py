# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/keyring/keyring/backends/fail.py
# Compiled at: 2020-01-10 16:25:34
# Size of source mod 2**32: 765 bytes
from ..backend import KeyringBackend

class Keyring(KeyringBackend):
    __doc__ = "\n    Keyring that raises error on every operation.\n\n    >>> kr = Keyring()\n    >>> kr.get_password('svc', 'user')\n    Traceback (most recent call last):\n    ...\n    RuntimeError: ...No recommended backend...\n    "
    priority = 0

    def get_password(self, service, username, password=None):
        msg = 'No recommended backend was available. Install a recommended 3rd party backend package; or, install the keyrings.alt package if you want to use the non-recommended backends. See https://pypi.org/project/keyring for details.'
        raise RuntimeError(msg)

    set_password = delete_password = get_password