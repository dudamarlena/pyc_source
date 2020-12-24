# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wursterk/code/tinyflow/venv/lib/python3.6/site-packages/tinyflow/exceptions.py
# Compiled at: 2017-03-15 21:10:24
# Size of source mod 2**32: 986 bytes
"""Exceptions, error handlers, and high level validators."""

class TinyFlowException(Exception):
    __doc__ = 'Base exception for ``tinyflow``.'


class NotAnOperation(TinyFlowException):
    __doc__ = "Raise when an object should be an instance of\n    ``tinyflow.ops.Operation()`` but isn't.\n    "


class NotACoroOperation(NotAnOperation):
    __doc__ = 'Like ``NotAnOperation()`` but for ``tinyflow.coro.ops``.'


class NotACoroTarget(NotACoroOperation):
    __doc__ = 'Like ``NotACoroOperation()`` but for coroutine targets.'


class TooManyTargets(TinyFlowException):
    __doc__ = "Raised when a ``tinyflow.coro.CoroPipeline()`` receives too many\n    ``tinyflow.coro.ops.CoroTarget()``'s.\n    "


class NoPipeline(TinyFlowException):
    __doc__ = 'Raised when an operation has not been attached to a pipeline, but\n    requests its parent pipeline.\n    '


class NoPool(TinyFlowException):
    __doc__ = 'Raised when a thread or process pool is requested but was not passed\n    to ``tinyflow.Pipeline()``.\n    '