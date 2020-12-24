# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/exceptions/DatabaseNotFoundException.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 294 bytes
"""
An Exception to be raised when a database could not be found.
"""

class DatabaseNotFoundException(Exception):

    def __init__(self, msg):
        super().__init__(msg)