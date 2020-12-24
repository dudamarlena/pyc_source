# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_keep_running.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 3323 bytes
"""Tests for keep_running property of Module."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.module import Module, ModuleManager
from astrality.tests.utils import Retry

def test_module_that_does_not_need_to_keep_running():
    """on_startup block and on_exit block does not need to keep running."""
    module = Module(name='test',
      module_config={'run':{'shell': 'hi!'}, 
     'on_exit':{'run': {'shell': 'modified!'}}},
      module_directory=(Path('/')))
    @py_assert1 = module.keep_running
    @py_assert4 = False
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.keep_running\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(module) if 'module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module) else 'module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_module_that_needs_to_keep_running_due_to_on_modified():
    """on_modified block needs to keep running."""
    module = Module(name='test',
      module_config={'on_modified': {'some/path': {'run': {'shell': 'modified!'}}}},
      module_directory=(Path('/')))
    @py_assert1 = module.keep_running
    @py_assert4 = True
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.keep_running\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(module) if 'module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module) else 'module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_module_that_needs_to_keep_running_due_to_on_event():
    """on_event with event listener need to keep running."""
    module = Module(name='test',
      module_config={'event_listener':{'type': 'weekday'}, 
     'on_event':{'run': {'shell': 'modified!'}}},
      module_directory=(Path('/')))
    @py_assert1 = module.keep_running
    @py_assert4 = True
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.keep_running\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(module) if 'module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module) else 'module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_module_without_event_listener_does_not_need_to_keep_running():
    """on_event without event listener need not to keep running."""
    module = Module(name='test',
      module_config={'on_event': {'run': {'shell': 'modified!'}}},
      module_directory=(Path('/')))
    @py_assert1 = module.keep_running
    @py_assert4 = False
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.keep_running\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(module) if 'module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module) else 'module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_that_reprocess_modified_files_causes_keep_running():
    """ModuleManager with reprocess_modified_files causes keep_running."""
    module_manager = ModuleManager(config={'modules': {'reprocess_modified_files': True}})
    @py_assert1 = module_manager.keep_running
    @py_assert4 = True
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.keep_running\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_that_no_reprocess_modified_files_does_not_cause_keep_running():
    """ModuleManager without reprocess_modified_files does not keep_running."""
    module_manager = ModuleManager(config={'modules': {'reprocess_modified_files':False, 
                 'enabled_modules':[
                  {'name': 'A'}]}},
      modules={'A': {}})
    @py_assert1 = Retry()
    @py_assert3 = lambda : module_manager.keep_running is False
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s()\n}(%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(Retry) if 'Retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Retry) else 'Retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_that_module_manager_asks_its_modules_if_it_should_keep_running():
    """ModuleManager should query its modules."""
    module_manager = ModuleManager(modules={'A': {'on_modified': {'some/path': {}}}})
    @py_assert1 = module_manager.keep_running
    @py_assert4 = True
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.keep_running\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_that_running_processes_causes_keep_running():
    """If shell commands are running, keep_running should be True."""
    module_manager = ModuleManager(modules={'A': {'run': {'shell': 'sleep 10'}}})
    module_manager.finish_tasks()
    @py_assert1 = module_manager.keep_running
    @py_assert4 = True
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.keep_running\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None