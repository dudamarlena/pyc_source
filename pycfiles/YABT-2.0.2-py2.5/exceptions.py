# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/YABT/exceptions.py
# Compiled at: 2009-03-18 06:50:27
"""
This module provides the exception classes for YABT

InvalidStateException: Exception to indicate that the state does not exist
InvalidTranslationTableException: Indicates that the table does not
conform to the format.

"""

class InvalidTranslationTableException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidStateException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)