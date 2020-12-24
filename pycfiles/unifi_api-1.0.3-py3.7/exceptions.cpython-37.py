# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/unifi/exceptions.py
# Compiled at: 2018-07-05 17:45:37
# Size of source mod 2**32: 250 bytes
from __future__ import print_function

class APIError(Exception):
    pass


class CredentialsMissing(Exception):
    __doc__ = ' username or password are missing. '


class ConnectionError(Exception):
    pass