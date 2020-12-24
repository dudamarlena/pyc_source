# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pythogic/fol/semantics/Function.py
# Compiled at: 2018-02-25 16:32:30
# Size of source mod 2**32: 1270 bytes
from typing import Tuple, Dict
from pythogic.base.Symbol import FunctionSymbol

class Function(object):

    def __init__(self, function_symbol: FunctionSymbol, function_dictionary: Dict[(Tuple, object)]):
        assert all(type(t) == tuple and len(t) == function_symbol.arity for t in function_dictionary)
        self.function_symbol = function_symbol
        self.function_dictionary = function_dictionary

    def __str__(self):
        return str(self.function_symbol) + ' ' + str(self.function_dictionary)

    def __repr__(self):
        return str(self.function_symbol)

    def _members(self):
        return (
         self.function_symbol, tuple(sorted(self.function_dictionary.items())))

    def __eq__(self, other):
        if type(other) is type(self):
            return self._members() == other._members()
        else:
            return False

    def __hash__(self):
        return hash(self._members())

    def __call__(self, *args):
        assert len(args) == self.function_symbol.arity and args in self.function_dictionary
        return self.function_dictionary[args]