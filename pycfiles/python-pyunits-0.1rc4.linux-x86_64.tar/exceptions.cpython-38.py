# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/exceptions.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 300 bytes


class UnitError(Exception):
    __doc__ = '\n    General error for units.\n    '


class CastError(Exception):
    __doc__ = '\n    Raised when a cast fails.\n    '


class InterningError(Exception):
    __doc__ = '\n    Raised when we try to use an interned class in a way that would break the\n    pattern.\n    '