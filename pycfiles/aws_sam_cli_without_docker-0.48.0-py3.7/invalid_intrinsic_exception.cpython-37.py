# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/intrinsic_resolver/invalid_intrinsic_exception.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 189 bytes
"""
A custom Exception to display Invalid Intrinsics and Symbol Table format.
"""

class InvalidIntrinsicException(Exception):
    pass


class InvalidSymbolException(Exception):
    pass