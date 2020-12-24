# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/test_utils.py
# Compiled at: 2013-12-08 17:19:04
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys
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
    @py_assert2 = format_object(foo)
    @py_assert6 = FOO_TEMPLATE.format
    @py_assert11 = id(foo)
    @py_assert13 = hex(@py_assert11)
    @py_assert15 = @py_assert6(@py_assert13)
    @py_assert4 = @py_assert2 == @py_assert15
    if not @py_assert4:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py16)s\n{%(py16)s = %(py7)s\n{%(py7)s = %(py5)s.format\n}(%(py14)s\n{%(py14)s = %(py8)s(%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n})\n})\n}',), (@py_assert2, @py_assert15)) % {'py8': @pytest_ar._saferepr(hex) if 'hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex) else 'hex', 'py9': @pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id', 'py0': @pytest_ar._saferepr(format_object) if 'format_object' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_object) else 'format_object', 'py1': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py10': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py3': @pytest_ar._saferepr(@py_assert2), 'py16': @pytest_ar._saferepr(@py_assert15), 'py5': @pytest_ar._saferepr(FOO_TEMPLATE) if 'FOO_TEMPLATE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FOO_TEMPLATE) else 'FOO_TEMPLATE', 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert11 = @py_assert13 = @py_assert15 = None
    return


def test_format_method(mio):
    foo = Foo()
    @py_assert2 = foo.noargs
    @py_assert4 = format_method(@py_assert2)
    @py_assert7 = 'noargs()'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.noargs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(format_method) if 'format_method' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_method) else 'format_method', 'py1': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = foo.args
    @py_assert4 = format_method(@py_assert2)
    @py_assert7 = 'args(a, b, c)'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.args\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(format_method) if 'format_method' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_method) else 'format_method', 'py1': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = foo.varargs
    @py_assert4 = format_method(@py_assert2)
    @py_assert7 = 'varargs(*args)'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.varargs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(format_method) if 'format_method' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_method) else 'format_method', 'py1': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    return


def test_format_function(mio):
    @py_assert2 = format_function(foo)
    @py_assert5 = 'foo()'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(format_function) if 'format_function' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_function) else 'format_function', 'py1': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = format_function(bar)
    @py_assert5 = 'Return "Bar"'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(format_function) if 'format_function' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_function) else 'format_function', 'py1': @pytest_ar._saferepr(bar) if 'bar' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bar) else 'bar', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_format_value():
    obj = Foo()
    @py_assert2 = obj.noargs
    @py_assert4 = format_value(@py_assert2)
    @py_assert7 = 'noargs()'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.noargs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(format_value) if 'format_value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_value) else 'format_value', 'py1': @pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = obj.args
    @py_assert4 = format_value(@py_assert2)
    @py_assert7 = 'args(a, b, c)'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.args\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(format_value) if 'format_value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_value) else 'format_value', 'py1': @pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = obj.varargs
    @py_assert4 = format_value(@py_assert2)
    @py_assert7 = 'varargs(*args)'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.varargs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(format_value) if 'format_value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_value) else 'format_value', 'py1': @pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    return


def test_format_value2():
    @py_assert2 = format_value(foo)
    @py_assert5 = 'foo()'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(format_value) if 'format_value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_value) else 'format_value', 'py1': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = format_value(bar)
    @py_assert5 = 'Return "Bar"'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(format_value) if 'format_value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_value) else 'format_value', 'py1': @pytest_ar._saferepr(bar) if 'bar' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bar) else 'bar', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_format_value3():
    @py_assert1 = 1
    @py_assert3 = format_value(@py_assert1)
    @py_assert6 = '1'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(format_value) if 'format_value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_value) else 'format_value', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_format_result():
    obj = Foo()
    @py_assert2 = obj.noargs
    @py_assert4 = format_result(@py_assert2)
    @py_assert7 = 'noargs()'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.noargs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(format_result) if 'format_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_result) else 'format_result', 'py1': @pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = obj.args
    @py_assert4 = format_result(@py_assert2)
    @py_assert7 = 'args(a, b, c)'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.args\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(format_result) if 'format_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_result) else 'format_result', 'py1': @pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = obj.varargs
    @py_assert4 = format_result(@py_assert2)
    @py_assert7 = 'varargs(*args)'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.varargs\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(format_result) if 'format_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_result) else 'format_result', 'py1': @pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    return


def test_format_result2():
    @py_assert2 = format_result(foo)
    @py_assert5 = 'foo()'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(format_result) if 'format_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_result) else 'format_result', 'py1': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = format_result(bar)
    @py_assert5 = 'Return "Bar"'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(format_result) if 'format_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_result) else 'format_result', 'py1': @pytest_ar._saferepr(bar) if 'bar' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bar) else 'bar', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_format_result3():
    @py_assert1 = 1
    @py_assert3 = format_result(@py_assert1)
    @py_assert6 = '1'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(format_result) if 'format_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_result) else 'format_result', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_format_result4(mio):
    @py_assert2 = mio.eval
    @py_assert4 = 'None'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = format_result(@py_assert6)
    @py_assert10 = @py_assert8 is None
    if not @py_assert10:
        @py_format12 = @pytest_ar._call_reprcompare(('is',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} is %(py11)s',), (@py_assert8, None)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None', 'py0': @pytest_ar._saferepr(format_result) if 'format_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_result) else 'format_result', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    return


def test_format_result5(mio):
    mio.eval('\n        Foo = Object clone() do(\n            __repr__ = method("Foo")\n        )\n    ')
    @py_assert2 = mio.eval
    @py_assert4 = 'Foo'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = format_result(@py_assert6)
    @py_assert11 = 'Foo'
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(format_result) if 'format_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_result) else 'format_result', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    return


def test_format_result6(mio):
    Foo = mio.eval('Foo = Object clone()')
    @py_assert2 = mio.eval
    @py_assert4 = 'Foo'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = format_result(@py_assert6)
    @py_assert11 = 'Foo(Object) at {0:s}'
    @py_assert13 = @py_assert11.format
    @py_assert18 = id(Foo)
    @py_assert20 = hex(@py_assert18)
    @py_assert22 = @py_assert13(@py_assert20)
    @py_assert10 = @py_assert8 == @py_assert22
    if not @py_assert10:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} == %(py23)s\n{%(py23)s = %(py14)s\n{%(py14)s = %(py12)s.format\n}(%(py21)s\n{%(py21)s = %(py15)s(%(py19)s\n{%(py19)s = %(py16)s(%(py17)s)\n})\n})\n}',), (@py_assert8, @py_assert22)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py19': @pytest_ar._saferepr(@py_assert18), 'py23': @pytest_ar._saferepr(@py_assert22), 'py0': @pytest_ar._saferepr(format_result) if 'format_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(format_result) else 'format_result', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py3': @pytest_ar._saferepr(@py_assert2), 'py16': @pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11), 'py17': @pytest_ar._saferepr(Foo) if 'Foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Foo) else 'Foo', 'py15': @pytest_ar._saferepr(hex) if 'hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex) else 'hex', 'py21': @pytest_ar._saferepr(@py_assert20)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert18 = @py_assert20 = @py_assert22 = None
    return


def test_default_repr(mio):
    Foo = mio.eval('Foo = Object clone()')
    @py_assert2 = mio.eval
    @py_assert4 = 'Foo'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = default_repr(@py_assert6)
    @py_assert11 = 'Foo(Object) at {0:s}'
    @py_assert13 = @py_assert11.format
    @py_assert18 = id(Foo)
    @py_assert20 = hex(@py_assert18)
    @py_assert22 = @py_assert13(@py_assert20)
    @py_assert10 = @py_assert8 == @py_assert22
    if not @py_assert10:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} == %(py23)s\n{%(py23)s = %(py14)s\n{%(py14)s = %(py12)s.format\n}(%(py21)s\n{%(py21)s = %(py15)s(%(py19)s\n{%(py19)s = %(py16)s(%(py17)s)\n})\n})\n}',), (@py_assert8, @py_assert22)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py19': @pytest_ar._saferepr(@py_assert18), 'py23': @pytest_ar._saferepr(@py_assert22), 'py0': @pytest_ar._saferepr(default_repr) if 'default_repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_repr) else 'default_repr', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py3': @pytest_ar._saferepr(@py_assert2), 'py16': @pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11), 'py17': @pytest_ar._saferepr(Foo) if 'Foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Foo) else 'Foo', 'py15': @pytest_ar._saferepr(hex) if 'hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex) else 'hex', 'py21': @pytest_ar._saferepr(@py_assert20)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert18 = @py_assert20 = @py_assert22 = None
    return


def test_tryimport(mio):
    m = tryimport('sys')
    @py_assert1 = m is sys
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (m, sys)) % {'py0': @pytest_ar._saferepr(m) if 'm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(m) else 'm', 'py2': @pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def test_tryimport_fail(mio):
    try:
        tryimport('foo', 'foo')
    except Warning as w:
        @py_assert0 = w[0]
        @py_assert3 = 'foo'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    return


def test_null(mio):
    @py_assert1 = Null is Null
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (Null, Null)) % {'py0': @pytest_ar._saferepr(Null) if 'Null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Null) else 'Null', 'py2': @pytest_ar._saferepr(Null) if 'Null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Null) else 'Null'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = Null()
    @py_assert3 = @py_assert1 is Null
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} is %(py4)s', ), (@py_assert1, Null)) % {'py0': @pytest_ar._saferepr(Null) if 'Null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Null) else 'Null', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(Null) if 'Null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Null) else 'Null'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    return