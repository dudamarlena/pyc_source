# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/resonate/library/exceptions.py
# Compiled at: 2017-10-04 08:27:16
# Size of source mod 2**32: 230 bytes
"""Generic Exception Class."""

class GenericException(Exception):
    __doc__ = 'Exceptions.'

    def __init__(self, msg):
        """Init."""
        self.msg = msg

    def __str__(self):
        """STR."""
        return self.msg