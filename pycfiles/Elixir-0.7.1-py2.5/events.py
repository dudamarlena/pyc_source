# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/elixir/events.py
# Compiled at: 2009-11-13 14:51:36
__all__ = ['before_insert',
 'after_insert',
 'before_update',
 'after_update',
 'before_delete',
 'after_delete',
 'reconstructor']

def create_decorator(event_name):

    def decorator(func):
        if not hasattr(func, '_elixir_events'):
            func._elixir_events = []
        func._elixir_events.append(event_name)
        return func

    return decorator


before_insert = create_decorator('before_insert')
after_insert = create_decorator('after_insert')
before_update = create_decorator('before_update')
after_update = create_decorator('after_update')
before_delete = create_decorator('before_delete')
after_delete = create_decorator('after_delete')
try:
    from sqlalchemy.orm import reconstructor
except ImportError:

    def reconstructor(func):
        raise Exception('The reconstructor method decorator is only available with SQLAlchemy 0.5 and later')