# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/wheel/symengine/tests/test_subs.py
# Compiled at: 2020-03-16 01:41:57
from symengine.utilities import raises
from symengine import Symbol, sin, cos, sqrt, Add, function_symbol

def test_basic():
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    e = x + y + z
    assert e.subs({x: y, z: y}) == 3 * y


def test_sin():
    x = Symbol('x')
    y = Symbol('y')
    e = sin(x)
    assert e.subs({x: y}) == sin(y)
    assert e.subs({x: y}) != sin(x)
    e = cos(x)
    assert e.subs({x: 0}) == 1
    assert e.subs(x, 0) == 1


def test_args():
    x = Symbol('x')
    e = cos(x)
    raises(TypeError, lambda : e.subs(x, 0, 3))


def test_f():
    x = Symbol('x')
    y = Symbol('y')
    f = function_symbol('f', x)
    g = function_symbol('g', x)
    assert f.subs({function_symbol('f', x): function_symbol('g', x)}) == g
    assert (f + g).subs({function_symbol('f', x): function_symbol('g', x)}) == 2 * g
    e = (f + x) ** 3
    assert e.subs({f: y}) == (x + y) ** 3
    e = e.expand()
    assert e.subs({f: y}) == ((x + y) ** 3).expand()


def test_msubs():
    x = Symbol('x')
    y = Symbol('y')
    f = function_symbol('f', x)
    assert f.msubs({f: y}) == y
    assert f.diff(x).msubs({f: y}) == f.diff(x)


def test_xreplace():
    x = Symbol('x')
    y = Symbol('y')
    f = sin(cos(x))
    assert f.xreplace({x: y}) == sin(cos(y))