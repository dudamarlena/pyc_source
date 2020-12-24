# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/wheel/symengine/tests/test_var.py
# Compiled at: 2020-03-16 01:41:57
from symengine import Symbol, var
from symengine.utilities import raises

def _make_z1():
    var('z1')


def __make_z2():
    var('z2')


def _make_z2():
    __make_z2()


def test_var():
    var('a')
    assert a == Symbol('a')
    var('b bb cc zz _x')
    assert b == Symbol('b')
    assert bb == Symbol('bb')
    assert cc == Symbol('cc')
    assert zz == Symbol('zz')
    assert _x == Symbol('_x')
    v = var(['d', 'e', 'fg'])
    assert d == Symbol('d')
    assert e == Symbol('e')
    assert fg == Symbol('fg')
    assert v == [d, e, fg]


def test_var_global_namespace():
    raises(NameError, lambda : z1)
    _make_z1()
    assert z1 == Symbol('z1')
    raises(NameError, lambda : z2)
    _make_z2()
    assert z2 == Symbol('z2')


def test_var_return():
    raises(ValueError, lambda : var(''))
    v2 = var('q')
    v3 = var('q p')
    assert v2 == Symbol('q')
    assert v3 == (Symbol('q'), Symbol('p'))


def test_var_accepts_comma():
    v1 = var('x y z')
    v2 = var('x,y,z')
    v3 = var('x,y z')
    assert v1 == v2
    assert v1 == v3