# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/loradecoder/loraExceptions.py
# Compiled at: 2016-06-20 07:00:28
"""
This module contains exceptions raised when an operation
on the LoraWAN data fails, 
for example: missing formats, invalid values, etc.

At the moment two exception classes are provided: 
- ``loraPayloadException``: raised for exceptions caused by API calls
- ``loraDecoderException``: raised for other exceptions
"""

class loraPayloadException(Exception):
    """
    LoraPayLoadException
    """
    pass


class loraDecoderException(Exception):
    """
    loraDecoderException
    """
    pass