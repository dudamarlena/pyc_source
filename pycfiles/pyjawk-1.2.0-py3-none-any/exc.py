# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/pyjaw/exc.py
# Compiled at: 2009-02-10 14:34:00
__doc__ = 'Contains all the exceptions that can be raised by the Rejaw API'

class RejawError(Exception):
    """The base exception raised by the RejawClient class"""


class SessionRequired(RejawError):
    """Raised when a session is required but not active"""


class SessionActive(RejawError):
    """Raised when a session is already active"""