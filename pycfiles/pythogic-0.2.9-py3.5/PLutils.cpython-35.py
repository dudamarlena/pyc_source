# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pythogic/pl/PLutils.py
# Compiled at: 2018-03-14 06:21:22
# Size of source mod 2**32: 759 bytes
from pythogic.base.Formula import Formula, Equivalence, And, Not, DUMMY_ATOMIC, Or, Implies

def _or_to_and(f: Or) -> Formula:
    return Not(And(Not(f.f1), Not(f.f2)))


def _implies_to_or(f: Implies) -> Formula:
    equivalent_formula = Or(Not(f.f1), f.f2)
    return _or_to_and(equivalent_formula)


def _equivalence_to_equivalent_formula(f: Equivalence) -> Formula:
    positive_equivalence = And(f.f1, f.f2)
    negative_equivalence = And(Not(f.f1), Not(f.f2))
    return Not(And(Not(positive_equivalence), Not(negative_equivalence)))


def _trueFormula_to_equivalent_formula(*args) -> Formula:
    return Not(_falseFormula_to_equivalent_formula())


def _falseFormula_to_equivalent_formula(*args) -> Formula:
    return And(DUMMY_ATOMIC, Not(DUMMY_ATOMIC))