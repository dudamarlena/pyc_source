# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/exceptions/parsing.py
# Compiled at: 2015-11-06 23:45:35
from salve.exceptions.base import SALVEException

class ParsingException(SALVEException):
    """
    A specialized exception for parsing errors.

    A ParsingException (PE) often carres the token that tripped the
    exception in its message.
    """

    def __init__(self, msg, file_context):
        """
        ParsingException constructor

        Args:
            @msg
            A string message that describes the error.
            @file_context
            The FileContext.
        """
        SALVEException.__init__(self, msg, file_context)


class TokenizationException(ParsingException):
    """
    A SALVE exception specialized for tokenization.
    """

    def __init__(self, msg, file_context):
        """
        TokenizationException constructor

        Args:
            @msg
            A string message that describes the error.
            @file_context
            The FileContext.
        """
        SALVEException.__init__(self, msg, file_context)