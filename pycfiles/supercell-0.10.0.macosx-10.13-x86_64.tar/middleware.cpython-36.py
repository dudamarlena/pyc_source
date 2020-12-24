# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jannis/Documents/code/rtr-supercell/supercell/env3/lib/python3.6/site-packages/supercell/middleware.py
# Compiled at: 2018-10-08 11:55:52
# Size of source mod 2**32: 2623 bytes
from __future__ import absolute_import, division, print_function, with_statement
from abc import ABCMeta, abstractmethod
from functools import wraps
from schematics.models import Model
from tornado.gen import coroutine, Return
from supercell._compat import with_metaclass
from supercell.mediatypes import ReturnInformationT

class Middleware(with_metaclass(ABCMeta, object)):
    __doc__ = 'Base class for middleware implementations.\n\n    Each request handler is assigned a list of `Middleware` implementations.\n    Before a handler is called, each middleware is executed using the\n    `Middleware.before` method. When the underlying handler is finished, the\n    `Middleware.after` method may manipulate the result.\n    '

    def __init__(self, *args, **kwargs):
        """Initialize the decorator and register the `after()` callback."""
        pass

    def __call__(self, fn):
        """Call the `before()` method and then the decorated method. If this
        returns a `Future`, add the `after()` method as a `done` callback.
        Otherwise execute it immediately.
        """

        @coroutine
        @wraps(fn)
        def before(other, *args, **kwargs):
            before_result = yield self.before(other, args, kwargs)
            if isinstance(before_result, (ReturnInformationT, Model)):
                raise Return(before_result)
            result = yield fn(other, *args, **kwargs)
            after_result = yield self.after(other, args, kwargs, result)
            if isinstance(after_result, (ReturnInformationT, Model)):
                raise Return(after_result)
            raise Return(result)

        return before

    @abstractmethod
    def before(self, handler, args, kwargs):
        """Method executed before the underlying request handler is called."""
        pass

    @abstractmethod
    def after(self, handler, args, kwargs, result):
        """Method executed after the unterlying request handler ist called."""
        pass