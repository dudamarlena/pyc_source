# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/OpenCobolIDE/open_cobol_ide/extlibs/keyring/backends/fail.py
# Compiled at: 2016-12-30 07:03:15
# Size of source mod 2**32: 662 bytes
from ..backend import KeyringBackend

class Keyring(KeyringBackend):
    __doc__ = "\n    Keyring that raises error on every operation.\n\n    >>> kr = Keyring()\n    >>> kr.get_password('svc', 'user')\n    Traceback (most recent call last):\n    ...\n    RuntimeError: ...No recommended backend...\n    "
    priority = 0

    def get_password(self, service, username, password=None):
        raise RuntimeError('No recommended backend was available. Install the keyrings.alt package if you want to use the non-recommended backends. See README.rst for details.')

    set_password = delete_pasword = get_password