# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/testutils/helpers/socket.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import six, ipaddress
from sentry.net import socket as net_socket
__all__ = [
 'override_blacklist']

def override_blacklist(*ip_addresses):

    def decorator(func):

        def wrapper(*args, **kwargs):
            disallowed_ips = frozenset(net_socket.DISALLOWED_IPS)
            net_socket.DISALLOWED_IPS = frozenset(ipaddress.ip_network(six.text_type(ip)) for ip in ip_addresses)
            try:
                func(*args, **kwargs)
            finally:
                net_socket.DISALLOWED_IPS = disallowed_ips
                net_socket.is_ipaddress_allowed.cache_clear()

        return wrapper

    return decorator