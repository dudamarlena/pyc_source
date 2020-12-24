# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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