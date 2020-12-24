# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pybasic/symbol_table.py
# Compiled at: 2019-04-20 23:19:54
# Size of source mod 2**32: 1256 bytes
import platform, math, os
from .utils import BasicError, Stack

class SymbolTable:

    def __init__(self, parent=None):
        self._table = {}
        self.parent = parent

    def get(self, id):
        id = id.upper()
        if id in self._table:
            return self._table[id]
            if self.parent is None:
                raise BasicError('undefined variable "%s"' % id)
        else:
            return self.parent.get(id)

    def set(self, id, value):
        self._table[id.upper()] = value

    def register(self, id):

        def decorator(func):
            self.set(id, func)
            return func

        return decorator

    def reflect(self, id, func=None):
        if func is not None:
            new_func = lambda n: func(*(x.run() for x in n))
            self.set(id, new_func)
        else:

            def decorator(func):
                new_func = lambda n: func(*(x.run() for x in n))
                self.set(id, new_func)
                return new_func

            return decorator


global_table = SymbolTable()
table_stack = Stack([global_table])
global_table.set('Nothing', None)
global_table.set('True', True)
global_table.set('False', False)
global_table.set('Pi', 3.14159265)