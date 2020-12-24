# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/wheel/symengine/tests/test_expr.py
# Compiled at: 2020-03-16 01:41:57
from symengine import Add, Mul, Symbol, Integer
from symengine.utilities import raises

def test_as_coefficients_dict():
    x = Symbol('x')
    y = Symbol('y')
    check = [x, y, x * y, Integer(1)]
    assert [ (3 * x + 2 * x + y + 3).as_coefficients_dict()[i] for i in check ] == [
     5, 1, 0, 3]
    assert [ (3 * x * y).as_coefficients_dict()[i] for i in check ] == [
     0, 0, 3, 0]
    assert (3.0 * x * y).as_coefficients_dict()[(3.0 * x * y)] == 0
    assert (3.0 * x * y).as_coefficients_dict()[(x * y)] == 3.0