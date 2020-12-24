# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_debug.py
# Compiled at: 2018-10-03 08:49:11
# Size of source mod 2**32: 3781 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, re
from funcy.debug import *
from funcy.flow import silent
from funcy.py3 import lmap

def test_tap():
    @py_assert2 = 42
    @py_assert4 = capture(tap, @py_assert2)
    @py_assert7 = '42\n'
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=9)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(tap) if 'tap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tap) else 'tap', 'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(capture) if 'capture' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(capture) else 'capture', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = 42
    @py_assert4 = 'Life and ...'
    @py_assert6 = capture(tap, @py_assert2, label=@py_assert4)
    @py_assert9 = 'Life and ...: 42\n'
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=10)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py1)s, %(py3)s, label=%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(capture) if 'capture' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(capture) else 'capture', 'py1': @pytest_ar._saferepr(tap) if 'tap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tap) else 'tap', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_log_calls():
    log = []

    @log_calls(log.append)
    def f(x, y):
        return x + y

    f(1, 2)
    f('a', 'b')
    @py_assert2 = ['Call f(1, 2)', '-> 3 from f(1, 2)', "Call f('a', 'b')", "-> 'ab' from f('a', 'b')"]
    @py_assert1 = log == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=22)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (log, @py_assert2)) % {'py0': @pytest_ar._saferepr(log) if 'log' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log) else 'log', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_print_calls():

    def f(x, y):
        return x + y

    (
     capture(print_calls(f), 1, 2) == 'Call f(1, 2)\n-> 3 from f(1, 2)\n',)
    (capture(print_calls()(f), 1, 2) == 'Call f(1, 2)\n-> 3 from f(1, 2)\n',)


def test_log_calls_raise():
    log = []

    @log_calls(log.append, stack=False)
    def f():
        raise Exception('something bad')

    silent(f)()
    @py_assert2 = ['Call f()', '-> Exception: something bad raised in f()']
    @py_assert1 = log == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=45)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (log, @py_assert2)) % {'py0': @pytest_ar._saferepr(log) if 'log' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log) else 'log', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_log_errors():
    log = []

    @log_errors(log.append)
    def f(x):
        return 1 / x

    silent(f)(1)
    silent(f)(0)
    @py_assert2 = len(log)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=60)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(log) if 'log' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log) else 'log', 'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = log[0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'Traceback'
    @py_assert6 = @py_assert2(@py_assert4)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=61)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert1 = re.search
    @py_assert3 = 'ZeroDivisionError: .*\\n    raised in f\\(0\\)$'
    @py_assert5 = log[0]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=62)
    if not @py_assert7:
        @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py6)s)\n}') % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're', 'py8': @pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_log_errors_manager():
    log = []
    try:
        with log_errors(log.append):
            1 / 0
    except ZeroDivisionError:
        pass

    try:
        with log_errors(log.append, 'name check', stack=False):
            hey
    except NameError:
        pass

    @py_assert2 = len(log)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=77)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(log) if 'log' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log) else 'log', 'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    print(log)
    @py_assert0 = log[0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'Traceback'
    @py_assert6 = @py_assert2(@py_assert4)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=79)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert1 = re.search
    @py_assert3 = 'ZeroDivisionError: .* zero\\s*$'
    @py_assert5 = log[0]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=80)
    if not @py_assert7:
        @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py6)s)\n}') % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're', 'py8': @pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert0 = log[1]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'Traceback'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = not @py_assert6
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=81)
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = re.search
    @py_assert3 = "NameError: (global )?name 'hey' is not defined raised in name check"
    @py_assert5 = log[1]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=82)
    if not @py_assert7:
        @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py6)s)\n}') % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're', 'py8': @pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_print_errors():

    def error():
        1 / 0

    f = print_errors(error)
    @py_assert1 = f.__name__
    @py_assert4 = 'error'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=90)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__name__\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = 'ZeroDivisionError'
    @py_assert6 = silent(f)
    @py_assert8 = capture(@py_assert6)
    @py_assert2 = @py_assert0 in @py_assert8
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=91)
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py9)s\n{%(py9)s = %(py3)s(%(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n})\n}', ), (@py_assert0, @py_assert8)) % {'py5': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f', 'py4': @pytest_ar._saferepr(silent) if 'silent' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(silent) else 'silent', 'py1': @pytest_ar._saferepr(@py_assert0), 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(capture) if 'capture' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(capture) else 'capture'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert6 = @py_assert8 = None
    g = print_errors(stack=False)(error)
    @py_assert1 = g.__name__
    @py_assert4 = 'error'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=94)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__name__\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(g) if 'g' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(g) else 'g'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert3 = silent(g)
    @py_assert5 = capture(@py_assert3)
    @py_assert7 = @py_assert5.startswith
    @py_assert9 = 'ZeroDivisionError'
    @py_assert11 = @py_assert7(@py_assert9)
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=95)
    if not @py_assert11:
        @py_format13 = ('' + 'assert %(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n}.startswith\n}(%(py10)s)\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py12': @pytest_ar._saferepr(@py_assert11), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(capture) if 'capture' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(capture) else 'capture', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(silent) if 'silent' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(silent) else 'silent', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(g) if 'g' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(g) else 'g'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_print_errors_manager():

    @silent
    def f():
        with print_errors:
            1 / 0

    @py_assert0 = 'ZeroDivisionError'
    @py_assert5 = capture(f)
    @py_assert2 = @py_assert0 in @py_assert5
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=104)
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f', 'py3': @pytest_ar._saferepr(capture) if 'capture' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(capture) else 'capture'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None
    @py_assert2 = capture(f)
    @py_assert4 = @py_assert2.startswith
    @py_assert6 = 'Traceback'
    @py_assert8 = @py_assert4(@py_assert6)
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=105)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}.startswith\n}(%(py7)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(capture) if 'capture' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(capture) else 'capture', 'py1': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_print_errors_recursion():

    @silent
    @print_errors(stack=False)
    def f(n):
        if n:
            f(0)
            1 / 0

    @py_assert0 = 'f(1)'
    @py_assert5 = 1
    @py_assert7 = capture(f, @py_assert5)
    @py_assert2 = @py_assert0 in @py_assert7
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=116)
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py4)s, %(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(capture) if 'capture' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(capture) else 'capture'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_log_durations(monkeypatch):
    timestamps = iter([0, 0.01, 1, 1.000025])
    monkeypatch.setattr('time.time', lambda : next(timestamps))
    log = []
    f = log_durations(log.append)(lambda : None)
    f()
    with log_durations(log.append, 'hello'):
        pass
    @py_assert1 = '^\\s*(\\d+\\.\\d+ mk?s) in (?:<lambda>\\(\\)|hello)$'
    @py_assert4 = lmap(@py_assert1, log)
    @py_assert7 = [
     '10.00 ms', '25.00 mks']
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=129)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap', 'py3': @pytest_ar._saferepr(log) if 'log' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log) else 'log'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_log_durations_ex(monkeypatch):
    timestamps = [
     0, 0.01, 1, 1.001, 2, 2.02]
    timestamps_iter = iter(timestamps)
    monkeypatch.setattr('time.time', lambda : next(timestamps_iter))
    log = []
    f = log_durations(log.append, unit='ms', threshold=0.0011)(lambda : None)
    f()
    f()
    f()
    @py_assert2 = len(log)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=141)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(log) if 'log' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log) else 'log', 'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = '^\\s*(\\d+\\.\\d+) ms in'
    @py_assert4 = lmap(@py_assert1, log)
    @py_assert7 = [
     '10.00', '20.00']
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=142)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap', 'py3': @pytest_ar._saferepr(log) if 'log' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log) else 'log'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_log_iter_dirations():
    log = []
    for item in log_iter_durations([1, 2], log.append):
        pass

    @py_assert2 = len(log)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_debug.py', lineno=149)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(log) if 'log' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log) else 'log', 'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


import sys
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        return sys.stdout.read()
    finally:
        sys.stdout = out