# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_decorators.py
# Compiled at: 2017-05-16 09:59:43
# Size of source mod 2**32: 2601 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from funcy.decorators import *

def test_decorator_no_args():

    @decorator
    def inc(call):
        return call() + 1

    @inc
    def ten():
        return 10

    @py_assert1 = ten()
    @py_assert4 = 11
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(ten) if 'ten' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ten) else 'ten'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_decorator_with_args():

    @decorator
    def add(call, n):
        return call() + n

    @add(2)
    def ten():
        return 10

    @py_assert1 = ten()
    @py_assert4 = 12
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(ten) if 'ten' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ten) else 'ten'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_decorator_access_arg():

    @decorator
    def multiply(call):
        return call() * call.n

    @multiply
    def square(n):
        return n

    @py_assert1 = 5
    @py_assert3 = square(@py_assert1)
    @py_assert6 = 25
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(square) if 'square' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(square) else 'square'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_decorator_access_nonexistent_arg():

    @decorator
    def return_x(call):
        return call.x

    @return_x
    def f():
        pass

    with pytest.raises(AttributeError):
        f()


def test_decorator_required_arg():

    @decorator
    def deco(call):
        call.x

    @deco
    def f(x, y=42):
        pass

    with pytest.raises(AttributeError):
        f()


def test_double_decorator_defaults():

    @decorator
    def deco(call):
        return call.y

    @decorator
    def noop(call):
        return call()

    @deco
    @noop
    def f(x, y=1):
        pass

    @py_assert1 = 42
    @py_assert3 = f(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_decorator_defaults():

    @decorator
    def deco(call):
        return (call.y, call.z)

    @deco
    def f(x, y=1, z=2):
        pass

    @py_assert1 = 42
    @py_assert3 = f(@py_assert1)
    @py_assert6 = (1, 2)
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_decorator_with_method():

    @decorator
    def inc(call):
        return call() + 1

    class A(object):

        def ten(self):
            return 10

        @classmethod
        def ten_cls(cls):
            return 10

        @staticmethod
        def ten_static():
            return 10

    @py_assert2 = A()
    @py_assert4 = @py_assert2.ten
    @py_assert6 = inc(@py_assert4)
    @py_assert8 = @py_assert6()
    @py_assert11 = 11
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s()\n}.ten\n})\n}()\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(A) if 'A' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(A) else 'A', 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(@py_assert2), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert2 = A.ten_cls
    @py_assert4 = inc(@py_assert2)
    @py_assert6 = @py_assert4()
    @py_assert9 = 11
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.ten_cls\n})\n}()\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(A) if 'A' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(A) else 'A', 'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = A.ten_static
    @py_assert4 = inc(@py_assert2)
    @py_assert6 = @py_assert4()
    @py_assert9 = 11
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.ten_static\n})\n}()\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(A) if 'A' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(A) else 'A', 'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_decorator_with_method_descriptor():

    @decorator
    def exclaim(call):
        return call() + '!'

    @py_assert2 = str.upper
    @py_assert4 = exclaim(@py_assert2)
    @py_assert6 = 'hi'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert11 = 'HI!'
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.upper\n})\n}(%(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(@py_assert2), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(exclaim) if 'exclaim' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exclaim) else 'exclaim'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_chain_arg_access():

    @decorator
    def decor(call):
        return call.x + call()

    @decor
    @decor
    def func(x):
        return x

    @py_assert1 = 2
    @py_assert3 = func(@py_assert1)
    @py_assert6 = 6
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(func) if 'func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(func) else 'func'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_meta_attribtes():

    @decorator
    def decor(call):
        return call()

    def func(x):
        """Some doc"""
        return x

    decorated = decor(func)
    double_decorated = decor(decorated)
    @py_assert1 = decorated.__name__
    @py_assert4 = 'func'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__name__\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(decorated) if 'decorated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(decorated) else 'decorated'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = decorated.__module__
    @py_assert3 = @py_assert1 == __name__
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__module__\n} == %(py4)s', ), (@py_assert1, __name__)) % {'py4': @pytest_ar._saferepr(__name__) if '__name__' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(__name__) else '__name__', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(decorated) if 'decorated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(decorated) else 'decorated'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = decorated.__doc__
    @py_assert4 = 'Some doc'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__doc__\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(decorated) if 'decorated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(decorated) else 'decorated'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = decorated.__wrapped__
    @py_assert3 = @py_assert1 is func
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__wrapped__\n} is %(py4)s', ), (@py_assert1, func)) % {'py4': @pytest_ar._saferepr(func) if 'func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(func) else 'func', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(decorated) if 'decorated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(decorated) else 'decorated'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = decorated.__original__
    @py_assert3 = @py_assert1 is func
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__original__\n} is %(py4)s', ), (@py_assert1, func)) % {'py4': @pytest_ar._saferepr(func) if 'func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(func) else 'func', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(decorated) if 'decorated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(decorated) else 'decorated'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = double_decorated.__wrapped__
    @py_assert3 = @py_assert1 is decorated
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__wrapped__\n} is %(py4)s', ), (@py_assert1, decorated)) % {'py4': @pytest_ar._saferepr(decorated) if 'decorated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(decorated) else 'decorated', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(double_decorated) if 'double_decorated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(double_decorated) else 'double_decorated'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = double_decorated.__original__
    @py_assert3 = @py_assert1 is func
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__original__\n} is %(py4)s', ), (@py_assert1, func)) % {'py4': @pytest_ar._saferepr(func) if 'func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(func) else 'func', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(double_decorated) if 'double_decorated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(double_decorated) else 'double_decorated'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None