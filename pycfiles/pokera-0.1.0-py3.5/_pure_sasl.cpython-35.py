# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/cerebro/_pure_sasl.py
# Compiled at: 2018-05-22 15:24:37
# Size of source mod 2**32: 943 bytes
__version__ = '0.4.0'
__version_info__ = (0, 4, 0)

class SASLError(Exception):
    __doc__ = '\n    Typically represents a user error in configuration or usage of the\n    SASL client or mechanism.\n    '


class SASLProtocolException(Exception):
    __doc__ = '\n    Raised when an error occurs while communicating with the SASL server\n    or the client and server fail to agree on negotiated properties such\n    as quality of protection.\n    '


class QOP(object):
    AUTH = b'auth'
    AUTH_INT = b'auth-int'
    AUTH_CONF = b'auth-conf'
    all = (
     AUTH, AUTH_INT, AUTH_CONF)
    bit_map = {1: AUTH, 2: AUTH_INT, 4: AUTH_CONF}
    name_map = dict((bit, name) for name, bit in bit_map.items())

    @classmethod
    def names_from_bitmask(cls, byt):
        return set(name for bit, name in cls.bit_map.items() if bit & byt)

    @classmethod
    def flag_from_name(cls, name):
        return cls.name_map[name]