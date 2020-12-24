# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/protocol/TProtocolDecorator.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 1101 bytes


class TProtocolDecorator(object):

    def __new__(cls, protocol, *args, **kwargs):
        decorated_cls = type(''.join(['Decorated', protocol.__class__.__name__]), (
         cls, protocol.__class__), protocol.__dict__)
        return object.__new__(decorated_cls)