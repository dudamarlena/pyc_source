# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/haoxun/Data/Project/magic_parameter/tests/test_usage.py
# Compiled at: 2016-04-17 07:33:28
# Size of source mod 2**32: 3778 bytes
from __future__ import division, absolute_import, print_function, unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from builtins import *
from future.builtins.disabled import *
import pytest
from magic_parameter import *

def test_function_parameter():

    @function_parameter([
     (
      'a', int),
     (
      'b', float)])
    def example(args):
        @py_assert1 = args.a
        @py_assert4 = 1
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.a\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = args.b
        @py_assert4 = 1.0
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.b\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    example(1, 1.0)
    example(b=1.0, a=1)
    with pytest.raises(AssertionError):
        example(2, 1.0)
    with pytest.raises(TypeError):
        example(1)
    with pytest.raises(TypeError):
        example(1.0)
    with pytest.raises(TypeError):
        example(1, a=1)


def test_method_parameter():

    class Case1(object):

        @classmethod
        @method_parameter([
         (
          'a', int)], pass_by_cls_or_self_attributes=True)
        def test_cls(cls):
            @py_assert1 = cls.a
            @py_assert4 = 1
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.a\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(cls) if 'cls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cls) else 'cls'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None

        @method_parameter([
         (
          'a', int)], pass_by_cls_or_self_attributes=True, no_warning_on_cls_or_self_attributes=False)
        def test_self1(self):
            @py_assert1 = self.a
            @py_assert4 = 1
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.a\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None

        @method_parameter([
         (
          'a', int)], pass_by_function_argument=True)
        def test_self2(self, args):
            @py_assert1 = args.a
            @py_assert4 = 1
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.a\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None

    Case1.test_cls(1)
    Case1.test_cls(a=1)
    with pytest.raises(AssertionError):
        Case1.test_cls(2)
    case1 = Case1()
    case1.test_self1(1)
    case1.test_self2(1)
    with pytest.raises(TypeError):
        case1.test_self1(1)
    case1.test_self2(1)
    with pytest.raises(SyntaxError):

        class Case2(object):

            @classmethod
            @method_parameter([
             (
              'a', int)])
            def test_cls(cls):
                pass

    with pytest.raises(TypeError):
        method_parameter([], pass_by_function_argument=True)(1)


def test_method_init_parameter():

    class Case1(object):

        @method_init_parameter([
         (
          'a', int)])
        def __init__(self):
            @py_assert1 = self.a
            @py_assert4 = 1
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.a\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None

    Case1(1)
    Case1(a=1)
    with pytest.raises(AssertionError):
        Case1(2)
    with pytest.raises(TypeError):
        Case1(b=1)
    with pytest.raises(TypeError):
        Case1(1.0)


def test_class_init_parameter():

    @class_init_parameter
    class Case1(object):
        PARAMETERS = [
         (
          'a', int)]

        def __init__(self):
            @py_assert1 = self.a
            @py_assert4 = 1
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.a\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None

    Case1(1)
    Case1(a=1)
    with pytest.raises(AssertionError):
        Case1(2)

    @class_init_parameter
    class Case2(object):
        PARAMETERS = [
         (
          'a', int)]

    Case2(1)
    Case2(a=1)
    with pytest.raises(SyntaxError):
        class_init_parameter(1)


def test_nested_type():

    @function_parameter([
     (
      'a', list_t(int)),
     (
      'b', list_t(or_t(int, float)), None)])
    def func1(args):
        return (
         args.a, args.b)

    r1, r2 = func1([1, 2])
    @py_assert2 = [1, 2]
    @py_assert1 = r1 == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (r1, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(r1) if 'r1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r1) else 'r1'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = None
    @py_assert1 = r2 is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (r2, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(r2) if 'r2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r2) else 'r2'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = [1, 2]
    if not @py_assert0:
        @py_format2 = (@pytest_ar._format_assertmsg([1, 2.0] == func1([1, 2], [1, 2.0])) + '\n>assert %(py1)s') % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    with pytest.raises(TypeError):
        func1([1.0, 2.0])
    with pytest.raises(TypeError):
        func1(a=[1], b=['test'])

    @function_parameter([
     (
      'a', dict_t(str, int))])
    def func2(args):
        return args.a

    @py_assert0 = {'a': 1, 'b': 2}
    @py_assert4 = {'b': 2, 'a': 1}
    @py_assert6 = func2(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(func2) if 'func2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(func2) else 'func2'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    with pytest.raises(TypeError):
        func2({'a': 1.0})
    with pytest.raises(TypeError):
        func2({1: 1})