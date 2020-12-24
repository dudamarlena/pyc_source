# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ant/core/exceptions.py
# Compiled at: 2011-10-07 13:47:21


class ANTException(Exception):
    pass


class DriverError(ANTException):
    pass


class MessageError(ANTException):

    def __init__(self, msg, internal=''):
        Exception.__init__(self, msg)
        self.internal = internal


class NodeError(ANTException):
    pass


class ChannelError(ANTException):
    pass