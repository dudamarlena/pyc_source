# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/subaligner/exception.py
# Compiled at: 2020-01-25 08:37:53
# Size of source mod 2**32: 222 bytes


class UnsupportedFormatException(Exception):
    __doc__ = ' An exception raised due to unsupported formats.'


class TerminalException(Exception):
    __doc__ = ' An exception raised due to unrecoverable failures.'