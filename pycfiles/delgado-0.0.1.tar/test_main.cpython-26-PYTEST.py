# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alfredo/python/delgado/delgado/tests/test_main.py
# Compiled at: 2013-03-11 23:29:08
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import raises
from delgado import main

class TestMain(object):

    def test_get_help_with_no_args(self, capsys):
        with raises(SystemExit):
            main.Delgado([])
        (out, err) = capsys.readouterr()
        @py_assert2 = ''
        @py_assert1 = err == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() is not @py_builtins.globals() else 'err', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        @py_assert0 = 'Version:'
        @py_assert2 = @py_assert0 in out
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, out)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() is not @py_builtins.globals() else 'out'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        return

    def test_load_pytest(self, capsys):
        main.Delgado(['delgado', '--log', 'debug'])
        (out, err) = capsys.readouterr()
        @py_assert2 = ''
        @py_assert1 = err == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() is not @py_builtins.globals() else 'err', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        @py_assert0 = 'loading pytest'
        @py_assert2 = @py_assert0 in out
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, out)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() is not @py_builtins.globals() else 'out'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        return

    def test_info_logger_doesnt_show_plugin_loading(self, capsys):
        main.Delgado(['delgado', '--logging', 'info'])
        (out, err) = capsys.readouterr()
        @py_assert0 = 'loading pytest'
        @py_assert2 = @py_assert0 not in out
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, out)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() is not @py_builtins.globals() else 'out'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        return

    def test_unkown_command(self, capsys):
        main.Delgado(['delgado', '--foo', 'info'])
        (out, err) = capsys.readouterr()
        @py_assert0 = 'Unknown command'
        @py_assert2 = @py_assert0 in out
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, out)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() is not @py_builtins.globals() else 'out'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        return