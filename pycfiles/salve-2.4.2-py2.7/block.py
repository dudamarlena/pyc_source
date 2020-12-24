# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/exceptions/block.py
# Compiled at: 2015-11-06 23:45:35
from salve.exceptions.base import SALVEException

class BlockException(SALVEException):
    """
    A SALVE exception specialized for blocks.
    """

    def __init__(self, msg, file_context):
        """
        BlockException constructor

        Args:
            @msg
            A string message that describes the error or exception.
            @file_context
            A FileContext that identifies the origin of this
            exception.
        """
        SALVEException.__init__(self, msg, file_context=file_context)