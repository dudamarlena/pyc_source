# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /uri/part/host.py
# Compiled at: 2018-10-22 09:58:17
# Size of source mod 2**32: 478 bytes
from __future__ import unicode_literals
from socket import inet_pton, AF_INET6, error as SocketError
from .base import ProxyPart

class HostPart(ProxyPart):
    attribute = '_host'

    def render(self, obj, value):
        result = super(HostPart, self).render(obj, value)
        if result:
            try:
                inet_pton(AF_INET6, value)
            except SocketError:
                pass
            else:
                result = '[' + result + ']'
        return result