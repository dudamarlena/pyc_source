# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/networking.py
# Compiled at: 2017-06-08 00:03:15
# Size of source mod 2**32: 334 bytes
SOCK_PROTOCOL_VERSION = 5

class AddressType:
    IPv4 = 1
    IPv6 = 4
    DomainName = 3


class ConnectionStatus:
    SUCCEEDED = 0
    GENERAL_FAIL = 1
    NOT_ALLOWED_BY_RULESET = 2
    NETWORK_UNREACHABLE = 3
    HOST_UNREACHABLE = 4
    CONN_REFUSED = 5
    TTL_EXPIRED = 6
    COMM_NOT_SUPP = 7
    ATYP_NOT_SUPP = 8