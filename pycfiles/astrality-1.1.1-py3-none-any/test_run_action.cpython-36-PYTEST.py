# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/actions/test_run_action.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 5797 bytes
"""Tests for RunAction."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, logging, os
from pathlib import Path
from astrality.actions import RunAction
from astrality.persistence import CreatedFiles

def test_null_object_pattern():
    """Null objects should be executable."""
    run_action = RunAction(options={}, directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    run_action.execute()


def test_directory_of_executed_shell_command(tmpdir):
    """All commands should be run from `directory`."""
    temp_dir = Path(tmpdir)
    run_action = RunAction(options={'shell':'touch touched.tmp', 
     'timeout':1},
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    run_action.execute()
    @py_assert1 = 'touched.tmp'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = @py_assert3.is_file
    @py_assert6 = @py_assert4()
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = None


def test_that_dry_run_is_respected(tmpdir, caplog):
    """If dry_run is True, no commands should be executed, only logged."""
    temp_dir = Path(tmpdir)
    run_action = RunAction(options={'shell':'touch touched.tmp', 
     'timeout':1},
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    caplog.clear()
    result = run_action.execute(dry_run=True)
    @py_assert2 = ('touch touched.tmp', '')
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'SKIPPED: '
    @py_assert3 = caplog.record_tuples[0][2]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'touch touched.tmp'
    @py_assert3 = caplog.record_tuples[0][2]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = 'touched.tmp'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = @py_assert3.is_file
    @py_assert6 = @py_assert4()
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_use_of_replacer(tmpdir):
    """All commands should be run from `directory`."""
    temp_dir = Path(tmpdir)
    run_action = RunAction(options={'shell':'whatever', 
     'timeout':1},
      directory=temp_dir,
      replacer=(lambda x: 'echo test'),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    command, result = run_action.execute()
    @py_assert2 = 'echo test'
    @py_assert1 = command == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (command, @py_assert2)) % {'py0':@pytest_ar._saferepr(command) if 'command' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(command) else 'command',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 'test'
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_run_timeout_specified_in_action_block(tmpdir):
    """
    Run actions can time out.

    The option `timeout` overrides any timeout providided to `execute()`.
    """
    temp_dir = Path(tmpdir)
    run_action = RunAction(options={'shell':'sleep 0.1 && echo hi', 
     'timeout':0.05},
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    _, result = run_action.execute(default_timeout=10000)
    @py_assert2 = ''
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    run_action = RunAction(options={'shell':'sleep 0.1 && echo hi', 
     'timeout':0.2},
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    _, result = run_action.execute(default_timeout=0)
    @py_assert2 = 'hi'
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_run_timeout_specified_in_execute(tmpdir, caplog):
    """
    Run actions can time out, and should log this.

    The the option `timeout` is not specified, use `default_timeout` argument
    instead.
    """
    temp_dir = Path(tmpdir)
    run_action = RunAction(options={'shell': 'sleep 0.1 && echo hi'},
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    caplog.clear()
    _, result = run_action.execute(default_timeout=0.05)
    @py_assert0 = 'used more than 0.05 seconds'
    @py_assert3 = caplog.record_tuples[1][2]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert2 = ''
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    run_action = RunAction(options={'shell': 'sleep 0.1 && echo hi'},
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    _, result = run_action.execute(default_timeout=0.2)
    @py_assert2 = 'hi'
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_running_shell_command_with_non_zero_exit_code(caplog):
    """Shell commands with non-zero exit codes should log this."""
    run_action = RunAction(options={'shell':'thiscommandshould not exist', 
     'timeout':2},
      directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    caplog.clear()
    run_action.execute()
    @py_assert0 = 'not found'
    @py_assert3 = caplog.record_tuples[1][2]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'non-zero return code'
    @py_assert3 = caplog.record_tuples[2][2]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_running_shell_command_with_environment_variable(caplog):
    """Shell commands should have access to the environment."""
    run_action = RunAction(options={'shell':'echo $USER', 
     'timeout':2},
      directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    caplog.clear()
    run_action.execute()
    @py_assert1 = caplog.record_tuples
    @py_assert4 = [
     (
      'astrality.actions', logging.INFO, f"""Running command "echo {os.environ['USER']}"."""), ('astrality.utils', logging.INFO, os.environ['USER'])]
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.record_tuples\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_that_environment_variables_are_expanded():
    """String parameters in any Action type should expand env variables."""
    run_action = RunAction(options={'shell': 'echo $EXAMPLE_ENV_VARIABLE'},
      directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    command, _ = run_action.execute()
    @py_assert2 = 'echo test_value'
    @py_assert1 = command == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (command, @py_assert2)) % {'py0':@pytest_ar._saferepr(command) if 'command' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(command) else 'command',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None