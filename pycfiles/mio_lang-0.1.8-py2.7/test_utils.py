# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_utils.py
# Compiled at: 2013-12-08 17:19:04
import sys
from mio.object import Object
from mio.utils import default_repr, format_function, format_method, format_object, format_result, format_value, method, tryimport, Null

def foo():
    pass


def bar():
    """Return "Bar\""""
    pass


class Foo(Object):

    @method()
    def noargs(self, receiver, context, m):
        pass

    @method()
    def args(self, receiver, context, m, a, b, c):
        pass

    @method()
    def varargs(self, receiver, context, m, *args):
        pass


FOO_TEMPLATE = 'Foo at {0:s}:\n       args            = args(a, b, c)\n       noargs          = noargs()\n       varargs         = varargs(*args)'

def test_format_object(mio):
    foo = Foo()
    assert format_object(foo) == FOO_TEMPLATE.format(hex(id(foo)))


def test_format_method(mio):
    foo = Foo()
    assert format_method(foo.noargs) == 'noargs()'
    assert format_method(foo.args) == 'args(a, b, c)'
    assert format_method(foo.varargs) == 'varargs(*args)'


def test_format_function(mio):
    assert format_function(foo) == 'foo()'
    assert format_function(bar) == 'Return "Bar"'


def test_format_value():
    obj = Foo()
    assert format_value(obj.noargs) == 'noargs()'
    assert format_value(obj.args) == 'args(a, b, c)'
    assert format_value(obj.varargs) == 'varargs(*args)'


def test_format_value2():
    assert format_value(foo) == 'foo()'
    assert format_value(bar) == 'Return "Bar"'


def test_format_value3():
    assert format_value(1) == '1'


def test_format_result():
    obj = Foo()
    assert format_result(obj.noargs) == 'noargs()'
    assert format_result(obj.args) == 'args(a, b, c)'
    assert format_result(obj.varargs) == 'varargs(*args)'


def test_format_result2():
    assert format_result(foo) == 'foo()'
    assert format_result(bar) == 'Return "Bar"'


def test_format_result3():
    assert format_result(1) == '1'


def test_format_result4(mio):
    assert format_result(mio.eval('None')) is None
    return


def test_format_result5(mio):
    mio.eval('\n        Foo = Object clone() do(\n            __repr__ = method("Foo")\n        )\n    ')
    assert format_result(mio.eval('Foo')) == 'Foo'


def test_format_result6(mio):
    Foo = mio.eval('Foo = Object clone()')
    assert format_result(mio.eval('Foo')) == ('Foo(Object) at {0:s}').format(hex(id(Foo)))


def test_default_repr(mio):
    Foo = mio.eval('Foo = Object clone()')
    assert default_repr(mio.eval('Foo')) == ('Foo(Object) at {0:s}').format(hex(id(Foo)))


def test_tryimport(mio):
    m = tryimport('sys')
    assert m is sys


def test_tryimport_fail(mio):
    try:
        tryimport('foo', 'foo')
    except Warning as w:
        assert w[0] == 'foo'


def test_null(mio):
    assert Null is Null
    assert Null() is Null