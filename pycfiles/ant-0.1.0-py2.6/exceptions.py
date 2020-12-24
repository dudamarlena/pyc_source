# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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