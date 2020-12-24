# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/cerebro/_pure_sasl.py
# Compiled at: 2018-05-22 15:24:37
# Size of source mod 2**32: 943 bytes
__version__ = '0.4.0'
__version_info__ = (0, 4, 0)

class SASLError(Exception):
    """SASLError"""
    pass


class SASLProtocolException(Exception):
    """SASLProtocolException"""
    pass


class QOP(object):
    AUTH = 'auth'
    AUTH_INT = 'auth-int'
    AUTH_CONF = 'auth-conf'
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