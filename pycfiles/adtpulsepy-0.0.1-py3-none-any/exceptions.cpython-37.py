# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tamell/code/adtpulsepy/adtpulsepy/exceptions.py
# Compiled at: 2018-10-26 15:56:13
# Size of source mod 2**32: 554 bytes
"""The exceptions used by ADTPulsePy."""

class ADTPulseException(Exception):
    __doc__ = 'Class to throw general abode exception.'

    def __init__(self, error, details=None):
        """Initialize ADTPulseException."""
        super(ADTPulseException, self).__init__(error[1])
        self.errcode = error[0]
        self.message = error[1]
        self.details = details


class ADTPulseAuthException(ADTPulseException):
    __doc__ = 'Class to throw authentication exception.'