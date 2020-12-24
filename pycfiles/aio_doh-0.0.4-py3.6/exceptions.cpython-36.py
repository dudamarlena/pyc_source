# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doh/exceptions.py
# Compiled at: 2017-12-16 15:37:57
# Size of source mod 2**32: 1299 bytes
__all__ = ['DNSException', 'FormErr', 'ServFail', 'NXDomain', 'NotImpl',
 'Refused', 'YXDomain', 'XRRSet', 'NotAuth', 'NotZone', 'DOHException']

class DNSException(Exception):

    @classmethod
    def from_response(cls, response):
        code = response['Status']
        assert 1 <= code <= 9
        exc_class = cls.__subclasses__()[(code - 1)]
        return exc_class(response.get('comment', exc_class.__doc__))


class FormErr(DNSException):
    __doc__ = 'DNS query format error\n    '
    code = 1


class ServFail(DNSException):
    __doc__ = 'Server failed to complete the DNS request\n    '
    code = 2


class NXDomain(DNSException):
    __doc__ = 'Domain name does not exist\n    '
    code = 3


class NotImpl(DNSException):
    __doc__ = 'Function not implemented\n    '
    code = 4


class Refused(DNSException):
    __doc__ = 'The server refused to answer for the reply\n    '
    code = 5


class YXDomain(DNSException):
    __doc__ = 'Name that should not exist, does exist\n    '
    code = 6


class XRRSet(DNSException):
    __doc__ = 'RRset that should not exist, does exist\n    '
    code = 7


class NotAuth(DNSException):
    __doc__ = 'Server not authoritative for the zone\n    '
    code = 8


class NotZone(DNSException):
    __doc__ = 'Name not in zone\n    '
    code = 9


class DOHException(Exception):
    pass