# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/oedialect/error.py
# Compiled at: 2018-09-20 08:32:21
# Size of source mod 2**32: 140 bytes


class CursorError(Exception):

    def __init__(self, message):
        self.message = message


class NotSupportedError(Exception):
    pass