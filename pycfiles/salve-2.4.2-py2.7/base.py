# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/exceptions/base.py
# Compiled at: 2015-11-06 23:45:35


class SALVEException(Exception):
    """
    A specialized exception for errors specific to SALVE.
    """

    def __init__(self, message, file_context):
        """
        SALVEException constructor.

        Args:
            @message
            The string to be reported by the error.
            @file_context
            A FileContext to be included in the error message.
        """
        Exception.__init__(self, message)
        self.message = message
        self.file_context = file_context