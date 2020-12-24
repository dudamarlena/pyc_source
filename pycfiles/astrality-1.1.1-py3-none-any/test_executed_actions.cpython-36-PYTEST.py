# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/persistence/test_executed_actions.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 2333 bytes
"""Tests for astrality.persistence.ExecutedActions."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, logging
from astrality.persistence import ExecutedActions

def test_that_executed_action_path_is_monkeypatched_in_all_files():
    """Autouse fixture should monkeypatch path property of ExecutedActions."""
    executed_actions = ExecutedActions(module_name='github::user/repo::module')
    path = executed_actions.path
    @py_assert1 = path.is_file
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = path.name
    @py_assert4 = 'setup.yml'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = path.parent
    @py_assert3 = @py_assert1.name
    @py_assert6 = 'astrality'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parent\n}.name\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = 'test'
    @py_assert3 = path.parents[3]
    @py_assert5 = @py_assert3.name
    @py_assert2 = @py_assert0 in @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py4)s.name\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None


def test_that_actions_are_saved_to_file(caplog):
    """Saved actions should be persisted properly."""
    action_option = {'shell': 'echo setup'}
    executed_actions = ExecutedActions(module_name='github::user/repo::module')
    @py_assert1 = executed_actions.is_new
    @py_assert3 = 'run'
    @py_assert6 = @py_assert1(action_type=@py_assert3, action_options=action_option)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.is_new\n}(action_type=%(py4)s, action_options=%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(executed_actions) if 'executed_actions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(executed_actions) else 'executed_actions',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(action_option) if 'action_option' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(action_option) else 'action_option',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    executed_actions.write()
    @py_assert1 = executed_actions.is_new
    @py_assert3 = 'run'
    @py_assert6 = @py_assert1(action_type=@py_assert3, action_options=action_option)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.is_new\n}(action_type=%(py4)s, action_options=%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(executed_actions) if 'executed_actions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(executed_actions) else 'executed_actions',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(action_option) if 'action_option' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(action_option) else 'action_option',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    del executed_actions
    executed_actions = ExecutedActions(module_name='github::user/repo::module')
    @py_assert1 = executed_actions.is_new
    @py_assert3 = 'run'
    @py_assert6 = @py_assert1(action_type=@py_assert3, action_options=action_option)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.is_new\n}(action_type=%(py4)s, action_options=%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(executed_actions) if 'executed_actions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(executed_actions) else 'executed_actions',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(action_option) if 'action_option' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(action_option) else 'action_option',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    del executed_actions
    executed_actions = ExecutedActions(module_name='github::user/repo::module')
    caplog.clear()
    executed_actions.reset()
    @py_assert1 = executed_actions.is_new
    @py_assert3 = 'run'
    @py_assert6 = @py_assert1(action_type=@py_assert3, action_options=action_option)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.is_new\n}(action_type=%(py4)s, action_options=%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(executed_actions) if 'executed_actions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(executed_actions) else 'executed_actions',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(action_option) if 'action_option' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(action_option) else 'action_option',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert0 = caplog.record_tuples[0][1]
    @py_assert4 = logging.INFO
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.INFO\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(logging) if 'logging' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(logging) else 'logging',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    executed_actions.reset()
    del executed_actions
    executed_actions = ExecutedActions(module_name='github::user/repo::module')
    @py_assert1 = executed_actions.is_new
    @py_assert3 = 'run'
    @py_assert6 = @py_assert1(action_type=@py_assert3, action_options=action_option)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.is_new\n}(action_type=%(py4)s, action_options=%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(executed_actions) if 'executed_actions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(executed_actions) else 'executed_actions',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(action_option) if 'action_option' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(action_option) else 'action_option',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    caplog.clear()
    ExecutedActions(module_name='i_do_not_exist').reset()
    @py_assert0 = caplog.record_tuples[0][1]
    @py_assert4 = logging.ERROR
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.ERROR\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(logging) if 'logging' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(logging) else 'logging',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None