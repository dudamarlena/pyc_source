# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/exception.py
# Compiled at: 2018-05-31 03:53:16
__authors__ = [
 'TimChow']

class MVCError(StandardError):
    pass


class MissingArgumentError(MVCError):
    pass


class InvalidArgumentError(MVCError):
    pass


class InvalidReturnValueError(MVCError):
    pass


class InvalidRedirectURLError(MVCError):
    pass


class InterceptError(MVCError):
    pass


class NoHandlerFoundError(MVCError):
    pass


class NoAdapterFoundError(MVCError):
    pass


class UnkownRequestMethodError(MVCError):
    pass


class MaxRedirectCountReached(MVCError):
    pass