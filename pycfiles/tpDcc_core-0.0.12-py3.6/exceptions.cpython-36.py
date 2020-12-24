# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/core/exceptions.py
# Compiled at: 2020-05-13 19:27:59
# Size of source mod 2**32: 309 bytes
"""
Module that contains consts exception used by libraries
"""
from __future__ import print_function, division, absolute_import

class DccError(Exception):
    pass


class NoMatchFoundError(DccError):
    pass


class NoObjectFoundError(DccError):
    pass