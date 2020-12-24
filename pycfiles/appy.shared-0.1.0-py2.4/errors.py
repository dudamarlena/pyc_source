# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/shared/errors.py
# Compiled at: 2008-02-21 11:38:58


class AppyError(Exception):
    """Root Appy exception class."""
    __module__ = __name__


class ValidationError(AppyError):
    """Represents an error that occurs on data sent to the Appy server."""
    __module__ = __name__


class InternalError(AppyError):
    """Represents a programming error: something that should never occur."""
    __module__ = __name__