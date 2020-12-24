# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 27232 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, signal, weakref
from unittest.mock import call, Mock, patch
import pytest, paleomix.atomiccmd.command, paleomix.common.fileutils as fileutils
from paleomix.common.versions import RequirementObj
from paleomix.atomiccmd.command import AtomicCmd, CmdError

def test_file(*args):
    test_root = os.path.dirname(os.path.dirname(__file__))
    return (os.path.join)(test_root, 'data', *args)


def test_atomiccmd__command_str():
    cmd = AtomicCmd('ls')
    @py_assert1 = cmd.executables
    @py_assert5 = [
     'ls']
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=51)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.executables\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_atomiccmd__executables_empty_str():
    with pytest.raises(ValueError, match='Empty command in AtomicCmd constructor'):
        AtomicCmd('')


def test_atomiccmd__command_tuple():
    cmd = AtomicCmd(('cd', '.'))
    @py_assert1 = cmd.executables
    @py_assert5 = [
     'cd']
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=61)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.executables\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_atomiccmd__executables_empty_tuple():
    with pytest.raises(ValueError, match='Empty command in AtomicCmd constructor'):
        AtomicCmd(())


def test_atomiccmd__executables_empty_str_in_tuple():
    with pytest.raises(ValueError, match='Empty command in AtomicCmd constructor'):
        AtomicCmd('')


@pytest.mark.parametrize('set_cwd', (True, False))
def test_atomiccmd__set_cwd(tmp_path, set_cwd):
    cwd = os.getcwd()
    cmd = AtomicCmd(('bash', '-c', 'echo -n ${PWD}'),
      TEMP_OUT_STDOUT='result.txt', set_cwd=set_cwd)
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=86)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert3 = os.getcwd
    @py_assert5 = @py_assert3()
    @py_assert1 = cwd == @py_assert5
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=87)
    if not @py_assert1:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.getcwd\n}()\n}', ), (cwd, @py_assert5)) % {'py0':@pytest_ar._saferepr(cwd) if 'cwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cwd) else 'cwd',  'py2':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    expected = tmp_path if set_cwd else cwd
    result = (tmp_path / 'result.txt').read_text()
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.samefile
    @py_assert7 = @py_assert3(expected, result)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=91)
    if not @py_assert7:
        @py_format9 = (@pytest_ar._format_assertmsg('%r != %r' % (expected, result)) + '\n>assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.samefile\n}(%(py5)s, %(py6)s)\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py6':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert7 = None


@pytest.mark.parametrize('set_cwd', (True, False))
@pytest.mark.parametrize('key', ('TEMP_IN_FOO', 'TEMP_OUT_FOO'))
def test_atomiccmd__set_cwd__temp_in_out(tmp_path, set_cwd, key):
    cmd = AtomicCmd(
 (
  'echo', '-n', '%()s' (key,)), TEMP_OUT_STDOUT='result.txt', 
     set_cwd=set_cwd, **{key: 'test_file'})
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=105)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    expected = os.path.join('' if set_cwd else tmp_path, 'test_file')
    result = (tmp_path / 'result.txt').read_text()
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.abspath
    @py_assert6 = @py_assert3(expected)
    @py_assert10 = os.path
    @py_assert12 = @py_assert10.abspath
    @py_assert15 = @py_assert12(result)
    @py_assert8 = @py_assert6 == @py_assert15
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=109)
    if not @py_assert8:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.abspath\n}(%(py5)s)\n} == %(py16)s\n{%(py16)s = %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s.path\n}.abspath\n}(%(py14)s)\n}', ), (@py_assert6, @py_assert15)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = None


def test_atomiccmd__paths():
    cmd = AtomicCmd('ls',
      IN_AAA='/a/b/c',
      IN_AAB='/x/y/z',
      TEMP_IN_ABB='tmp_in',
      OUT_AAA='/out/foo',
      OUT_BBC='foo/bar',
      TEMP_OUT_A='xyb',
      EXEC_OTHER='true',
      AUX_WAT='wat/wat',
      CHECK_FUNC=bool,
      OUT_STDERR='/var/log/pipe.stderr',
      TEMP_OUT_STDOUT='pipe.stdout')
    @py_assert1 = cmd.executables
    @py_assert5 = [
     'ls', 'true']
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=133)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.executables\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = cmd.requirements
    @py_assert5 = [
     bool]
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=134)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.requirements\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = cmd.input_files
    @py_assert5 = [
     '/a/b/c', '/x/y/z']
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=135)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.input_files\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = cmd.output_files
    @py_assert5 = [
     '/out/foo', 'foo/bar', '/var/log/pipe.stderr']
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=136)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.output_files\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = cmd.auxiliary_files
    @py_assert5 = [
     'wat/wat']
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=139)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.auxiliary_files\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = cmd.expected_temp_files
    @py_assert5 = [
     'foo', 'bar', 'pipe.stderr']
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=140)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.expected_temp_files\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert0 = 'xyb'
    @py_assert4 = cmd.optional_temp_files
    @py_assert2 = @py_assert0 in @py_assert4
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=141)
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.optional_temp_files\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'pipe.stdout'
    @py_assert4 = cmd.optional_temp_files
    @py_assert2 = @py_assert0 in @py_assert4
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=142)
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.optional_temp_files\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_atomiccmd__paths_optional():
    cmd = AtomicCmd(['ls'], IN_OPTIONAL=None, OUT_OPTIONAL=None)
    @py_assert1 = cmd.input_files
    @py_assert5 = frozenset()
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=147)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.input_files\n} == %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = cmd.output_files
    @py_assert5 = frozenset()
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=148)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.output_files\n} == %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_atomiccmd__pipes_stdin(tmp_path):
    fname = test_file('fasta_file.fasta')
    cmd = AtomicCmd('cat', IN_STDIN=fname, OUT_STDOUT='result.txt')
    @py_assert1 = cmd.input_files
    @py_assert5 = [
     fname]
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=154)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.input_files\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=156)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    result = (tmp_path / 'result.txt').read_text()
    @py_assert2 = '>This_is_FASTA!\nACGTN\n>This_is_ALSO_FASTA!\nCGTNA\n'
    @py_assert1 = result == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=158)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_atomiccmd__pipes_stdin__temp_file(tmp_path):
    cmd = AtomicCmd('cat', TEMP_IN_STDIN='infile.fasta', OUT_STDOUT='result.txt')
    @py_assert1 = cmd.input_files
    @py_assert5 = frozenset()
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=163)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.input_files\n} == %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    (tmp_path / 'infile.fasta').write_text('a\nbc\nd')
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=166)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    result = (tmp_path / 'result.txt').read_text()
    @py_assert2 = 'a\nbc\nd'
    @py_assert1 = result == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=168)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_atomiccmd__pipes_stdin__dev_null_implicit_1(tmp_path):
    cmd = AtomicCmd('cat')
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=175)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_atomiccmd__pipes_stdin__dev_null_implicit_2(tmp_path):
    cmd = AtomicCmd('cat', IN_STDIN=None)
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=182)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_atomiccmd__pipes_stdin__dev_null_explicit(tmp_path):
    cmd = AtomicCmd('cat', IN_STDIN=(AtomicCmd.DEVNULL))
    cmd.run(tmp_path, wrap_errors=False)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=189)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


_TEST_OUTPUT_PIPES = (
 (
  'pipe_bash_{0}.stdout', 'pipe_bash_{0}.stderr', {}),
 (
  'pipe_bash_{0}.stdout', 'stderr.txt', {'OUT_STDERR': 'stderr.txt'}),
 (
  'stdout.txt', 'pipe_bash_{0}.stderr', {'OUT_STDOUT': 'stdout.txt'}),
 (
  'stdout.txt',
  'stderr.txt',
  {'OUT_STDOUT':'stdout.txt', 
   'OUT_STDERR':'stderr.txt'}),
 (
  None, None, {'OUT_STDOUT':AtomicCmd.DEVNULL,  'OUT_STDERR':AtomicCmd.DEVNULL}),
 (
  None, 'pipe_bash_{0}.stderr', {'OUT_STDOUT': AtomicCmd.DEVNULL}),
 (
  'pipe_bash_{0}.stdout', None, {'OUT_STDERR': AtomicCmd.DEVNULL}))

@pytest.mark.parametrize('stdout, stderr, kwargs', _TEST_OUTPUT_PIPES)
def test_atomiccmd__pipes_out(tmp_path, stdout, stderr, kwargs):
    call = ('bash', '-c', "echo -n 'STDERR!' > /dev/stderr; echo -n 'STDOUT!';")
    cmd = AtomicCmd(call, **kwargs)
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=214)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    expected_files = []
    for tmpl, text in ((stdout, 'STDOUT!'), (stderr, 'STDERR!')):
        if tmpl is not None:
            fname = tmpl.format(id(cmd))
            result = (tmp_path / fname).read_text()
            @py_assert1 = result == text
            if @py_assert1 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=221)
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, text)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(text) if 'text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(text) else 'text'}
                @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None
            expected_files.append(fname)

    @py_assert2 = os.listdir
    @py_assert5 = @py_assert2(tmp_path)
    @py_assert7 = set(@py_assert5)
    @py_assert12 = set(expected_files)
    @py_assert9 = @py_assert7 == @py_assert12
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=224)
    if not @py_assert9:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}(%(py4)s)\n})\n} == %(py13)s\n{%(py13)s = %(py10)s(%(py11)s)\n}', ), (@py_assert7, @py_assert12)) % {'py0':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py11':@pytest_ar._saferepr(expected_files) if 'expected_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_files) else 'expected_files',  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = None


_MALFORMED_PATH_KEYS = (
 {'IN': '/var/foo'},
 {'IN_': '/var/foo'},
 {'TEMP_OUT': '/var/foo'},
 {'TEMP_OUT_': '/var/foo'},
 {'TEMP_OUX_FOO': 'foo'},
 {'INS_BAR': 'foo'})

@pytest.mark.parametrize('kwargs', _MALFORMED_PATH_KEYS)
def test_atomiccmd__paths__malformed_keys(kwargs):
    with pytest.raises(ValueError):
        AtomicCmd(*('true', ), **kwargs)


_INVALID_PATH_VALUES = (
 {'IN_FILE': 1},
 {'TEMP_IN_FILE': set()},
 {'OUT_FILE': [1, 2, 3]},
 {'TEMP_OUT_FILE': 1.0},
 {'IN_STDIN': {}},
 {'TEMP_IN_STDIN': frozenset()},
 {'OUT_STDOUT': 1.7},
 {'TEMP_OUT_STDOUT': ()},
 {'OUT_STDERR': range(3)},
 {'TEMP_OUT_STDERR': -1})

@pytest.mark.parametrize('kwargs', _INVALID_PATH_VALUES)
def test_atomiccmd__paths__invalid_values(kwargs):
    with pytest.raises(TypeError):
        AtomicCmd(*('true', ), **kwargs)


_INVALID_TEMP_PATHS = (
 {'TEMP_IN_FOO': 'sub/infile'},
 {'TEMP_IN_STDIN': 'sub/stdin'},
 {'TEMP_OUT_FOO': 'sub/outfile'},
 {'TEMP_OUT_STDOUT': 'sub/stdout'},
 {'TEMP_OUT_STDERR': 'sub/stderr'},
 {'TEMP_IN_FOO': '/tmp/sub/infile'},
 {'TEMP_IN_STDIN': '/dev/sub/stdin'},
 {'TEMP_OUT_FOO': '/etc/sub/outfile'},
 {'TEMP_OUT_STDOUT': '/var/sub/stdout'},
 {'TEMP_OUT_STDERR': '/home/sub/stderr'})

@pytest.mark.parametrize('kwargs', _INVALID_TEMP_PATHS)
def test_atomiccmd__paths__invalid_temp_paths(kwargs):
    with pytest.raises(ValueError):
        AtomicCmd(*('true', ), **kwargs)


_OVERLAPPING_OUT_FILENAMES = (
 {'OUT_FILE_1':'/foo/bar/outfile', 
  'OUT_FILE_2':'/var/outfile'},
 {'TEMP_OUT_FILE_1':'outfile', 
  'OUT_FILE_1':'/var/outfile'},
 {'OUT_FILE_1':'/foo/bar/outfile', 
  'TEMP_OUT_FILE_1':'outfile'},
 {'TEMP_OUT_FILE_1':'outfile', 
  'TEMP_OUT_FILE_2':'outfile'},
 {'OUT_FILE_1':'/foo/bar/outfile', 
  'OUT_STDOUT':'/var/outfile'},
 {'TEMP_OUT_FILE_1':'outfile', 
  'OUT_STDOUT':'/var/outfile'},
 {'OUT_FILE_1':'/foo/bar/outfile', 
  'TEMP_OUT_STDOUT':'outfile'},
 {'TEMP_OUT_FILE_1':'outfile', 
  'TEMP_OUT_STDOUT':'outfile'},
 {'OUT_FILE_1':'/foo/bar/outfile', 
  'OUT_STDERR':'/var/outfile'},
 {'TEMP_OUT_FILE_1':'outfile', 
  'OUT_STDERR':'/var/outfile'},
 {'OUT_FILE_1':'/foo/bar/outfile', 
  'TEMP_OUT_STDERR':'outfile'},
 {'TEMP_OUT_FILE_1':'outfile', 
  'TEMP_OUT_STDERR':'outfile'})

@pytest.mark.parametrize('kwargs', _OVERLAPPING_OUT_FILENAMES)
def test_atomiccmd__paths__overlapping_output(kwargs):
    with pytest.raises(ValueError):
        AtomicCmd(*(('ls',), ), **kwargs)


@pytest.mark.parametrize('key', ('IN_STDIN', 'OUT_STDOUT', 'OUT_STDERR'))
def test_atomiccmd__pipes__duplicates(key):
    kwargs = {'TEMP_' + key: 'temp_file', key: 'file'}
    with pytest.raises(CmdError):
        AtomicCmd(['ls'], **kwargs)


def test_atomicmcd__exec__reqobj():
    reqobj = RequirementObj(call=('echo', 'version'), search='version', checks=str)
    cmd = AtomicCmd('true', CHECK_VERSION=reqobj)
    @py_assert1 = cmd.requirements
    @py_assert5 = [
     reqobj]
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=324)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.requirements\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_atomiccmd__checks__non_callable():
    with pytest.raises(TypeError, match='CHECK_FOO must be callable'):
        AtomicCmd('ls', CHECK_FOO='ls')


@pytest.mark.parametrize('obj', (str, {}, 1, b'foo'))
def test_atomiccmd__exec__invalid(obj):
    with pytest.raises(TypeError, match='EXEC_FOO must be string, not '):
        AtomicCmd('true', EXEC_FOO=obj)


@pytest.mark.parametrize('obj', (str, {}, 1, b'foo'))
def test_atomiccmd__aux__invalid(obj):
    with pytest.raises(TypeError, match='AUX_FOO must be string, not '):
        AtomicCmd('true', AUX_FOO=obj)


def test_atomiccmd__paths_non_str(tmp_path):
    cmd = AtomicCmd(('touch', 1234), OUT_FOO='1234', set_cwd=True)
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=359)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = '1234'
    @py_assert13 = @py_assert8(tmp_path, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=360)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_atomiccmd__paths_missing():
    with pytest.raises(CmdError, match='Value not specified for path'):
        AtomicCmd(('touch', '%(IN_FOO)s'))


def test_atomiccmd__paths_invalid():
    with pytest.raises(CmdError, match='incomplete format'):
        AtomicCmd(('touch', '%(IN_FOO)'), IN_FOO='abc')


def test_atomiccmd__paths__key(tmp_path):
    cmd = AtomicCmd(('echo', '-n', '%(TEMP_DIR)s'), OUT_STDOUT=(AtomicCmd.PIPE))
    cmd.run(tmp_path)
    path = cmd._proc.stdout.read()
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.samefile
    @py_assert7 = @py_assert3(tmp_path, path)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=377)
    if not @py_assert7:
        @py_format9 = (@pytest_ar._format_assertmsg((tmp_path, path)) + '\n>assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.samefile\n}(%(py5)s, %(py6)s)\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py6':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert7 = None
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=378)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_atomiccmd__piping(tmp_path):
    cmd_1 = AtomicCmd(['echo', '-n', '#@!$^'], OUT_STDOUT=(AtomicCmd.PIPE))
    @py_assert1 = cmd_1.output_files
    @py_assert5 = frozenset()
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=388)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.output_files\n} == %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(cmd_1) if 'cmd_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_1) else 'cmd_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    cmd_2 = AtomicCmd(['cat'], IN_STDIN=cmd_1, OUT_STDOUT='piped.txt')
    @py_assert1 = cmd_2.input_files
    @py_assert5 = frozenset()
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=390)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.input_files\n} == %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(cmd_2) if 'cmd_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_2) else 'cmd_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    cmd_1.run(tmp_path)
    cmd_2.run(tmp_path)
    @py_assert1 = cmd_1.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=393)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd_1) if 'cmd_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_1) else 'cmd_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = cmd_2.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=394)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd_2) if 'cmd_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_2) else 'cmd_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    result = (tmp_path / 'piped.txt').read_text()
    @py_assert2 = '#@!$^'
    @py_assert1 = result == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=396)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_atomiccmd__piping_temp(tmp_path):
    cmd_1 = AtomicCmd(['echo', '-n', '#@!$^'], TEMP_OUT_STDOUT=(AtomicCmd.PIPE))
    @py_assert1 = cmd_1.output_files
    @py_assert5 = frozenset()
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=401)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.output_files\n} == %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(cmd_1) if 'cmd_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_1) else 'cmd_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    cmd_2 = AtomicCmd(['cat'], TEMP_IN_STDIN=cmd_1, OUT_STDOUT='piped.txt')
    @py_assert1 = cmd_2.input_files
    @py_assert5 = frozenset()
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=403)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.input_files\n} == %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(cmd_2) if 'cmd_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_2) else 'cmd_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    cmd_1.run(tmp_path)
    cmd_2.run(tmp_path)
    @py_assert1 = cmd_1.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=406)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd_1) if 'cmd_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_1) else 'cmd_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = cmd_2.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=407)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd_2) if 'cmd_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_2) else 'cmd_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    result = (tmp_path / 'piped.txt').read_text()
    @py_assert2 = '#@!$^'
    @py_assert1 = result == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=409)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


_INVALID_PIPE_TARGETS = ('IN_FILE_1', 'IN_STDIN', 'OUT_FILE_2', 'OUT_STDERR', 'TEMP_IN_FILE_1',
                         'TEMP_IN_STDIN', 'TEMP_OUT_FILE_2', 'TEMP_OUT_STDERR')

@pytest.mark.parametrize('key', _INVALID_PIPE_TARGETS)
def test_atomiccmd__piping__wrong_pipe(key):
    with pytest.raises(TypeError):
        AtomicCmd(*('ls', ), **{key: AtomicCmd.PIPE})


def test_atomiccmd__piping_is_only_allowed_once(tmp_path):
    cmd_1 = AtomicCmd(['echo', '-n', 'foo\nbar'], OUT_STDOUT=(AtomicCmd.PIPE))
    cmd_2a = AtomicCmd(['grep', 'foo'], IN_STDIN=cmd_1)
    cmd_2b = AtomicCmd(['grep', 'bar'], IN_STDIN=cmd_1)
    cmd_1.run(tmp_path)
    cmd_2a.run(tmp_path)
    with pytest.raises(CmdError):
        cmd_2b.run(tmp_path)
    @py_assert1 = cmd_1.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=439)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd_1) if 'cmd_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_1) else 'cmd_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = cmd_2a.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=440)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd_2a) if 'cmd_2a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_2a) else 'cmd_2a',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = cmd_2b.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     None]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=441)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd_2b) if 'cmd_2b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_2b) else 'cmd_2b',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_atomiccmd__run__already_running(tmp_path):
    cmd = AtomicCmd(('sleep', '10'))
    cmd.run(tmp_path)
    with pytest.raises(CmdError):
        cmd.run(tmp_path)
    cmd.terminate()
    cmd.join()


def test_atomiccmd__run__exception_on_missing_command(tmp_path):
    cmd = AtomicCmd(('xyzabcefgh', '10'))
    with pytest.raises(CmdError):
        cmd.run(tmp_path)
    cmd.terminate()
    cmd.join()


def test_atomiccmd__run__exception_on_missing_command__no_wrap(tmp_path):
    cmd = AtomicCmd(('xyzabcefgh', '10'))
    with pytest.raises(OSError):
        cmd.run(tmp_path, wrap_errors=False)
    cmd.terminate()
    cmd.join()


def test_atomiccmd__run__invalid_temp(tmp_path):
    cmd = AtomicCmd(('sleep', '10'))
    with pytest.raises(CmdError):
        cmd.run(os.path.join(tmp_path, 'foo'))
    cmd.terminate()
    cmd.join()


def test_atomiccmd__ready(tmp_path):
    cmd = AtomicCmd('ls')
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     None]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=489)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = cmd.ready
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=490)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ready\n}()\n}' % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=492)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = cmd.ready
    @py_assert3 = @py_assert1()
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=493)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ready\n}()\n}' % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


@pytest.mark.parametrize('call, after', (('true', 0), ('false', 1)))
def test_atomiccmd__join(tmp_path, call, after):
    cmd = AtomicCmd(call)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     None]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=504)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     after]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=506)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


@pytest.mark.parametrize('call, after', (('true', 0), ('false', 1)))
def test_atomiccmd__wait(tmp_path, call, after):
    cmd = AtomicCmd(call)
    @py_assert1 = cmd.wait
    @py_assert3 = @py_assert1()
    @py_assert6 = None
    @py_assert5 = @py_assert3 is @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=512)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.wait\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    cmd.run(tmp_path)
    @py_assert1 = cmd.wait
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == after
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=514)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.wait\n}()\n} == %(py6)s', ), (@py_assert3, after)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(after) if 'after' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(after) else 'after'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_atomiccmd__terminate(tmp_path):
    cmd = AtomicCmd(('sleep', '10'))
    cmd.run(tmp_path)
    with patch('os.killpg', wraps=(os.killpg)) as (os_killpg):
        cmd.terminate()
        @py_assert1 = cmd.join
        @py_assert3 = @py_assert1()
        @py_assert6 = [
         'SIGTERM']
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=528)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = os_killpg.mock_calls
        @py_assert4 = [
         call(cmd._proc.pid, signal.SIGTERM)]
        @py_assert3 = @py_assert1 == @py_assert4
        if @py_assert3 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=530)
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(os_killpg) if 'os_killpg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os_killpg) else 'os_killpg',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None


def test_atomiccmd__terminate_exception(tmp_path):
    killpg = os.killpg
    cmd = AtomicCmd(('sleep', '10'))
    cmd.run(tmp_path)

    def _killpg(pid, sig):
        killpg(pid, sig)
        raise OSError('Proccess not found')

    with patch('os.killpg', wraps=_killpg) as (os_killpg):
        cmd.terminate()
        @py_assert1 = cmd.join
        @py_assert3 = @py_assert1()
        @py_assert6 = [
         'SIGTERM']
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=544)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = os_killpg.mock_calls
        @py_assert4 = [
         call(cmd._proc.pid, signal.SIGTERM)]
        @py_assert3 = @py_assert1 == @py_assert4
        if @py_assert3 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=546)
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(os_killpg) if 'os_killpg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os_killpg) else 'os_killpg',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None


def test_atomiccmd__terminate_race_condition(tmp_path):
    cmd = AtomicCmd('true')
    cmd.run(tmp_path)
    while cmd._proc.poll() is None:
        pass

    cmd.terminate()
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=557)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_atomiccmd__terminate_after_join(tmp_path):
    cmd = AtomicCmd('true')
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=564)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    cmd.terminate()
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=566)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_atomiccmd__terminate_sigterm(tmp_path):
    cmd = AtomicCmd(('sleep', '10'))
    cmd.run(tmp_path)
    cmd.terminate()
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     'SIGTERM']
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=574)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_atomiccmd__terminate_sigkill(tmp_path):
    cmd = AtomicCmd(('sleep', '10'))
    cmd.run(tmp_path)
    cmd._proc.kill()
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     'SIGKILL']
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=581)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def _setup_for_commit(tmp_path, create_cmd=True):
    destination = tmp_path / 'out'
    tmp_path = tmp_path / 'tmp'
    os.makedirs(destination)
    os.makedirs(tmp_path)
    if not create_cmd:
        return (destination, tmp_path)
    else:
        cmd = AtomicCmd(('touch', '%(OUT_FOO)s'), OUT_FOO=(os.path.join(destination, '1234')))
        cmd.run(tmp_path)
        @py_assert1 = cmd.join
        @py_assert3 = @py_assert1()
        @py_assert6 = [
         0]
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=600)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        return (
         destination, tmp_path, cmd)


def test_atomiccmd__commit_simple(tmp_path):
    destination, tmp_path, cmd = _setup_for_commit(tmp_path)
    cmd.commit(tmp_path)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = '1234'
    @py_assert13 = @py_assert8(tmp_path, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    @py_assert17 = not @py_assert15
    if @py_assert17 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=608)
    if not @py_assert17:
        @py_format18 = 'assert not %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = '1234'
    @py_assert13 = @py_assert8(destination, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=609)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(destination) if 'destination' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination) else 'destination',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_atomiccmd__commit_temp_out(tmp_path):
    dest, temp = _setup_for_commit(tmp_path, create_cmd=False)
    cmd = AtomicCmd(('echo', 'foo'),
      OUT_STDOUT=(os.path.join(dest, 'foo.txt')),
      TEMP_OUT_FOO='bar.txt')
    cmd.run(temp)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=620)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    (temp / 'bar.txt').write_text('1 2 3')
    cmd.commit(temp)
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(temp)
    @py_assert7 = []
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=623)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(temp) if 'temp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp) else 'temp',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(dest)
    @py_assert7 = [
     'foo.txt']
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=624)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_atomiccmd__commit_temp_only(tmp_path):
    cmd = AtomicCmd(('echo', 'foo'), TEMP_OUT_STDOUT='bar.txt')
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=630)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'bar.txt'
    @py_assert13 = @py_assert8(tmp_path, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=631)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None
    cmd.commit(tmp_path)
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    @py_assert7 = []
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=633)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_atomiccmd__commit_before_run():
    cmd = AtomicCmd('true')
    with pytest.raises(CmdError):
        cmd.commit('/tmp')


def test_atomiccmd__commit_while_running(tmp_path):
    cmd = AtomicCmd(('sleep', '10'))
    cmd.run(tmp_path)
    with pytest.raises(CmdError):
        cmd.commit(tmp_path)
    cmd.terminate()
    cmd.join()


def test_atomiccmd__commit_before_join(tmp_path):
    cmd = AtomicCmd(('sleep', '0.1'))
    cmd.run(tmp_path)
    while cmd._proc.poll() is None:
        pass

    with pytest.raises(CmdError):
        cmd.commit(tmp_path)
    cmd.join()


def test_atomiccmd__commit_temp_folder(tmp_path):
    destination, tmp_path, cmd = _setup_for_commit(tmp_path)
    cmd.commit(os.path.realpath(tmp_path))
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = '1234'
    @py_assert13 = @py_assert8(tmp_path, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    @py_assert17 = not @py_assert15
    if @py_assert17 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=665)
    if not @py_assert17:
        @py_format18 = 'assert not %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = '1234'
    @py_assert13 = @py_assert8(destination, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=666)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(destination) if 'destination' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination) else 'destination',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_atomiccmd__commit_wrong_temp_folder(tmp_path):
    destination, tmp_path, cmd = _setup_for_commit(tmp_path)
    with pytest.raises(CmdError):
        cmd.commit(destination)


def test_atomiccmd__commit_missing_files(tmp_path):
    destination, tmp_path = _setup_for_commit(tmp_path, False)
    cmd = AtomicCmd(('touch', '%(OUT_FOO)s'),
      OUT_FOO=(os.path.join(destination, '1234')),
      OUT_BAR=(os.path.join(destination, '4567')))
    cmd.run(tmp_path)
    cmd.join()
    before = set(os.listdir(tmp_path))
    with pytest.raises(CmdError):
        cmd.commit(tmp_path)
    @py_assert4 = os.listdir
    @py_assert7 = @py_assert4(tmp_path)
    @py_assert9 = set(@py_assert7)
    @py_assert1 = before == @py_assert9
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=687)
    if not @py_assert1:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py10)s\n{%(py10)s = %(py2)s(%(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.listdir\n}(%(py6)s)\n})\n}', ), (before, @py_assert9)) % {'py0':@pytest_ar._saferepr(before) if 'before' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(before) else 'before',  'py2':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py3':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert7 = @py_assert9 = None


def test_atomiccmd__commit_failure_cleanup(tmp_path):
    counter = []
    move_file = fileutils.move_file

    def _monkey_move_file(source, destination):
        if counter:
            raise OSError('ARRRGHHH!')
        counter.append(destination)
        return move_file(source, destination)

    destination, tmp_path = _setup_for_commit(tmp_path, False)
    command = AtomicCmd(('touch', '%(OUT_FILE_1)s', '%(OUT_FILE_2)s', '%(OUT_FILE_3)s'),
      OUT_FILE_1=(os.path.join(destination, 'file_1')),
      OUT_FILE_2=(os.path.join(destination, 'file_2')),
      OUT_FILE_3=(os.path.join(destination, 'file_3')))
    try:
        fileutils.move_file = _monkey_move_file
        command.run(tmp_path)
        @py_assert1 = command.join
        @py_assert3 = @py_assert1()
        @py_assert6 = [
         0]
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=712)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(command) if 'command' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(command) else 'command',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        with pytest.raises(OSError):
            command.commit(tmp_path)
        @py_assert2 = os.listdir
        @py_assert5 = @py_assert2(destination)
        @py_assert7 = tuple(@py_assert5)
        @py_assert10 = ()
        @py_assert9 = @py_assert7 == @py_assert10
        if @py_assert9 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=716)
        if not @py_assert9:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}(%(py4)s)\n})\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(destination) if 'destination' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination) else 'destination',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    finally:
        fileutils.move_file = move_file


def test_atomiccmd__commit_with_pipes(tmp_path):
    destination, tmp_path = _setup_for_commit(tmp_path, False)
    command_1 = AtomicCmd(('echo', 'Hello, World!'), OUT_STDOUT=(AtomicCmd.PIPE))
    command_2 = AtomicCmd(('gzip', ),
      IN_STDIN=command_1, OUT_STDOUT=(os.path.join(destination, 'foo.gz')))
    command_1.run(tmp_path)
    command_2.run(tmp_path)
    @py_assert1 = command_1.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=731)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(command_1) if 'command_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(command_1) else 'command_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = command_2.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=732)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(command_2) if 'command_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(command_2) else 'command_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    command_1.commit(tmp_path)
    command_2.commit(tmp_path)
    @py_assert2 = os.listdir
    @py_assert5 = @py_assert2(destination)
    @py_assert7 = set(@py_assert5)
    @py_assert11 = ('foo.gz', )
    @py_assert13 = set(@py_assert11)
    @py_assert9 = @py_assert7 == @py_assert13
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=737)
    if not @py_assert9:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}(%(py4)s)\n})\n} == %(py14)s\n{%(py14)s = %(py10)s(%(py12)s)\n}', ), (@py_assert7, @py_assert13)) % {'py0':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(destination) if 'destination' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination) else 'destination',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert2 = os.listdir
    @py_assert5 = @py_assert2(tmp_path)
    @py_assert7 = set(@py_assert5)
    @py_assert11 = set()
    @py_assert9 = @py_assert7 == @py_assert11
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=738)
    if not @py_assert9:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}(%(py4)s)\n})\n} == %(py12)s\n{%(py12)s = %(py10)s()\n}', ), (@py_assert7, @py_assert11)) % {'py0':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_atomiccmd__str__():
    cmd = AtomicCmd(('echo', 'test'))
    @py_assert1 = paleomix.atomiccmd
    @py_assert3 = @py_assert1.pprint
    @py_assert5 = @py_assert3.pformat
    @py_assert8 = @py_assert5(cmd)
    @py_assert13 = str(cmd)
    @py_assert10 = @py_assert8 == @py_assert13
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=749)
    if not @py_assert10:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.atomiccmd\n}.pprint\n}.pformat\n}(%(py7)s)\n} == %(py14)s\n{%(py14)s = %(py11)s(%(py12)s)\n}', ), (@py_assert8, @py_assert13)) % {'py0':@pytest_ar._saferepr(paleomix) if 'paleomix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paleomix) else 'paleomix',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py12':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert13 = None


def test_atomiccmd__cleanup_proc__commit(tmp_path):
    @py_assert1 = paleomix.atomiccmd
    @py_assert3 = @py_assert1.command
    @py_assert5 = @py_assert3._PROCS
    @py_assert9 = set()
    @py_assert7 = @py_assert5 == @py_assert9
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=762)
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.atomiccmd\n}.command\n}._PROCS\n} == %(py10)s\n{%(py10)s = %(py8)s()\n}', ), (@py_assert5, @py_assert9)) % {'py0':@pytest_ar._saferepr(paleomix) if 'paleomix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paleomix) else 'paleomix',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    cmd = AtomicCmd('ls')
    cmd.run(tmp_path)
    ref = next(iter(paleomix.atomiccmd.command._PROCS))
    @py_assert1 = ref()
    @py_assert5 = cmd._proc
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=767)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py6)s\n{%(py6)s = %(py4)s._proc\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(ref) if 'ref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref) else 'ref',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=768)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    cmd.commit(tmp_path)
    @py_assert1 = ref()
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=771)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(ref) if 'ref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref) else 'ref',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert3 = paleomix.atomiccmd
    @py_assert5 = @py_assert3.command
    @py_assert7 = @py_assert5._PROCS
    @py_assert1 = ref not in @py_assert7
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=773)
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.atomiccmd\n}.command\n}._PROCS\n}', ), (ref, @py_assert7)) % {'py0':@pytest_ar._saferepr(ref) if 'ref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref) else 'ref',  'py2':@pytest_ar._saferepr(paleomix) if 'paleomix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paleomix) else 'paleomix',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_atomiccmd__cleanup_proc__gc(tmp_path):
    @py_assert1 = paleomix.atomiccmd
    @py_assert3 = @py_assert1.command
    @py_assert5 = @py_assert3._PROCS
    @py_assert9 = set()
    @py_assert7 = @py_assert5 == @py_assert9
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=778)
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.atomiccmd\n}.command\n}._PROCS\n} == %(py10)s\n{%(py10)s = %(py8)s()\n}', ), (@py_assert5, @py_assert9)) % {'py0':@pytest_ar._saferepr(paleomix) if 'paleomix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paleomix) else 'paleomix',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    cmd = AtomicCmd('ls')
    cmd.run(tmp_path)
    ref = next(iter(paleomix.atomiccmd.command._PROCS))
    @py_assert1 = ref()
    @py_assert5 = cmd._proc
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=783)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py6)s\n{%(py6)s = %(py4)s._proc\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(ref) if 'ref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref) else 'ref',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=784)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    cmd = None
    @py_assert1 = ref()
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=787)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(ref) if 'ref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref) else 'ref',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert3 = paleomix.atomiccmd
    @py_assert5 = @py_assert3.command
    @py_assert7 = @py_assert5._PROCS
    @py_assert1 = ref not in @py_assert7
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=789)
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.atomiccmd\n}.command\n}._PROCS\n}', ), (ref, @py_assert7)) % {'py0':@pytest_ar._saferepr(ref) if 'ref' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref) else 'ref',  'py2':@pytest_ar._saferepr(paleomix) if 'paleomix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paleomix) else 'paleomix',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_atomiccmd__cleanup_sigterm():
    procs = [
     lambda : Mock(pid=7913), lambda : Mock(pid=12345)]
    with patch('paleomix.atomiccmd.command._PROCS', procs):
        patches = Mock()
        with patch('os.killpg', patches.killpg):
            with patch('sys.exit', patches.exit):
                paleomix.atomiccmd.command._cleanup_children(signal.SIGTERM, None)
                @py_assert1 = patches.mock_calls
                @py_assert4 = [
                 call.killpg(7913, signal.SIGTERM), call.killpg(12345, signal.SIGTERM), call.exit(-signal.SIGTERM)]
                @py_assert3 = @py_assert1 == @py_assert4
                if @py_assert3 is None:
                    from _pytest.warning_types import PytestAssertRewriteWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=800)
                if not @py_assert3:
                    @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(patches) if 'patches' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(patches) else 'patches',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                    @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format8))
                @py_assert1 = @py_assert3 = @py_assert4 = None


def test_atomiccmd__cleanup_sigterm__continues_on_exception():
    procs = [
     lambda : Mock(pid=7913), lambda : Mock(pid=12345)]
    with patch('paleomix.atomiccmd.command._PROCS', procs):
        patches = Mock()
        with patch('os.killpg', patches.killpg):
            with patch('sys.exit', patches.exit):
                patches.killpg.side_effect = [
                 OSError('already killed'), None]
                paleomix.atomiccmd.command._cleanup_children(signal.SIGTERM, None)
                @py_assert1 = patches.mock_calls
                @py_assert4 = [
                 call.killpg(7913, signal.SIGTERM), call.killpg(12345, signal.SIGTERM), call.exit(-signal.SIGTERM)]
                @py_assert3 = @py_assert1 == @py_assert4
                if @py_assert3 is None:
                    from _pytest.warning_types import PytestAssertRewriteWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=817)
                if not @py_assert3:
                    @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(patches) if 'patches' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(patches) else 'patches',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                    @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format8))
                @py_assert1 = @py_assert3 = @py_assert4 = None


def test_atomiccmd__cleanup_sigterm__dead_weakrefs():
    dead_ref = weakref.ref(AtomicCmd('ls'))
    with patch('paleomix.atomiccmd.command._PROCS', [dead_ref]):
        patches = Mock()
        with patch('os.killpg', patches.killpg):
            with patch('sys.exit', patches.exit):
                paleomix.atomiccmd.command._cleanup_children(signal.SIGTERM, None)
                @py_assert1 = patches.mock_calls
                @py_assert4 = [
                 call.exit(-signal.SIGTERM)]
                @py_assert3 = @py_assert1 == @py_assert4
                if @py_assert3 is None:
                    from _pytest.warning_types import PytestAssertRewriteWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/command_test.py', lineno=833)
                if not @py_assert3:
                    @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(patches) if 'patches' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(patches) else 'patches',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                    @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format8))
                @py_assert1 = @py_assert3 = @py_assert4 = None