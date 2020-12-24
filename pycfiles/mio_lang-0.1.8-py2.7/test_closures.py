# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_closures.py
# Compiled at: 2013-11-13 10:21:41
from pytest import fixture
from mio import runtime

@fixture(scope='session')
def mio(request):
    runtime.init()
    return runtime.state


def test_closure(mio, capfd):
    mio.eval('\n        foo = block(\n            block(\n                print("foo")\n            )\n        )\n    ')
    mio.eval('x = foo()')
    assert mio.frommio(mio.eval('x()')) is None
    out, err = capfd.readouterr()
    assert out == 'foo\n'
    return


def test_closure_locals(mio):
    mio.eval('\n        counter = block(n,\n            block(\n                this n = n + 1\n                n\n            )\n        )\n    ')
    mio.eval('x = counter(1)')
    mio.eval('y = counter(2)')
    assert mio.eval('x()') == 2
    assert mio.eval('y()') == 3
    assert mio.eval('x()') == 3
    assert mio.eval('y()') == 4


def test_closure_locals2(mio):
    mio.eval('\n        counter = block(n,\n            block(\n                n = n + 1\n                n\n            )\n        )\n    ')
    mio.eval('x = counter(1)')
    assert mio.eval('x()') == 2
    assert mio.eval('x()') == 2