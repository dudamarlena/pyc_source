# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\socket_says\custom_errors.py
# Compiled at: 2020-04-19 22:10:15
# Size of source mod 2**32: 95 bytes


class BadPortError(Exception):
    pass


class BadAddressError(Exception):
    pass