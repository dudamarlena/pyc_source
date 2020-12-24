# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/test_main.py
# Compiled at: 2013-12-08 17:19:04
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys
from subprocess import Popen, PIPE
from mio.main import USAGE, VERSION
import main_wrapper
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.mio')

def test_help():
    p = Popen([sys.executable, main_wrapper.__file__, '--help'], stdout=PIPE)
    stdout = p.communicate()[0].strip()
    @py_assert1 = stdout == USAGE
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (stdout, USAGE)) % {'py0': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py2': @pytest_ar._saferepr(USAGE) if 'USAGE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(USAGE) else 'USAGE'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def test_version():
    p = Popen([sys.executable, main_wrapper.__file__, '--version'], stdout=PIPE)
    stdout = p.communicate()[0].strip()
    @py_assert1 = stdout == VERSION
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (stdout, VERSION)) % {'py0': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py2': @pytest_ar._saferepr(VERSION) if 'VERSION' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(VERSION) else 'VERSION'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def test_eval():
    p = Popen([sys.executable, main_wrapper.__file__, '-e', 'print(1 + 2)'], stdout=PIPE)
    stdout = p.communicate()[0]
    @py_assert2 = '3\n'
    @py_assert1 = stdout == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (stdout, @py_assert2)) % {'py0': @pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_inspect():
    p = Popen([sys.executable, main_wrapper.__file__, '-i', TEST_FILE], stdin=PIPE, stdout=PIPE)
    stdout = p.communicate('exit()\n')[0]
    @py_assert0 = stdout.split()[0]
    @py_assert3 = '3'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_repl():
    p = Popen([sys.executable, main_wrapper.__file__], stdin=PIPE, stdout=PIPE)
    stdout = p.communicate('print(1 + 2)\nexit()\n')[0]
    @py_assert0 = stdout.split()[3]
    @py_assert3 = '3'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_repl_cont():
    p = Popen([sys.executable, main_wrapper.__file__], stdin=PIPE, stdout=PIPE)
    stdout = p.communicate('foo = block(\n    print("Hello World!")\n)')[0]
    lines = stdout.split()[3:]
    @py_assert0 = lines[0]
    @py_assert3 = '....'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = lines[1]
    @py_assert3 = '....'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return