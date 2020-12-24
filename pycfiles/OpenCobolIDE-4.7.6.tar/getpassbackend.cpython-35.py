# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/getpassbackend.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 312 bytes
"""Specific support for getpass."""
import getpass
from . import core

def get_password(prompt='Password: ', stream=None, service_name='Python', username=None):
    if username is None:
        username = getpass.getuser()
    return core.get_password(service_name, username)