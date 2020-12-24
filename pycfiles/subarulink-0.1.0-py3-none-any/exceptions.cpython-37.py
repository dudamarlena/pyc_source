# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/data/proj/subarulink/subarulink/exceptions.py
# Compiled at: 2020-03-22 16:18:57
# Size of source mod 2**32: 1679 bytes
"""
Python Package for controlling Subaru Starlink API.

For more details about this api, please refer to the documentation at
https://github.com/G-Two/subarulink
"""

class SubaruException(Exception):
    __doc__ = 'Class of Subaru API exceptions.'

    def __init__(self, message, *args, **kwargs):
        self.message = message
        (super().__init__)(*args, **kwargs)


class RetryLimitError(SubaruException):
    __doc__ = 'Class of exceptions for hitting retry limits.'

    def __init__(self, *args, **kwargs):
        """Initialize exceptions for the Subaru retry limit API."""
        pass


class IncompleteCredentials(SubaruException):
    __doc__ = 'Class of exceptions for hitting retry limits.'

    def __init__(self, *args, **kwargs):
        """Initialize exceptions for the Subaru retry limit API."""
        pass