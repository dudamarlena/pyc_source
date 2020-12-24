# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
     type(''), type(''))
    text_type = unicode
    COMPACT_SEPARATORS = (',', ':')
    VERBOSE_SEPARATORS = (',', ': ')
    from urlparse import urlparse

    def copy_signature(copy_from, copy_to):
        copy_to._argspec = getargspec(copy_from)


    def getargspec(func):
        return getattr(func, '_argspec', inspect.getargspec(func))


    Base64DecodeError = TypeError