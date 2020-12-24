# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_external_modules.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 3658 bytes
"""Test module for the use of external modules."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from sys import platform
import pytest
from astrality.context import Context
from astrality.module import ModuleManager
from astrality.tests.utils import Retry
MACOS = platform == 'darwin'

def test_that_external_modules_are_brought_in(test_config_directory):
    application_config = {'modules': {'modules_directory':'test_modules', 
                 'enabled_modules':[
                  {'name': 'thailand::thailand'},
                  {'name': '*'}]}}
    modules = {'cambodia': {'enabled_modules': True}}
    module_manager = ModuleManager(config=application_config,
      modules=modules)
    @py_assert2 = module_manager.modules
    @py_assert4 = @py_assert2.keys
    @py_assert6 = @py_assert4()
    @py_assert8 = tuple(@py_assert6)
    @py_assert11 = ('thailand::thailand', 'cambodia')
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.modules\n}.keys\n}()\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py1':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


@pytest.yield_fixture
def temp_test_files(test_config_directory):
    module_dir = test_config_directory / 'test_modules' / 'using_all_actions'
    watched_file = module_dir / 'watched_for_modifications'
    compile_target = module_dir / 'compiled.tmp'
    touch_target = module_dir / 'touched.tmp'
    watch_touch_target = module_dir / 'watch_touched.tmp'
    for file in (compile_target, touch_target, watch_touch_target):
        if file.is_file():
            os.remove(file)

    yield (
     compile_target, touch_target, watch_touch_target, watched_file)
    for file in (compile_target, touch_target, watch_touch_target):
        if file.is_file():
            os.remove(file)


@pytest.mark.slow
@pytest.mark.skipif(MACOS, reason='Flaky on MacOS')
def test_correct_relative_paths_used_in_external_module(temp_test_files, test_config_directory):
    application_config = {'modules': {'modules_directory':'test_modules', 
                 'enabled_modules':[
                  {'name': 'using_all_actions::*'}]}}
    module_manager = ModuleManager(config=application_config)
    compile_target, touch_target, watch_touch_target, watched_file = temp_test_files
    for file in (compile_target, touch_target, watch_touch_target):
        @py_assert1 = file.is_file
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None

    module_manager.finish_tasks()
    with open(compile_target, 'r') as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = "Vietnam's capitol is Ho Chi Minh City"
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = touch_target.is_file
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(touch_target) if 'touch_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(touch_target) else 'touch_target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    watched_file.write_text('This watched file has been modified')
    retry = Retry()
    @py_assert1 = lambda : compile_target.read_text() == "Vietnam's capitol is Hanoi"
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = lambda : watch_touch_target.is_file()
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    touch_target.unlink()
    compile_target.unlink()
    watch_touch_target.unlink()
    watched_file.write_text('')


def test_that_external_module_contexts_are_imported_correctly(test_config_directory):
    application_config = {'modules': {'modules_directory':'test_modules', 
                 'enabled_modules':[
                  {'name': 'module_with_context::*'}]}}
    context = Context({'china': {'capitol': 'beijing'}})
    module_manager = ModuleManager(config=application_config,
      context=context)
    expected_context = Context({'laos':{'capitol': 'vientiane'}, 
     'china':{'capitol': 'beijing'}})
    @py_assert1 = module_manager.application_context
    @py_assert3 = @py_assert1 == expected_context
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.application_context\n} == %(py4)s', ), (@py_assert1, expected_context)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected_context) if 'expected_context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_context) else 'expected_context'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None