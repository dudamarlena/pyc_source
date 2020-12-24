# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pythogic/fol/semantics/Relation.py
# Compiled at: 2018-02-25 16:32:30
# Size of source mod 2**32: 963 bytes
from typing import Set, Tuple
from pythogic.base.Symbol import PredicateSymbol

class Relation(object):

    def __init__(self, predicate_symbol: PredicateSymbol, tuples: Set[Tuple]):
        assert all(type(t) == tuple and len(t) == predicate_symbol.arity for t in tuples)
        self.predicate_symbol = predicate_symbol
        self.tuples = tuples

    def __str__(self):
        return str(self.predicate_symbol) + ' ' + str(self.tuples)

    def __repr__(self):
        return str(self.predicate_symbol)

    def _members(self):
        return (
         
          self.predicate_symbol, *self.tuples)

    def __eq__(self, other):
        if type(other) is type(self):
            return self._members() == other._members()
        else:
            return False

    def __hash__(self):
        return hash(self._members())