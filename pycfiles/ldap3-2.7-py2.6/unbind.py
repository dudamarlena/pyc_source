# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\operation\unbind.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from ..protocol.rfc4511 import UnbindRequest

def unbind_operation():
    request = UnbindRequest()
    return request