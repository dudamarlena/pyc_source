# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/andrean/dev/repos/librarian/greentasks/greentasks/exceptions.py
# Compiled at: 2016-06-15 06:22:07


class BaseTaskError(Exception):
    """
    All exceptions should inherit from this base exception.
    """
    pass


class InvalidTaskError(BaseTaskError):
    """
    Raised when the passed in task cannot be used because it's instantiation
    fails.
    """
    pass