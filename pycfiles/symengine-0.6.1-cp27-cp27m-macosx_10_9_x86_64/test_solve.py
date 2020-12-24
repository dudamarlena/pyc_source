# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/wheel/symengine/tests/test_solve.py
# Compiled at: 2020-03-16 01:41:57
from symengine.utilities import raises
from symengine import Interval, EmptySet, FiniteSet, I, oo, Eq, Symbol, linsolve
from symengine.lib.symengine_wrapper import solve

def test_solve():
    x = Symbol('x')
    reals = Interval(-oo, oo)
    assert solve(1, x, reals) == EmptySet()
    assert solve(0, x, reals) == reals
    assert solve(x + 3, x, reals) == FiniteSet(-3)
    assert solve(x + 3, x, Interval(0, oo)) == EmptySet()
    assert solve(x, x, reals) == FiniteSet(0)
    assert solve(x ** 2 + 1, x) == FiniteSet(-I, I)
    assert solve(x ** 2 - 2 * x + 1, x) == FiniteSet(1)
    assert solve(Eq(x ** 3 + 3 * x ** 2 + 3 * x, -1), x, reals) == FiniteSet(-1)
    assert solve(x ** 3 - x, x) == FiniteSet(0, 1, -1)


def test_linsolve():
    x = Symbol('x')
    y = Symbol('y')
    assert linsolve([x - 2], [x]) == (2, )
    assert linsolve([x - 2, y - 3], [x, y]) == (2, 3)
    assert linsolve([x + y - 3, x + 2 * y - 4], [x, y]) == (2, 1)