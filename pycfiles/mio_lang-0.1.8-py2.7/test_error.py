# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/core/test_error.py
# Compiled at: 2013-12-08 17:19:04


def test_error(mio):
    mio.eval('e = Error clone("Foo", "FooBar!")')
    assert mio.eval('e type') == 'Foo'
    assert mio.eval('e message') == 'FooBar!'


def test_call(mio):
    mio.eval('e = Error("FooBar!")')
    assert mio.eval('e message == "FooBar!"')


def test_repr(mio):
    e = mio.eval('Error clone("Foo", "FooBar!")')
    assert repr(e) == 'Foo(FooBar!)'


def test_exception(mio):
    mio.eval('e = Exception try(a + b)')
    assert mio.eval('e type') == 'AttributeError'
    assert mio.eval('e message') == "Object has no attribute 'a'"