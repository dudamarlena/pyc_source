# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snakeflake/exceptions.py
# Compiled at: 2020-03-04 03:29:14
# Size of source mod 2**32: 180 bytes
"""Defines Custom Exceptions"""

class ExceededTimeException(Exception):
    pass


class ExceededBitsException(Exception):
    pass


class EpochFutureException(Exception):
    pass