# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/behave/api/features/common/exception.py
# Compiled at: 2018-09-26 16:15:23
# Size of source mod 2**32: 389 bytes
"""
Commonly used exceptions used in tests.
"""

class BaseBehaveException(Exception):
    message = 'Not Set'

    def __init__(self, message=None):
        super(BaseBehaveException, self).__init__()
        self.message = message or self.message

    def __str__(self):
        return repr(self.message)


class TimeoutException(BaseBehaveException):
    message = 'Request timed out'