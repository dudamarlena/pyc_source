# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/maegen/core/exceptions.py
# Compiled at: 2011-11-21 11:50:15
"""
Created on Oct 29, 2011

@author: maemo
"""
from ..common import version
version.getInstance().submitRevision('$Revision: 72 $')

class MaegenException(Exception):
    """
    Base class for all application exception
    """

    def __init_(self, message=None, cause=None):
        self.meseage = message
        self.cause = cause

    def __str__(self):
        if cause:
            return repr(self.message) + 'caused by \n' + repr(self.cause)
        else:
            return repr(self.message)


class MaegenIntegrityExceptiopn(MaegenException):
    """
    A database intéegrity error was detected
    """
    pass