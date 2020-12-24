# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alfredo/python/delgado/delgado/tests/test_loader.py
# Compiled at: 2013-03-16 17:11:47
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import raises
from delgado import loader
from delgado.exceptions import InvalidFormat, Forbidden

class TestFormatCommand(object):

    def test_get_executable_first(self):
        obj = {'executable': [1, 2, 3]}
        result = loader.format_command(obj)
        @py_assert2 = ['executable', 1, 2, 3]
        @py_assert1 = result == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() is not @py_builtins.globals() else 'result', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        return

    def test_no_arguments_are_ok(self):
        obj = {'executable': []}
        result = loader.format_command(obj)
        @py_assert2 = ['executable']
        @py_assert1 = result == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() is not @py_builtins.globals() else 'result', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        return

    def test_raise_invalid_format(self):
        with raises(InvalidFormat):
            loader.format_command([])

    def test_get_correct_rpr(self):
        with raises(InvalidFormat) as (exc):
            loader.format_command([])
        error = exc.value.args[0]
        @py_assert0 = 'received: []'
        @py_assert2 = @py_assert0 in error
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, error)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() is not @py_builtins.globals() else 'error'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        return

    def test_no_obj(self):
        with raises(InvalidFormat):
            loader.format_command({})


class TestLoader(object):

    def test_loader_simplest_obj(self):
        result = loader.loader('{"foo": []}', allowed=['foo'])
        @py_assert2 = ['foo']
        @py_assert1 = result == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() is not @py_builtins.globals() else 'result', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        return

    def test_loader_not_allowed(self):
        with raises(Forbidden):
            loader.loader('{"foo": []}')

    def test_unable_to_parse(self):
        with raises(InvalidFormat):
            loader.loader('foo": []}', allowed=['foo'])