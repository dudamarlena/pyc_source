# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/_pure_sasl.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 1046 bytes
__version__ = '0.5.1'
__version_info__ = (0, 5, 1)

class SASLError(Exception):
    """SASLError"""
    pass


class SASLProtocolException(Exception):
    """SASLProtocolException"""
    pass


class SASLWarning(Warning):
    """SASLWarning"""
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