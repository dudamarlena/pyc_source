# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_expressions.py
# Compiled at: 2013-12-08 17:19:04


def test_empty(mio):
    assert mio.frommio(mio.eval('()')) is None
    return


def test_simple(mio):
    assert mio.eval('1 + 2') == 3


def test_complex(mio):
    assert mio.eval('1 + 2 * 3') == 9


def test_grouping(mio):
    assert mio.eval('1 + (2 * 3)') == 7


def test_assignment(mio):
    mio.eval('x = 1')
    assert mio.eval('x') == 1


def test_complex_assignment_expression(mio):
    mio.eval('x = 1')
    assert mio.eval('x') == 1
    mio.eval('x = x + 1')
    assert mio.eval('x') == 2


def test_complex_assignment_attribute(mio):
    mio.eval('Foo = Object clone()')
    mio.eval('Foo x = 1')
    assert mio.eval('Foo x') == 1
    mio.eval('Foo x = Foo x + 1')
    assert mio.eval('Foo x') == 2