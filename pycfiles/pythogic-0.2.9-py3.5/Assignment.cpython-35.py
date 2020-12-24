# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pythogic/fol/semantics/Assignment.py
# Compiled at: 2018-02-25 16:32:30
# Size of source mod 2**32: 875 bytes
from typing import Dict
from pythogic.fol.semantics.Interpretation import Interpretation
from pythogic.fol.syntax.Term import Variable, Term, FunctionTerm

class Assignment(object):

    def __init__(self, variable2object: Dict[(Variable, object)], interpretation: Interpretation):
        self.variable2object = variable2object
        self.interpretation = interpretation

    def __call__(self, term: Term):
        if isinstance(term, Variable):
            assert term in self.variable2object
            return self.variable2object[term]
        if isinstance(term, FunctionTerm):
            assert term.symbol in self.interpretation.alphabet.functions
            args = [self(arg) for arg in term.args]
            return self.interpretation.getFunction(term.symbol)(*args)
        raise ValueError('Term is nor a Variable neither a FunctionTerm')