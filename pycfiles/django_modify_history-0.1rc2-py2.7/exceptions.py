# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modify_history/exceptions.py
# Compiled at: 2011-06-10 23:28:22


class HistoryError(Exception):
    """A generic exception for all others to extend."""
    pass


class AlreadyRegistered(HistoryError):
    """Raised when a model is already registered with a site."""
    pass


class NotRegistered(HistoryError):
    """Raised when a model is not registered with a site."""
    pass