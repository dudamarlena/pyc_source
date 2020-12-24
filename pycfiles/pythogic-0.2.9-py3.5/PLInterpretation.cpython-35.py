# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pythogic/pl/semantics/PLInterpretation.py
# Compiled at: 2018-03-09 19:49:49
# Size of source mod 2**32: 821 bytes
from typing import Dict
from pythogic.base.Alphabet import Alphabet
from pythogic.base.Symbol import Symbol
from pythogic.base.Formula import AtomicFormula, Formula

class PLInterpretation(object):

    def __init__(self, alphabet: Alphabet, symbol2truth: Dict[(Symbol, bool)]):
        assert alphabet.symbols == symbol2truth.keys() and all(type(v) == bool for v in symbol2truth.values())
        self.alphabet = alphabet
        self.symbol2truth = symbol2truth

    def __eq__(self, other):
        if type(self) == type(other):
            return self.alphabet == other.alphabet and self.symbol2truth == other.symbol2truth
        else:
            return False

    def _members(self):
        return (self.alphabet, tuple(sorted(self.symbol2truth.items())))

    def __hash__(self):
        return hash(self._members())