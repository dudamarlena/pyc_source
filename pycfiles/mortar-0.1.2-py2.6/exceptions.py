# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/exceptions.py
# Compiled at: 2008-12-19 12:41:15


class NotPossible(Exception):
    """
    Base class for things that didn't work
    """
    pass


class NotAllowed(NotPossible):
    """
    User not authorised to perform action.
    """
    pass


class NotFound(NotPossible):
    """
    No value was found
    """
    pass


class NotSupported(NotPossible):
    """
    This action is never going to be possible.
    ie:writing to field whose name does not have a matching relational column.
    """
    pass