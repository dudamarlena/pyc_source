# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 11306 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from unittest.mock import call, Mock
import pytest, paleomix.atomiccmd.pprint
from paleomix.atomiccmd.command import AtomicCmd, CmdError
from paleomix.atomiccmd.sets import ParallelCmds, SequentialCmds
_SET_CLASSES = (
 ParallelCmds, SequentialCmds)

@pytest.mark.parametrize('cls', _SET_CLASSES)
def test_atomicsets__properties(cls):
    cmd_mock_1 = AtomicCmd(('true', ),
      CHECK_A=id,
      EXEC_1='false',
      IN_1='/foo/bar/in_1.file',
      IN_2='/foo/bar/in_2.file',
      OUT_1='/bar/foo/out',
      TEMP_OUT_1='out.log',
      AUX_A='/aux/fA',
      AUX_B='/aux/fB')
    cmd_mock_2 = AtomicCmd(('false', ),
      CHECK_A=list,
      EXEC_1='echo',
      EXEC_2='java',
      IN_1='/foo/bar/in.file',
      OUT_1='out.txt')
    obj = cls([cmd_mock_1, cmd_mock_2])
    @py_assert1 = obj.executables
    @py_assert5 = cmd_mock_1.executables
    @py_assert8 = cmd_mock_2.executables
    @py_assert10 = @py_assert5 | @py_assert8
    @py_assert3 = @py_assert1 == @py_assert10
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=61)
    if not @py_assert3:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.executables\n} == (%(py6)s\n{%(py6)s = %(py4)s.executables\n} | %(py9)s\n{%(py9)s = %(py7)s.executables\n})', ), (@py_assert1, @py_assert10)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(cmd_mock_1) if 'cmd_mock_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_1) else 'cmd_mock_1',  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(cmd_mock_2) if 'cmd_mock_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_2) else 'cmd_mock_2',  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None
    @py_assert1 = obj.requirements
    @py_assert5 = cmd_mock_1.requirements
    @py_assert8 = cmd_mock_2.requirements
    @py_assert10 = @py_assert5 | @py_assert8
    @py_assert3 = @py_assert1 == @py_assert10
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=62)
    if not @py_assert3:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.requirements\n} == (%(py6)s\n{%(py6)s = %(py4)s.requirements\n} | %(py9)s\n{%(py9)s = %(py7)s.requirements\n})', ), (@py_assert1, @py_assert10)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(cmd_mock_1) if 'cmd_mock_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_1) else 'cmd_mock_1',  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(cmd_mock_2) if 'cmd_mock_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_2) else 'cmd_mock_2',  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None
    @py_assert1 = obj.input_files
    @py_assert5 = cmd_mock_1.input_files
    @py_assert8 = cmd_mock_2.input_files
    @py_assert10 = @py_assert5 | @py_assert8
    @py_assert3 = @py_assert1 == @py_assert10
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=63)
    if not @py_assert3:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.input_files\n} == (%(py6)s\n{%(py6)s = %(py4)s.input_files\n} | %(py9)s\n{%(py9)s = %(py7)s.input_files\n})', ), (@py_assert1, @py_assert10)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(cmd_mock_1) if 'cmd_mock_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_1) else 'cmd_mock_1',  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(cmd_mock_2) if 'cmd_mock_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_2) else 'cmd_mock_2',  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None
    @py_assert1 = obj.output_files
    @py_assert5 = cmd_mock_1.output_files
    @py_assert8 = cmd_mock_2.output_files
    @py_assert10 = @py_assert5 | @py_assert8
    @py_assert3 = @py_assert1 == @py_assert10
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=64)
    if not @py_assert3:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.output_files\n} == (%(py6)s\n{%(py6)s = %(py4)s.output_files\n} | %(py9)s\n{%(py9)s = %(py7)s.output_files\n})', ), (@py_assert1, @py_assert10)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(cmd_mock_1) if 'cmd_mock_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_1) else 'cmd_mock_1',  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(cmd_mock_2) if 'cmd_mock_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_2) else 'cmd_mock_2',  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None
    @py_assert1 = obj.auxiliary_files
    @py_assert5 = cmd_mock_1.auxiliary_files
    @py_assert8 = cmd_mock_2.auxiliary_files
    @py_assert10 = @py_assert5 | @py_assert8
    @py_assert3 = @py_assert1 == @py_assert10
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=65)
    if not @py_assert3:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.auxiliary_files\n} == (%(py6)s\n{%(py6)s = %(py4)s.auxiliary_files\n} | %(py9)s\n{%(py9)s = %(py7)s.auxiliary_files\n})', ), (@py_assert1, @py_assert10)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(cmd_mock_1) if 'cmd_mock_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_1) else 'cmd_mock_1',  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(cmd_mock_2) if 'cmd_mock_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_2) else 'cmd_mock_2',  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None
    @py_assert1 = obj.expected_temp_files
    @py_assert5 = [
     'out', 'out.txt']
    @py_assert7 = frozenset(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=68)
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.expected_temp_files\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = obj.optional_temp_files
    @py_assert5 = cmd_mock_1.optional_temp_files
    @py_assert8 = cmd_mock_2.optional_temp_files
    @py_assert10 = @py_assert5 | @py_assert8
    @py_assert3 = @py_assert1 == @py_assert10
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=69)
    if not @py_assert3:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.optional_temp_files\n} == (%(py6)s\n{%(py6)s = %(py4)s.optional_temp_files\n} | %(py9)s\n{%(py9)s = %(py7)s.optional_temp_files\n})', ), (@py_assert1, @py_assert10)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(cmd_mock_1) if 'cmd_mock_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_1) else 'cmd_mock_1',  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(cmd_mock_2) if 'cmd_mock_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_mock_2) else 'cmd_mock_2',  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None


_NO_CLOBBERING_KWARGS = (
 (
  {'OUT_A': '/foo/out.txt'}, {'OUT_B': '/bar/out.txt'}),
 (
  {'OUT_A': '/foo/out.txt'}, {'TEMP_OUT_B': 'out.txt'}),
 (
  {'OUT_A': '/foo/out.txt'}, {'OUT_STDOUT': '/bar/out.txt'}),
 (
  {'OUT_A': '/foo/out.txt'}, {'TEMP_OUT_STDOUT': 'out.txt'}),
 (
  {'OUT_A': '/foo/out.txt'}, {'OUT_STDERR': '/bar/out.txt'}),
 (
  {'OUT_A': '/foo/out.txt'}, {'TEMP_OUT_STDERR': 'out.txt'}))

@pytest.mark.parametrize('cls', _SET_CLASSES)
@pytest.mark.parametrize('kwargs_1, kwargs_2', _NO_CLOBBERING_KWARGS)
def test_atomicsets__no_clobbering(cls, kwargs_1, kwargs_2):
    cmd_1 = AtomicCmd(*('true', ), **kwargs_1)
    cmd_2 = AtomicCmd(*('true', ), **kwargs_2)
    with pytest.raises(CmdError):
        cls([cmd_1, cmd_2])


@pytest.mark.parametrize('cls', _SET_CLASSES)
def test_atomicsets__commit(cls):
    mock = Mock()
    cmd_1 = AtomicCmd(['ls'])
    cmd_1.commit = mock.commit_1
    cmd_2 = AtomicCmd(['ls'])
    cmd_2.commit = mock.commit_2
    cmd_3 = AtomicCmd(['ls'])
    cmd_3.commit = mock.commit_3
    cls((cmd_1, cmd_2, cmd_3)).commit('xTMPx')
    @py_assert1 = mock.mock_calls
    @py_assert4 = [
     call.commit_1('xTMPx'), call.commit_2('xTMPx'), call.commit_3('xTMPx')]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=111)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.parametrize('cls', _SET_CLASSES)
def test_atomicsets__stdout(cls):
    cmds = cls([AtomicCmd('ls')])
    with pytest.raises(CmdError):
        cmds.stdout


@pytest.mark.parametrize('cls', _SET_CLASSES)
def test_atomicsets__terminate(cls):
    mock = Mock()
    cmd_1 = AtomicCmd(['ls'])
    cmd_1.terminate = mock.terminate_1
    cmd_2 = AtomicCmd(['ls'])
    cmd_2.terminate = mock.terminate_2
    cmd_3 = AtomicCmd(['ls'])
    cmd_3.terminate = mock.terminate_3
    cmds = cls((cmd_3, cmd_2, cmd_1))
    cmds.terminate()
    @py_assert1 = mock.mock_calls
    @py_assert4 = [
     call.terminate_3(), call.terminate_2(), call.terminate_1()]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=138)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.parametrize('cls', _SET_CLASSES)
def test_atomicsets__str__(cls):
    cmds = cls([AtomicCmd('ls')])
    @py_assert1 = paleomix.atomiccmd
    @py_assert3 = @py_assert1.pprint
    @py_assert5 = @py_assert3.pformat
    @py_assert8 = @py_assert5(cmds)
    @py_assert13 = str(cmds)
    @py_assert10 = @py_assert8 == @py_assert13
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=148)
    if not @py_assert10:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.atomiccmd\n}.pprint\n}.pformat\n}(%(py7)s)\n} == %(py14)s\n{%(py14)s = %(py11)s(%(py12)s)\n}', ), (@py_assert8, @py_assert13)) % {'py0':@pytest_ar._saferepr(paleomix) if 'paleomix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paleomix) else 'paleomix',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py12':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert13 = None


@pytest.mark.parametrize('cls', _SET_CLASSES)
def test_atomicsets__duplicate_cmds(cls):
    cmd_1 = AtomicCmd('true')
    cmd_2 = AtomicCmd('false')
    with pytest.raises(ValueError):
        cls([cmd_1, cmd_2, cmd_1])


def test_parallel_commands__run():
    mock = Mock()
    cmd_1 = AtomicCmd(['ls'])
    cmd_1.run = mock.run_1
    cmd_2 = AtomicCmd(['ls'])
    cmd_2.run = mock.run_2
    cmd_3 = AtomicCmd(['ls'])
    cmd_3.run = mock.run_3
    cmds = ParallelCmds((cmd_1, cmd_2, cmd_3))
    cmds.run('xTMPx')
    @py_assert1 = mock.mock_calls
    @py_assert4 = [
     call.run_1('xTMPx'), call.run_2('xTMPx'), call.run_3('xTMPx')]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=176)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.parametrize('value', (True, False))
def test_parallel_commands__ready_single(value):
    cmd = AtomicCmd(['ls'])
    cmd.ready = Mock()
    cmd.ready.return_value = value
    cmds = ParallelCmds([cmd])
    @py_assert1 = cmds.ready
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == value
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=189)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ready\n}()\n} == %(py6)s', ), (@py_assert3, value)) % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    cmd.ready.assert_called()


_READY_TWO_VALUES = ((True, True, True), (False, True, False), (True, False, False),
                     (False, False, False))

@pytest.mark.parametrize('first, second, result', _READY_TWO_VALUES)
def test_parallel_commands__ready_two(first, second, result):
    cmd_1 = AtomicCmd(['ls'])
    cmd_1.ready = Mock()
    cmd_1.ready.return_value = first
    cmd_2 = AtomicCmd(['ls'])
    cmd_2.ready = Mock()
    cmd_2.ready.return_value = second
    cmds = ParallelCmds([cmd_1, cmd_2])
    @py_assert1 = cmds.ready
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == result
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=212)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ready\n}()\n} == %(py6)s', ), (@py_assert3, result)) % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    cmd_1.ready.assert_called()
    @py_assert2 = bool(first)
    @py_assert7 = cmd_2.ready
    @py_assert9 = @py_assert7.call_count
    @py_assert11 = bool(@py_assert9)
    @py_assert4 = @py_assert2 == @py_assert11
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=215)
    if not @py_assert4:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py12)s\n{%(py12)s = %(py5)s(%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.ready\n}.call_count\n})\n}', ), (@py_assert2, @py_assert11)) % {'py0':@pytest_ar._saferepr(bool) if 'bool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bool) else 'bool',  'py1':@pytest_ar._saferepr(first) if 'first' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first) else 'first',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(bool) if 'bool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bool) else 'bool',  'py6':@pytest_ar._saferepr(cmd_2) if 'cmd_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_2) else 'cmd_2',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_parallel_commands__join_before_run():
    mock = Mock()
    cmd_1 = AtomicCmd(['ls'])
    cmd_1.join = mock.join_1
    cmd_2 = AtomicCmd(['ls'])
    cmd_2.join = mock.join_2
    cmd_3 = AtomicCmd(['ls'])
    cmd_3.join = mock.join_3
    cmds = ParallelCmds((cmd_3, cmd_2, cmd_1))
    @py_assert1 = cmds.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     None, None, None]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=228)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = mock.mock_calls
    @py_assert4 = []
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=230)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_parallel_commands__join_after_run(tmp_path):
    cmds = ParallelCmds([AtomicCmd('true') for _ in range(3)])
    cmds.run(tmp_path)
    @py_assert1 = cmds.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0, 0, 0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=236)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def _setup_mocks_for_failure(*do_mocks):
    results = []
    for do_mock in do_mocks:
        if do_mock:
            mock = AtomicCmd(('sleep', 10))
        else:
            mock = AtomicCmd('false')
        results.append(mock)

    return results


def test_parallel_commands__join_failure_1(tmp_path):
    mocks = _setup_mocks_for_failure(False, True, True)
    cmds = ParallelCmds(mocks)
    cmds.run(tmp_path)
    @py_assert1 = cmds.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     1, 'SIGTERM', 'SIGTERM']
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=254)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_parallel_commands__join_failure_2(tmp_path):
    mocks = _setup_mocks_for_failure(True, False, True)
    cmds = ParallelCmds(mocks)
    cmds.run(tmp_path)
    @py_assert1 = cmds.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     'SIGTERM', 1, 'SIGTERM']
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=261)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_parallel_commands__join_failure_3(tmp_path):
    mocks = _setup_mocks_for_failure(True, True, False)
    cmds = ParallelCmds(mocks)
    cmds.run(tmp_path)
    @py_assert1 = cmds.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     'SIGTERM', 'SIGTERM', 1]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=268)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_parallel_commands__reject_sequential():
    command = AtomicCmd(['ls'])
    seqcmd = SequentialCmds([command])
    with pytest.raises(CmdError):
        ParallelCmds([seqcmd])


def test_parallel_commands__accept_parallel():
    command = AtomicCmd(['ls'])
    parcmd = ParallelCmds([command])
    ParallelCmds([parcmd])


def test_parallel_commands__reject_noncommand():
    with pytest.raises(CmdError):
        ParallelCmds([object()])


def test_parallel_commands__reject_empty_commandset():
    with pytest.raises(CmdError):
        ParallelCmds([])


def test_sequential_commands__atomiccmds():
    mock = Mock()
    cmd_1 = AtomicCmd(['ls'])
    cmd_1.run = mock.run_1
    cmd_1.join = mock.join_1
    cmd_1.join.return_value = [0]
    cmd_2 = AtomicCmd(['ls'])
    cmd_2.run = mock.run_2
    cmd_2.join = mock.join_2
    cmd_2.join.return_value = [0]
    cmd_3 = AtomicCmd(['ls'])
    cmd_3.run = mock.run_3
    cmd_3.join = mock.join_3
    cmd_3.join.return_value = [0]
    cmds = SequentialCmds((cmd_1, cmd_2, cmd_3))
    @py_assert1 = cmds.ready
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=315)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ready\n}()\n}' % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    cmds.run('xTMPx')
    @py_assert1 = cmds.ready
    @py_assert3 = @py_assert1()
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=317)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ready\n}()\n}' % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = cmds.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0, 0, 0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=318)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = mock.mock_calls
    @py_assert4 = [
     call.run_1('xTMPx'), call.join_1(), call.run_2('xTMPx'), call.join_2(), call.run_3('xTMPx'), call.join_3(), call.join_1(), call.join_2(), call.join_3()]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=320)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_sequential_commands__abort_on_error_1(tmp_path):
    cmd_1 = AtomicCmd('false')
    cmd_2 = AtomicCmd(('sleep', 10))
    cmd_3 = AtomicCmd(('sleep', 10))
    cmds = SequentialCmds([cmd_1, cmd_2, cmd_3])
    cmds.run(tmp_path)
    @py_assert1 = cmds.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     1, None, None]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=339)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_sequential_commands__abort_on_error_2(tmp_path):
    cmd_1 = AtomicCmd('true')
    cmd_2 = AtomicCmd('false')
    cmd_3 = AtomicCmd(('sleep', 10))
    cmds = SequentialCmds([cmd_1, cmd_2, cmd_3])
    cmds.run(tmp_path)
    @py_assert1 = cmds.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0, 1, None]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=348)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_sequential_commands__abort_on_error_3(tmp_path):
    cmd_1 = AtomicCmd('true')
    cmd_2 = AtomicCmd('true')
    cmd_3 = AtomicCmd('false')
    cmds = SequentialCmds([cmd_1, cmd_2, cmd_3])
    cmds.run(tmp_path)
    @py_assert1 = cmds.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0, 0, 1]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/sets_test.py', lineno=357)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmds) if 'cmds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmds) else 'cmds',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_sequential_commands__accept_parallel():
    command = AtomicCmd(['ls'])
    parcmd = ParallelCmds([command])
    SequentialCmds([parcmd])


def test_sequential_commands__accept_sequential():
    command = AtomicCmd(['ls'])
    seqcmd = SequentialCmds([command])
    SequentialCmds([seqcmd])


def test_sequential_commands__reject_noncommand():
    with pytest.raises(CmdError):
        SequentialCmds([object()])


def test_sequential_commands__reject_empty_commandset():
    with pytest.raises(CmdError):
        SequentialCmds([])