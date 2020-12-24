# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/pyjaw/exc.py
# Compiled at: 2009-02-10 14:34:00
"""Contains all the exceptions that can be raised by the Rejaw API"""

class RejawError(Exception):
    """The base exception raised by the RejawClient class"""
    pass


class SessionRequired(RejawError):
    """Raised when a session is required but not active"""
    pass


class SessionActive(RejawError):
    """Raised when a session is already active"""
    pass