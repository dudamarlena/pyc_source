# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/wheel/symengine/tests/test_printing.py
# Compiled at: 2020-03-16 01:41:57
from symengine import ccode, Symbol, sqrt, Pow, Max, sin, Integer, MutableDenseMatrix
from symengine.utilities import raises
from symengine.printing import CCodePrinter

def test_ccode():
    x = Symbol('x')
    y = Symbol('y')
    assert ccode(x) == 'x'
    assert ccode(x ** 3) == 'pow(x, 3)'
    assert ccode(x ** (y ** 3)) == 'pow(x, pow(y, 3))'
    assert ccode(x ** (-1.0)) == 'pow(x, -1.0)'
    assert ccode(Max(x, x * x)) == 'fmax(x, pow(x, 2))'
    assert ccode(sin(x)) == 'sin(x)'
    assert ccode(Integer(67)) == '67'
    assert ccode(Integer(-1)) == '-1'


def test_CCodePrinter():
    x = Symbol('x')
    y = Symbol('y')
    myprinter = CCodePrinter()
    assert myprinter.doprint(1 + x, 'bork') == 'bork = 1 + x;'
    assert myprinter.doprint(1 * x) == 'x'
    assert myprinter.doprint(MutableDenseMatrix(1, 2, [x, y]), 'larry') == 'larry[0] = x;\nlarry[1] = y;'
    raises(TypeError, lambda : myprinter.doprint(sin(x), Integer))
    raises(RuntimeError, lambda : myprinter.doprint(MutableDenseMatrix(1, 2, [x, y])))