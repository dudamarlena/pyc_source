# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/binary2text/base64_tool.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 1169 bytes
import base64
from uuid import UUID

class Base64Tool:

    @classmethod
    def uuid2b64(cls, uuid):
        return base64.urlsafe_b64encode(uuid.bytes).decode('utf8').rstrip('=\n')

    @classmethod
    def b642uuid(cls, b64):
        return UUID(bytes=(base64.urlsafe_b64decode(b64 + '==')))

    @classmethod
    def utf82b64(cls, utf8):
        b_utf8 = utf8.encode('UTF-8')
        b_b64 = base64.b64encode(b_utf8)
        b64 = b_b64.decode('UTF-8')
        return b64

    @classmethod
    def b642utf8(cls, b64):
        b_b64 = b64.encode('UTF-8')
        b_utf8 = base64.b64decode(b_b64)
        utf8 = b_utf8.decode('UTF-8')
        return utf8

    @classmethod
    def utf82b64_url(cls, utf8):
        b_utf8 = utf8.encode('UTF-8')
        b_b64 = base64.urlsafe_b64encode(b_utf8)
        b64 = b_b64.decode('UTF-8')
        return b64

    @classmethod
    def b642utf8_url(cls, b64):
        b_b64 = b64.encode('UTF-8')
        b_utf8 = base64.urlsafe_b64decode(b_b64)
        utf8 = b_utf8.decode('UTF-8')
        return utf8