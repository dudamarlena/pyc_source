# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scanless/exceptions.py
# Compiled at: 2020-04-13 14:39:06
# Size of source mod 2**32: 120 bytes
"""scanless.exceptions"""

class ScannerNotFound(Exception):
    pass


class ScannerRequestError(Exception):
    pass