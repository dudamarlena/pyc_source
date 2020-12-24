# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/requests-toolbelt/requests_toolbelt/auth/_digest_auth_compat.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 910 bytes
"""Provide a compatibility layer for requests.auth.HTTPDigestAuth."""
import requests

class _ThreadingDescriptor(object):

    def __init__(self, prop, default):
        self.prop = prop
        self.default = default

    def __get__(self, obj, objtype=None):
        return getattr(obj._thread_local, self.prop, self.default)

    def __set__(self, obj, value):
        setattr(obj._thread_local, self.prop, value)


class _HTTPDigestAuth(requests.auth.HTTPDigestAuth):
    init = _ThreadingDescriptor('init', True)
    last_nonce = _ThreadingDescriptor('last_nonce', '')
    nonce_count = _ThreadingDescriptor('nonce_count', 0)
    chal = _ThreadingDescriptor('chal', {})
    pos = _ThreadingDescriptor('pos', None)
    num_401_calls = _ThreadingDescriptor('num_401_calls', 1)


if requests.__build__ < 133120:
    HTTPDigestAuth = requests.auth.HTTPDigestAuth
else:
    HTTPDigestAuth = _HTTPDigestAuth