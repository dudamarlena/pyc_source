# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/compat.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1610 bytes
import sys, noval.util.utils as utils
if utils.is_py2():
    from base64 import encodestring as b64_encode_bytes
    from base64 import decodestring as b64_decode_bytes

    def ensure_bytes(s, encoding='utf-8', errors='strict'):
        if isinstance(s, unicode):
            return s.encode(encoding, errors)
        if isinstance(s, str):
            return s
        raise ValueError('Expected str or unicode, received %s.' % type(s))


    def ensure_string(s, encoding='utf-8', errors='strict'):
        if isinstance(s, unicode):
            return s.encode(encoding, errors)
        if isinstance(s, str):
            return s
        raise ValueError('Expected str or unicode, received %s.' % type(s))


else:
    from base64 import encodebytes as b64_encode_bytes
    from base64 import decodebytes as b64_decode_bytes

    def ensure_bytes(s, encoding='utf-8', errors='strict'):
        if isinstance(s, str):
            return bytes(s, encoding=encoding)
        if isinstance(s, bytes):
            return s
        if isinstance(s, bytearray):
            return bytes(s)
        raise ValueError('Expected str or bytes or bytearray, received %s.' % type(s))


    def ensure_string(s, encoding='utf-8', errors='strict'):
        if isinstance(s, str):
            return s
        if isinstance(s, (bytes, bytearray)):
            return str(s, encoding=encoding)
        raise ValueError('Expected str or bytes or bytearray, received %s.' % type(s))


if sys.version_info[:2] == (2, 6):
    import simplejson as json
else:
    import json