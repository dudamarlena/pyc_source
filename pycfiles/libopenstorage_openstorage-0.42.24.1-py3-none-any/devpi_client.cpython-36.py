# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/keyring/keyring/devpi_client.py
# Compiled at: 2020-01-10 16:25:34
# Size of source mod 2**32: 199 bytes
from pluggy import HookimplMarker
import keyring
hookimpl = HookimplMarker('devpiclient')

@hookimpl()
def devpiclient_get_password(url, username):
    return keyring.get_password(url, username)