# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/llb3d/context.py
# Compiled at: 2019-01-14 11:29:04
# Size of source mod 2**32: 1923 bytes
"""Context for llb3d compiler.

Global and local Blitz objects.
"""
import threading

class Context:
    __doc__ = 'Context for global and local objects.'

    def __init__(self):
        """See help(type(obj))."""
        self.functions = {}
        self.globals = {}


_CURRENT_CONTEXT = threading.local()

class ContextProvider:
    __doc__ = 'Context provider.\n\n    Should use with current_context proxy:\n\n    >>> outer_context = Context()\n    >>> with ContextProvider(outer_context):\n    ...     with current_context() as inner_context:\n    ...         assert inner_context is outer_context\n    '

    def __init__(self, context: Context):
        """See help(type(obj))."""
        self.context = context
        self.prev_context = None

    def __enter__(self):
        """See help(type(obj))."""
        self.prev_context = getattr(_CURRENT_CONTEXT, 'context', None)
        _CURRENT_CONTEXT.context = self.context

    def __exit__(self, exception_type, exception_value, traceback):
        """See help(type(obj))."""
        _CURRENT_CONTEXT.context = self.prev_context


class ContextProxy:
    __doc__ = 'Context provider proxy.\n\n    Should use with ContextProvider:\n\n    >>> outer_context = Context()\n    >>> with ContextProvider(outer_context):\n    ...     with current_context() as inner_context:\n    ...         assert inner_context is outer_context\n    '

    def __enter__(self):
        """See help(type(obj))."""
        return getattr(_CURRENT_CONTEXT, 'context', None)

    def __exit__(self, exception_type, exception_value, traceback):
        """See help(type(obj))."""
        pass


def current_context():
    """Get current context manager.

    Should use with ContextProvider:
    >>> outer_context = Context()
    >>> with ContextProvider(outer_context):
    ...     with current_context() as inner_context:
    ...         assert inner_context is outer_context
    """
    return ContextProxy()