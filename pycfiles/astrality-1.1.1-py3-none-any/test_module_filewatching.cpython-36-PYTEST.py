# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_module_filewatching.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 14866 bytes
"""Tests for module manager behaviour related to file system modifications."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, shutil
from pathlib import Path
from sys import platform
import pytest
from astrality import utils
from astrality.context import Context
from astrality.module import ModuleManager
from astrality.tests.utils import Retry
MACOS = platform == 'darwin'

@pytest.yield_fixture
def modules_config(test_config_directory, temp_directory):
    empty_template = test_config_directory / 'templates' / 'empty.template'
    empty_template_target = empty_template.parent / 'empty_temp_template'
    touch_target = temp_directory / 'touched'
    secondary_template = test_config_directory / 'templates' / 'no_context.template'
    secondary_template_target = temp_directory / 'secondary_template.tmp'
    modules = {'A':{'on_modified': {str(empty_template): {'compile':[
                                             {'content':str(empty_template), 
                                              'target':str(empty_template_target)},
                                             {'content':str(secondary_template), 
                                              'target':str(secondary_template_target)}], 
                                            'run':[
                                             {'shell': 'touch ' + str(touch_target)}]}}}, 
     'B':{}}
    yield (
     modules,
     empty_template,
     empty_template_target,
     touch_target,
     secondary_template,
     secondary_template_target)
    if empty_template.is_file():
        empty_template.write_text('')
    if empty_template_target.is_file():
        os.remove(empty_template_target)
    if secondary_template_target.is_file():
        os.remove(secondary_template_target)
    if touch_target.is_file():
        os.remove(touch_target)


def test_modified_commands_of_module(modules_config):
    modules, empty_template, empty_template_target, touch_target, *_ = modules_config
    module_manager = ModuleManager(modules=modules)
    result = module_manager.modules['A'].execute(action='run',
      block='on_modified',
      path=empty_template)
    @py_assert2 = (
     (
      'touch ' + str(touch_target), ''),)
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_direct_invocation_of_modifed_method_of_module_manager(modules_config):
    modules, empty_template, empty_template_target, touch_target, secondary_template, secondary_template_target = modules_config
    module_manager = ModuleManager(modules=modules)
    empty_template.write_text('new content')
    module_manager.file_system_modified(empty_template)
    @py_assert1 = empty_template_target.is_file
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(empty_template_target) if 'empty_template_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty_template_target) else 'empty_template_target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    with open(empty_template_target) as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = 'new content'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = Retry()
    @py_assert3 = lambda : touch_target.is_file()
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s()\n}(%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(Retry) if 'Retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Retry) else 'Retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None


@pytest.mark.slow
@pytest.mark.skipif(MACOS, reason='Flaky on MacOS')
def test_on_modified_event_in_module(modules_config):
    modules, empty_template, empty_template_target, touch_target, secondary_template, secondary_template_target = modules_config
    module_manager = ModuleManager(modules=modules)
    module_manager.finish_tasks()
    @py_assert1 = empty_template.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = ''
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(empty_template) if 'empty_template' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty_template) else 'empty_template',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = touch_target.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(touch_target) if 'touch_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(touch_target) else 'touch_target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = empty_template_target.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(empty_template_target) if 'empty_template_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty_template_target) else 'empty_template_target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = secondary_template_target.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(secondary_template_target) if 'secondary_template_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(secondary_template_target) else 'secondary_template_target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    empty_template.write_text('new content')
    retry = Retry()
    @py_assert1 = lambda : empty_template_target.is_file()
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = lambda : empty_template_target.read_text() == 'new content'
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = lambda : secondary_template_target.is_file()
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = lambda : secondary_template_target.read_text() == 'one\ntwo\nthree'
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = lambda : touch_target.is_file()
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


@pytest.yield_fixture
def test_template_targets():
    template_target1 = Path('/tmp/astrality/target1')
    template_target2 = Path('/tmp/astrality/target2')
    yield (
     template_target1, template_target2)
    if template_target1.is_file():
        os.remove(template_target1)
    if template_target2.is_file():
        os.remove(template_target2)


@pytest.mark.skipif(MACOS, reason='Flaky on MacOS')
@pytest.mark.slow
def test_hot_reloading(test_template_targets, test_config_directory):
    template_target1, template_target2 = test_template_targets
    config1 = test_config_directory / 'modules1.yml'
    config2 = test_config_directory / 'modules2.yml'
    target_config = test_config_directory / 'modules.yml'
    shutil.copy(str(config1), str(target_config))
    modules1 = utils.compile_yaml(config1,
      context={})
    application_config1 = {'astrality': {'hot_reload_config': True}}
    module_manager = ModuleManager(config=application_config1,
      modules=modules1,
      directory=test_config_directory)
    @py_assert1 = template_target1.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(template_target1) if 'template_target1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template_target1) else 'template_target1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    module_manager.finish_tasks()
    @py_assert1 = template_target1.is_file
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(template_target1) if 'template_target1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template_target1) else 'template_target1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = module_manager.directory_watcher
    @py_assert3 = @py_assert1.observer
    @py_assert5 = @py_assert3.is_alive
    @py_assert7 = @py_assert5()
    if not @py_assert7:
        @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.directory_watcher\n}.observer\n}.is_alive\n}()\n}') % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    shutil.copy(str(config2), str(target_config))
    retry = Retry()
    @py_assert1 = lambda : template_target2.is_file()
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = lambda : not template_target1.is_file()
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    shutil.copy(str(config1), str(target_config))
    @py_assert1 = lambda : template_target1.is_file()
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = lambda : not template_target2.is_file()
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    if target_config.is_file():
        os.remove(target_config)
    module_manager.directory_watcher.stop()


@pytest.yield_fixture
def three_watchable_files(test_config_directory):
    file1 = test_config_directory / 'file1.tmp'
    file2 = test_config_directory / 'file2.tmp'
    file3 = test_config_directory / 'file3.tmp'
    if file1.is_file():
        os.remove(file1)
    if file2.is_file():
        os.remove(file2)
    if file3.is_file():
        os.remove(file3)
    yield (file1, file2, file3)
    if file1.is_file():
        os.remove(file1)
    if file2.is_file():
        os.remove(file2)
    if file3.is_file():
        os.remove(file3)


@pytest.mark.skipif(MACOS, reason='Flaky on MacOS')
@pytest.mark.slow
def test_all_three_actions_in_on_modified_block(three_watchable_files, test_config_directory):
    file1, file2, file3 = three_watchable_files
    car_template = test_config_directory / 'templates' / 'a_car.template'
    mercedes_context = test_config_directory / 'context' / 'mercedes.yml'
    tesla_context = test_config_directory / 'context' / 'tesla.yml'
    modules = {'car': {'on_startup':{'import_context':{'from_path': str(mercedes_context)}, 
              'compile':{'content':str(car_template), 
               'target':str(file1)}}, 
             'on_modified':{str(file2): {'import_context':{'from_path': str(tesla_context)}, 
                           'compile':{'content':str(car_template), 
                            'target':str(file1)}, 
                           'run':{'shell': 'touch ' + str(file3)}}}}}
    module_manager = ModuleManager(modules=modules)
    @py_assert1 = file1.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = file2.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(file2) if 'file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file2) else 'file2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = file3.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(file3) if 'file3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file3) else 'file3',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    module_manager.finish_tasks()
    @py_assert1 = file1.is_file
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = file2.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(file2) if 'file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file2) else 'file2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = file3.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(file3) if 'file3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file3) else 'file3',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    with open(file1) as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = 'My car is a Mercedes'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    file2.write_text('some new content')
    @py_assert1 = Retry()
    @py_assert3 = lambda : file3.is_file()
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s()\n}(%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(Retry) if 'Retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Retry) else 'Retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    module_manager.exit()


@pytest.mark.skipif(MACOS, reason='Flaky on MacOS')
@pytest.mark.slow
def test_recompile_templates_when_modified(three_watchable_files):
    template, target, _ = three_watchable_files
    template.touch()
    modules = {'module_name': {'on_startup': {'compile': {'content':str(template), 
                                                'target':str(target)}}}}
    application_config = {'modules': {'reprocess_modified_files': True}}
    module_manager = ModuleManager(config=application_config,
      modules=modules,
      context=(Context({'section': {1: 'value'}})))
    with open(template) as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = ''
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = target.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    module_manager.finish_tasks()
    with open(target) as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = ''
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    template.write_text('{{ section.2 }}')
    @py_assert1 = Retry()
    @py_assert3 = lambda : target.read_text() == 'value'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s()\n}(%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(Retry) if 'Retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Retry) else 'Retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    module_manager.exit()
    module_manager.directory_watcher.stop()


@pytest.mark.skipif(MACOS, reason='Flaky on MacOS')
@pytest.mark.slow
def test_recompile_templates_when_modified_overridden(three_watchable_files, test_config_directory):
    """
    If a file is watched in a on_modified block, it should override the
    reprocess_modified_files option.
    """
    template, target, touch_target = three_watchable_files
    template.touch()
    modules = {'module_name': {'on_startup':{'compile': {'content':str(template), 
                                  'target':str(target)}}, 
                     'on_modified':{str(template): {'run': {'shell': 'touch ' + str(touch_target)}}}}}
    application_config = {'modules': {'reprocess_modified_files': True}}
    module_manager = ModuleManager(config=application_config,
      modules=modules,
      context=(Context({'section': {1: 'value'}})),
      directory=test_config_directory)
    with open(template) as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = ''
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = target.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    module_manager.finish_tasks()
    with open(target) as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = ''
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    template.write_text('{{ section.2 }}')
    retry = Retry()
    @py_assert1 = lambda : target.read_text() == ''
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = lambda : touch_target.is_file()
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    module_manager.exit()


@pytest.mark.skipif(MACOS, reason='Flaky on MacOS')
@pytest.mark.slow
def test_importing_context_on_modification(three_watchable_files, test_config_directory):
    """Test that context values are imported in on_modified blocks."""
    file1, *_ = three_watchable_files
    mercedes_context = test_config_directory / 'context' / 'mercedes.yml'
    modules = {'module_name': {'on_modified': {str(file1): {'import_context': {'from_path': str(mercedes_context)}}}}}
    module_manager = ModuleManager(modules=modules,
      context=(Context({'car': {'manufacturer': 'Tesla'}})))
    module_manager.finish_tasks()
    @py_assert0 = module_manager.application_context['car']['manufacturer']
    @py_assert3 = 'Tesla'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    file1.touch()
    file1.write_text('new content, resulting in importing Mercedes')
    @py_assert1 = Retry()
    @py_assert3 = lambda : module_manager.application_context['car']['manufacturer'] == 'Mercedes'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s()\n}(%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(Retry) if 'Retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Retry) else 'Retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None


@pytest.mark.skipif(MACOS, reason='Flaky on MacOS')
@pytest.mark.slow
def test_that_stowed_templates_are_also_watched(three_watchable_files):
    """Stowing template instead of compiling it should still be watched."""
    template, target, _ = three_watchable_files
    template.touch()
    modules = {'module_name': {'on_startup': {'stow': {'content':str(template), 
                                             'target':str(target), 
                                             'templates':'(.+)', 
                                             'non_templates':'ignore'}}}}
    application_config = {'modules': {'reprocess_modified_files': True}}
    module_manager = ModuleManager(config=application_config,
      modules=modules,
      context=(Context({'section': {1: 'value'}})))
    with open(template) as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = ''
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = target.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    module_manager.finish_tasks()
    with open(target) as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = ''
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    template.write_text('{{ section.2 }}')
    @py_assert1 = Retry()
    @py_assert3 = lambda : target.read_text() == 'value'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s()\n}(%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(Retry) if 'Retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Retry) else 'Retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    module_manager.exit()