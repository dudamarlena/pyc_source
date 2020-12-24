# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/compat.py
# Compiled at: 2016-04-19 08:21:44
# Size of source mod 2**32: 1114 bytes
import binascii, inspect, sys
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (
     str,)
    text_type = str
    COMPACT_SEPARATORS = (',', ':')
    VERBOSE_SEPARATORS = (',', ': ')
    from urllib.parse import urlparse

    def copy_signature(copy_from, copy_to):
        copy_to.__signature__ = inspect.signature(copy_from)


    def getargspec(func):
        return inspect.getargspec(func)


    Base64DecodeError = binascii.Error
else:
    string_types = (
     type(b''), type(''))
    text_type = unicode
    COMPACT_SEPARATORS = (b',', b':')
    VERBOSE_SEPARATORS = (b',', b': ')
    from urlparse import urlparse

    def copy_signature(copy_from, copy_to):
        copy_to._argspec = getargspec(copy_from)


    def getargspec(func):
        return getattr(func, '_argspec', inspect.getargspec(func))


    Base64DecodeError = TypeError