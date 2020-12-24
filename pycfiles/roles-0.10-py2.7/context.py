# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/roles/context.py
# Compiled at: 2012-05-14 16:21:56
"""
Context.
"""
from __future__ import absolute_import
from functools import wraps
import threading
__all__ = [
 'context', 'in_context']

class ManagedContext(object):

    def __init__(self, stack, ctx, bindings):
        self.stack = stack
        self.ctx = ctx
        self.bindings = bindings

    def __enter__(self):
        """
        Activate the context, bind roles to instances defined in the context.
        """
        ctx = self.ctx
        self.stack.append(self.ctx)
        for var, role in self.bindings.iteritems():
            role.assign(getattr(ctx, var))

        return ctx

    def __exit__(self, exc_type, exc_value, traceback):
        ctx = self.stack.pop()
        assert ctx is self.ctx
        for var, role in self.bindings.iteritems():
            role.revoke(getattr(ctx, var))


class CurrentContextManager(threading.local):

    def __init__(self):
        self.__dict__['__stack'] = []

    def __call__--- This code section failed: ---

 L.  45         0  LOAD_FAST             1  'ctxobj'
                3  POP_JUMP_IF_TRUE     15  'to 15'
                6  LOAD_ASSERT              AssertionError
                9  LOAD_CONST               'Should provide a context object'
               12  RAISE_VARARGS_2       2  None

 L.  46        15  LOAD_GLOBAL           1  'ManagedContext'
               18  LOAD_FAST             0  'self'
               21  LOAD_ATTR             2  '__dict__'
               24  LOAD_CONST               '__stack'
               27  BINARY_SUBSCR    
               28  LOAD_FAST             1  'ctxobj'
               31  LOAD_FAST             2  'bindings'
               34  CALL_FUNCTION_3       3  None
               37  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 37

    @property
    def current_context(self):
        return self.__dict__['__stack'][(-1)]

    def __getattr__(self, key):
        return getattr(self.current_context, key)

    def __setattr__(self, key, val):
        return setattr(self.current_context, key, val)


context = CurrentContextManager()
context.__dict__['__doc__'] = '\nThe default application wide context stack.\n\nPut a new context class on the context stack. This functionality should\nbe called with the context class as first argument.\n\n>>> class SomeContext(object):\n...     pass # define some methods, define some roles\n...     def execute(self):\n...         with context(self):\n...             pass # do something\n\nRoles can be fetched from the context by calling ``context.name``.\nJust like that.\n\nYou can provide additional bindings to be performed:\n\n>>> from role import RoleType\n\n>>> class SomeRole(object):\n...     __metaclass__ = RoleType\n\n>>> class SomeContext(object):\n...     def __init__(self, data_object):\n...         self.data_object = data_object\n...     def execute(self):\n...         with context(self, data_object=SomeRole):\n...             pass # do something\n\nThose bindings are applied when the context is entered (in this case immediately).\n'

def in_context(func):
    """
    Decorator for running methods in context. The context is the object (self).
    """

    @wraps(func)
    def in_context_wrapper(self, *args, **kwargs):
        with context(self):
            return func(self, *args, **kwargs)

    return in_context_wrapper