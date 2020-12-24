# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/tamell/code/adtpulsepy/adtpulsepy/exceptions.py
# Compiled at: 2018-10-26 15:56:13
# Size of source mod 2**32: 554 bytes
__doc__ = 'The exceptions used by ADTPulsePy.'

class ADTPulseException(Exception):
    """ADTPulseException"""

    def __init__(self, error, details=None):
        """Initialize ADTPulseException."""
        super(ADTPulseException, self).__init__(error[1])
        self.errcode = error[0]
        self.message = error[1]
        self.details = details


class ADTPulseAuthException(ADTPulseException):
    """ADTPulseAuthException"""
    pass