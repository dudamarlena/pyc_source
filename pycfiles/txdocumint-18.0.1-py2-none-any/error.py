# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathan/Coding/txdocumint/txdocumint/error.py
# Compiled at: 2016-02-08 15:11:42


class DocumintErrorCause(object):
    """
    Specific error cause.
    """

    def __init__(self, type, reason, description=None):
        self.type = type
        self.reason = reason
        self.description = description

    def __repr__(self):
        return ('<{} type={} reason={} description={}>').format(self.__class__.__name__, self.type, self.reason, self.description)


class DocumintError(RuntimeError):
    """
    Structured Documint error.
    """

    def __init__(self, causes):
        RuntimeError.__init__(self, causes)
        self.causes = causes


class MalformedDocumintError(RuntimeError):
    """
    An error, indicated by status code, was malformed.

    :ivar bytes data: Error response data.
    """

    def __init__(self, data):
        RuntimeError.__init__(self, data)
        self.data = data


__all__ = [
 'DocumintError', 'MalformedDocumintError']