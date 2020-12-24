# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Edd\Workspace\python\ethronsoft\gcspypi\test\console_test.py
# Compiled at: 2018-07-15 07:17:56
# Size of source mod 2**32: 5859 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.exceptions import *
import sys, six, pytest
if six.PY2:
    from StringIO import StringIO
else:
    from io import StringIO

def test_no_exception():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        with Console() as (c):
            c.info('hello')
            c.error('wrong')
            c.warning('careful')
            c.badge('hello', 'success')
            c.badge('hello', 'warning')
            c.badge('hello', 'danger')
        out.seek(0)
        err.seek(0)
        @py_assert2 = out.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 0
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        @py_assert2 = err.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 6
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    finally:
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr


def test_dynamic():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        with Console() as (c):
            pending = c.info('hello', '\r')
            c.blank(pending)
            c.info('world')
        out.seek(0)
        err.seek(0)
        @py_assert2 = out.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 0
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        @py_assert2 = err.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 1
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    finally:
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr


def test_output():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    curr_stdin = sys.stdin
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        with Console() as (c):
            c.output('hello')
        out.seek(0)
        err.seek(0)
        @py_assert2 = out.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 1
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        @py_assert2 = err.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 0
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    finally:
        sys.stdin = curr_stdin
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr


def test_input_with_response():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    curr_stdin = sys.stdin
    try:
        out = StringIO()
        err = StringIO()
        cin = StringIO('hello\n')
        sys.stdout = out
        sys.stderr = err
        sys.stdin = cin
        with Console() as (c):
            @py_assert1 = c.input
            @py_assert3 = 'do this'
            @py_assert5 = 'default'
            @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
            @py_assert10 = 'hello'
            @py_assert9 = @py_assert7 == @py_assert10
            if not @py_assert9:
                @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.input\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
                @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
                raise AssertionError(@pytest_ar._format_explanation(@py_format14))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
        out.seek(0)
        err.seek(0)
        @py_assert2 = out.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 0
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        @py_assert2 = err.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 1
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    finally:
        sys.stdin = curr_stdin
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr


def test_input_without_response():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    curr_stdin = sys.stdin
    try:
        out = StringIO()
        err = StringIO()
        cin = StringIO('\n')
        sys.stdout = out
        sys.stderr = err
        sys.stdin = cin
        with Console() as (c):
            @py_assert1 = c.input
            @py_assert3 = 'do this'
            @py_assert5 = 'default'
            @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
            @py_assert10 = 'default'
            @py_assert9 = @py_assert7 == @py_assert10
            if not @py_assert9:
                @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.input\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
                @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
                raise AssertionError(@pytest_ar._format_explanation(@py_format14))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
        out.seek(0)
        err.seek(0)
        @py_assert2 = out.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 0
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        @py_assert2 = err.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 1
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    finally:
        sys.stdin = curr_stdin
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr


def test_selection():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    curr_stdin = sys.stdin
    try:
        out = StringIO()
        err = StringIO()
        cin = StringIO('y\n')
        sys.stdout = out
        sys.stderr = err
        sys.stdin = cin
        with Console() as (c):
            @py_assert1 = c.selection
            @py_assert3 = 'do this'
            @py_assert5 = [
             'y', 'n']
            @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
            @py_assert10 = 'y'
            @py_assert9 = @py_assert7 == @py_assert10
            if not @py_assert9:
                @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.selection\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
                @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
                raise AssertionError(@pytest_ar._format_explanation(@py_format14))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
        out.seek(0)
        err.seek(0)
        @py_assert2 = out.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 0
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        @py_assert2 = err.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 1
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    finally:
        sys.stdin = curr_stdin
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr


def test_exception():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        try:
            with Console(exit_on_error=False) as (c):
                c.info('hello')
                raise Exception('urgh')
        except:
            pass

        out.seek(0)
        err.seek(0)
        @py_assert2 = out.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 0
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        @py_assert2 = err.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 2
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    finally:
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr


def test_exception_verbose():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        try:
            with Console(exit_on_error=False, verbose=True) as (c):
                c.info('hello')
                raise Exception('urgh')
        except:
            pass

        out.seek(0)
        err.seek(0)
        @py_assert2 = out.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 0
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        @py_assert2 = err.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 1
        @py_assert8 = @py_assert6 > @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('>', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} > %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    finally:
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr


def test_custom_exceptions():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        excs = [NotFound, InvalidParameter, InvalidState, RepositoryError, ScriptError]
        for Exc in excs:
            try:
                with Console(exit_on_error=False):
                    raise Exc('urgh')
            except:
                pass

        out.seek(0)
        err.seek(0)
        @py_assert2 = out.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 0
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        @py_assert2 = err.readlines
        @py_assert4 = @py_assert2()
        @py_assert6 = len(@py_assert4)
        @py_assert11 = len(excs)
        @py_assert8 = @py_assert6 == @py_assert11
        if not @py_assert8:
            @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.readlines\n}()\n})\n} == %(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}', ), (@py_assert6, @py_assert11)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py10':@pytest_ar._saferepr(excs) if 'excs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excs) else 'excs',  'py12':@pytest_ar._saferepr(@py_assert11)}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = None
    finally:
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr