# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_module.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 27111 bytes
"""Tests for Module class."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, logging, os
from datetime import datetime, timedelta
from pathlib import Path
from freezegun import freeze_time
import pytest
from astrality import event_listener
from astrality.module import Module, ModuleManager
from astrality.context import Context
from astrality.tests.utils import RegexCompare, Retry

@pytest.fixture
def valid_module_section():
    return {'test_module': {'enabled':True, 
                     'event_listener':{'type': 'weekday'}, 
                     'on_startup':{'run':[
                       {'shell': 'echo {event}'}], 
                      'compile':[
                       {'content':'../templates/test_template.conf', 
                        'target':'/tmp/compiled_result'}]}, 
                     'on_event':{'run': [{'shell': 'echo {../templates/test_template.conf}'}]}, 
                     'on_exit':{'run': [{'shell': 'echo exit'}]}}}


@pytest.fixture
def simple_application_config():
    return {'config/modules': {'run_timeout': 2}}


@pytest.fixture
def module(valid_module_section, test_config_directory):
    return Module(name='test_module',
      module_config=(valid_module_section['test_module']),
      module_directory=test_config_directory,
      context_store=(Context({'fonts': {1: 'FuraMono Nerd Font'}})))


@pytest.fixture
def single_module_manager(simple_application_config, valid_module_section):
    return ModuleManager(config=simple_application_config,
      modules=valid_module_section,
      context=(Context({'fonts': {1: 'FuraMono Nerd Font'}})))


class TestModuleClass:

    def test_valid_class_section_method_with_valid_section(self, valid_module_section):
        @py_assert1 = Module.valid_module
        @py_assert3 = 'test'
        @py_assert6 = 2
        @py_assert9 = '/'
        @py_assert11 = Path(@py_assert9)
        @py_assert13 = @py_assert1(name=@py_assert3, config=valid_module_section, requires_timeout=@py_assert6, requires_working_directory=@py_assert11)
        @py_assert16 = True
        @py_assert15 = @py_assert13 is @py_assert16
        if not @py_assert15:
            @py_format18 = @pytest_ar._call_reprcompare(('is', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.valid_module\n}(name=%(py4)s, config=%(py5)s, requires_timeout=%(py7)s, requires_working_directory=%(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n})\n} is %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(Module) if 'Module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Module) else 'Module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(valid_module_section) if 'valid_module_section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(valid_module_section) else 'valid_module_section',  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
            @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
            raise AssertionError(@pytest_ar._format_explanation(@py_format20))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None

    def test_valid_class_section_method_with_disabled_module_section(self):
        disabled_module_section = {'enabled':False, 
         'on_startup':{'run': ['test']}, 
         'on_event':{'run': ['']}, 
         'on_exit':{'run': ['whatever']}}
        @py_assert1 = Module.valid_module
        @py_assert3 = 'test'
        @py_assert6 = 2
        @py_assert9 = '/'
        @py_assert11 = Path(@py_assert9)
        @py_assert13 = @py_assert1(name=@py_assert3, config=disabled_module_section, requires_timeout=@py_assert6, requires_working_directory=@py_assert11)
        @py_assert16 = False
        @py_assert15 = @py_assert13 is @py_assert16
        if not @py_assert15:
            @py_format18 = @pytest_ar._call_reprcompare(('is', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.valid_module\n}(name=%(py4)s, config=%(py5)s, requires_timeout=%(py7)s, requires_working_directory=%(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n})\n} is %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(Module) if 'Module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Module) else 'Module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(disabled_module_section) if 'disabled_module_section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(disabled_module_section) else 'disabled_module_section',  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
            @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
            raise AssertionError(@pytest_ar._format_explanation(@py_format20))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None

    def test_module_event_listener_class(self, module):
        @py_assert2 = module.event_listener
        @py_assert5 = event_listener.Weekday
        @py_assert7 = isinstance(@py_assert2, @py_assert5)
        if not @py_assert7:
            @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.event_listener\n}, %(py6)s\n{%(py6)s = %(py4)s.Weekday\n})\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(module) if 'module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module) else 'module',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(event_listener) if 'event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_listener) else 'event_listener',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert5 = @py_assert7 = None

    def test_using_default_static_event_listener_when_no_event_listener_given(self, test_config_directory):
        static_module = Module(name='static',
          module_config={},
          module_directory=test_config_directory)
        @py_assert2 = static_module.event_listener
        @py_assert5 = event_listener.Static
        @py_assert7 = isinstance(@py_assert2, @py_assert5)
        if not @py_assert7:
            @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.event_listener\n}, %(py6)s\n{%(py6)s = %(py4)s.Static\n})\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(static_module) if 'static_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(static_module) else 'static_module',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(event_listener) if 'event_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(event_listener) else 'event_listener',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert5 = @py_assert7 = None

    @freeze_time('2018-01-27')
    def test_running_module_manager_commands_with_special_interpolations(self, single_module_manager, caplog):
        single_module_manager.startup()
        @py_assert0 = ('astrality.actions', logging.INFO, 'Running command "echo saturday".')
        @py_assert4 = caplog.record_tuples
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.record_tuples\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = (
         'astrality.utils', logging.INFO, 'saturday')
        @py_assert4 = caplog.record_tuples
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.record_tuples\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        caplog.clear()
        single_module_manager.execute(action='run',
          block='on_event',
          module=(single_module_manager.modules['test_module']))
        @py_assert0 = (
         'astrality.actions', logging.INFO, RegexCompare('Running command "echo .+compiled_result"\\.'))
        @py_assert4 = caplog.record_tuples
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.record_tuples\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None

    @freeze_time('2018-01-27')
    def test_running_module_startup_command(self, single_module_manager, module, valid_module_section, caplog):
        single_module_manager.startup()
        @py_assert1 = caplog.record_tuples
        @py_assert4 = [
         (
          'astrality.compiler', logging.INFO, RegexCompare('\\[Compiling\\].+test_template\\.conf.+compiled_result"')), ('astrality.actions', logging.INFO, 'Running command "echo saturday".'), ('astrality.utils', logging.INFO, 'saturday')]
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.record_tuples\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_running_module_on_event_command(self, single_module_manager, module, caplog):
        single_module_manager.startup()
        caplog.clear()
        single_module_manager.execute(action='run',
          block='on_event',
          module=(single_module_manager.modules['test_module']))
        compiled_template = list(single_module_manager.modules['test_module'].performed_compilations().values())[0].pop()
        for log_event in [
         (
          'astrality.actions',
          logging.INFO,
          f'Running command "echo {compiled_template}".'),
         (
          'astrality.utils',
          logging.INFO,
          (f"{compiled_template}"))]:
            @py_assert3 = caplog.record_tuples
            @py_assert1 = log_event in @py_assert3
            if not @py_assert1:
                @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s.record_tuples\n}', ), (log_event, @py_assert3)) % {'py0':@pytest_ar._saferepr(log_event) if 'log_event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log_event) else 'log_event',  'py2':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert1 = @py_assert3 = None

    def test_running_module_exit_command(self, single_module_manager, caplog):
        single_module_manager.exit()
        for log_event in [
         (
          'astrality.actions',
          logging.INFO,
          'Running command "echo exit".'),
         (
          'astrality.utils',
          logging.INFO,
          'exit')]:
            @py_assert3 = caplog.record_tuples
            @py_assert1 = log_event in @py_assert3
            if not @py_assert1:
                @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s.record_tuples\n}', ), (log_event, @py_assert3)) % {'py0':@pytest_ar._saferepr(log_event) if 'log_event' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log_event) else 'log_event',  'py2':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert1 = @py_assert3 = None

    def test_missing_template_file(self, caplog):
        modules = {'test_module': {'on_startup': {'compile': [
                                                    {'content': '/not/existing'}]}}}
        module_manager = ModuleManager(modules=modules)
        caplog.clear()
        module_manager.finish_tasks()
        @py_assert0 = 'Could not compile template "/not/existing" to target "'
        @py_assert3 = caplog.record_tuples[0][2]
        @py_assert2 = @py_assert0 in @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_compilation_of_template(self, valid_module_section, simple_application_config, module, conf, caplog):
        valid_module_section['test_module']['event_listener']['type'] = 'solar'
        compiled_template_content = 'some text\n' + os.environ['USER'] + '\nFuraMono Nerd Font'
        module_manager = ModuleManager(config=simple_application_config,
          modules=valid_module_section,
          context=(Context({'fonts': {1: 'FuraMono Nerd Font'}})))
        directory = module_manager.config_directory
        caplog.clear()
        module_manager.execute(action='compile', block='on_startup')
        template_file = str((directory / '../templates/test_template.conf').resolve())
        compiled_template = str(list(module_manager.modules['test_module'].performed_compilations()[Path(template_file)])[0])
        with open('/tmp/compiled_result', 'r') as (file):
            compiled_result = file.read()
        @py_assert1 = compiled_template_content == compiled_result
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (compiled_template_content, compiled_result)) % {'py0':@pytest_ar._saferepr(compiled_template_content) if 'compiled_template_content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compiled_template_content) else 'compiled_template_content',  'py2':@pytest_ar._saferepr(compiled_result) if 'compiled_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compiled_result) else 'compiled_result'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert0 = ('astrality.compiler', logging.INFO, f'[Compiling] Template: "{template_file}" -> Target: "{compiled_template}"')
        @py_assert4 = caplog.record_tuples
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.record_tuples\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None


def test_running_finished_tasks_command(simple_application_config, valid_module_section, freezer, caplog):
    """Test that every task is finished at first finish_tasks() invocation."""
    thursday = datetime(year=2018,
      month=2,
      day=15,
      hour=12)
    freezer.move_to(thursday)
    module_manager = ModuleManager(simple_application_config,
      modules=valid_module_section,
      context=(Context({'fonts': {1: 'FuraMono Nerd Font'}})))
    caplog.clear()
    module_manager.finish_tasks()
    @py_assert1 = caplog.record_tuples
    @py_assert4 = [
     (
      'astrality.compiler', logging.INFO, RegexCompare('\\[Compiling\\] Template: ".+/templates/test_template.conf" -> Target: ".*compiled_result"')), ('astrality.actions', logging.INFO, 'Running command "echo thursday".'), ('astrality.utils', logging.INFO, 'thursday')]
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.record_tuples\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    caplog.clear()
    friday = datetime(year=2018,
      month=2,
      day=16,
      hour=12)
    freezer.move_to(friday)
    module_manager.finish_tasks()
    @py_assert1 = caplog.record_tuples
    @py_assert4 = [
     (
      'astrality.module', logging.INFO, '[module/test_module] New event "friday". Executing actions.'), ('astrality.actions', logging.INFO, RegexCompare('Running command "echo .+compiled_result"\\.')), ('astrality.utils', logging.INFO, RegexCompare('.+compiled_result'))]
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.record_tuples\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_has_unfinished_tasks(simple_application_config, valid_module_section, freezer):
    midday = datetime.now().replace(hour=12, minute=0)
    freezer.move_to(midday)
    weekday_module = ModuleManager(config=simple_application_config,
      modules=valid_module_section,
      context=(Context({'fonts': {1: 'FuraMono Nerd Font'}})))
    @py_assert1 = weekday_module.has_unfinished_tasks
    @py_assert3 = @py_assert1()
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.has_unfinished_tasks\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(weekday_module) if 'weekday_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weekday_module) else 'weekday_module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    weekday_module.finish_tasks()
    @py_assert1 = weekday_module.has_unfinished_tasks
    @py_assert3 = @py_assert1()
    @py_assert6 = False
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.has_unfinished_tasks\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(weekday_module) if 'weekday_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weekday_module) else 'weekday_module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    before_midnight = datetime.now().replace(hour=23, minute=59)
    freezer.move_to(before_midnight)
    @py_assert1 = weekday_module.has_unfinished_tasks
    @py_assert3 = @py_assert1()
    @py_assert6 = False
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.has_unfinished_tasks\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(weekday_module) if 'weekday_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weekday_module) else 'weekday_module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    two_minutes = timedelta(minutes=2)
    freezer.move_to(before_midnight + two_minutes)
    @py_assert1 = weekday_module.has_unfinished_tasks
    @py_assert3 = @py_assert1()
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.has_unfinished_tasks\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(weekday_module) if 'weekday_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weekday_module) else 'weekday_module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    weekday_module.finish_tasks()
    @py_assert1 = weekday_module.has_unfinished_tasks
    @py_assert3 = @py_assert1()
    @py_assert6 = False
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.has_unfinished_tasks\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(weekday_module) if 'weekday_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weekday_module) else 'weekday_module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


@pytest.fixture
def config_with_modules():
    context = Context()
    modules = {'solar_module':{'enabled':True, 
      'event_listener':{'type':'solar', 
       'longitude':0, 
       'latitude':0, 
       'elevation':0}, 
      'templates':{'template_name': {'content':'astrality/tests/templates/test_template.conf', 
                         'target':'/tmp/compiled_result'}}, 
      'on_startup':{'run': [{'shell': 'echo solar compiling {template_name}'}]}, 
      'on_event':{'run': [{'shell': 'echo solar {event}'}]}, 
      'on_exit':{'run': [{'shell': 'echo solar exit'}]}}, 
     'weekday_module':{'enabled':True, 
      'event_listener':{'type': 'weekday'}, 
      'on_startup':{'run': [{'shell': 'echo weekday startup'}]}, 
      'on_event':{'run': [{'shell': 'echo weekday {event}'}]}, 
      'on_exit':{'run': [{'shell': 'echo weekday exit'}]}}, 
     'disabled_module':{'enabled':False, 
      'event_listener':'static'}}
    return (
     modules, context)


@pytest.fixture
def module_manager(config_with_modules):
    modules, context = config_with_modules
    return ModuleManager(modules=modules, context=context)


def test_import_sections_on_event(config_with_modules, freezer):
    modules, context = config_with_modules
    modules['weekday_module']['on_event']['import_context'] = [
     {'to_section':'week', 
      'from_path':'astrality/tests/templates/weekday.yml', 
      'from_section':'{event}'}]
    modules.pop('solar_module')
    module_manager = ModuleManager(modules=modules,
      context=(Context({'fonts': {1: 'FuraCode Nerd Font'}})),
      directory=(Path(__file__).parents[3]))
    @py_assert0 = module_manager.application_context['fonts']
    @py_assert4 = {1: 'FuraCode Nerd Font'}
    @py_assert6 = Context(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(Context) if 'Context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Context) else 'Context',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    sunday = datetime(year=2018, month=2, day=4)
    freezer.move_to(sunday)
    module_manager.finish_tasks()
    @py_assert1 = module_manager.application_context
    @py_assert5 = {'fonts': Context({1: 'FuraCode Nerd Font'})}
    @py_assert7 = Context(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.application_context\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(Context) if 'Context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Context) else 'Context',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    monday = datetime(year=2018, month=2, day=5)
    freezer.move_to(monday)
    module_manager.finish_tasks()
    @py_assert1 = module_manager.application_context
    @py_assert4 = {'fonts':Context({1: 'FuraCode Nerd Font'}), 
     'week':Context({'day': 'monday'})}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.application_context\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_import_sections_on_startup(config_with_modules, freezer):
    modules, context = config_with_modules
    modules['weekday_module']['on_startup']['import_context'] = [
     {'to_section':'start_day', 
      'from_path':'astrality/tests/templates/weekday.yml', 
      'from_section':'{event}'}]
    modules['weekday_module']['on_event']['import_context'] = [
     {'to_section':'day_now', 
      'from_path':'astrality/tests/templates/weekday.yml', 
      'from_section':'{event}'}]
    modules.pop('solar_module')
    module_manager = ModuleManager(modules=modules,
      context=(Context({'fonts': {1: 'FuraCode Nerd Font'}})),
      directory=(Path(__file__).parents[3]))
    @py_assert0 = module_manager.application_context['fonts']
    @py_assert3 = {1: 'FuraCode Nerd Font'}
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    sunday = datetime(year=2018, month=2, day=4)
    freezer.move_to(sunday)
    module_manager.finish_tasks()
    @py_assert1 = module_manager.application_context
    @py_assert4 = {'fonts':Context({1: 'FuraCode Nerd Font'}), 
     'start_day':Context({'day': 'sunday'})}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.application_context\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    monday = datetime(year=2018, month=2, day=5)
    freezer.move_to(monday)
    module_manager.finish_tasks()
    @py_assert1 = module_manager.application_context
    @py_assert4 = {'fonts':Context({1: 'FuraCode Nerd Font'}), 
     'start_day':Context({'day': 'sunday'}),  'day_now':Context({'day': 'monday'})}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.application_context\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


class TestModuleManager:

    @pytest.mark.slow
    def test_invocation_of_module_manager_with_config(self, conf):
        ModuleManager(conf)

    @pytest.mark.slow
    def test_using_finish_tasks_on_example_configuration(self, conf, modules, context):
        module_manager = ModuleManager(config=conf,
          modules=modules,
          context=context)
        module_manager.finish_tasks()

    def test_number_of_modules_instanziated_by_module_manager(self, module_manager):
        @py_assert2 = len(module_manager)
        @py_assert5 = 2
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None


def test_time_until_next_event_of_several_modules(config_with_modules, module_manager, freezer):
    modules, context = config_with_modules
    solar_event_listener = event_listener.Solar(modules)
    noon = solar_event_listener.location.sun()['noon']
    one_minute = timedelta(minutes=1)
    freezer.move_to(noon - one_minute)
    @py_assert1 = module_manager.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == one_minute
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n} == %(py6)s', ), (@py_assert3, one_minute)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(one_minute) if 'one_minute' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one_minute) else 'one_minute'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    two_minutes_before_midnight = datetime.now().replace(hour=23, minute=58)
    freezer.move_to(two_minutes_before_midnight)
    @py_assert1 = module_manager.time_until_next_event
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.total_seconds
    @py_assert7 = @py_assert5()
    @py_assert11 = 2
    @py_assert13 = timedelta(minutes=@py_assert11)
    @py_assert15 = @py_assert13.total_seconds
    @py_assert17 = @py_assert15()
    @py_assert9 = @py_assert7 == @py_assert17
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.time_until_next_event\n}()\n}.total_seconds\n}()\n} == %(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py10)s(minutes=%(py12)s)\n}.total_seconds\n}()\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(timedelta) if 'timedelta' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timedelta) else 'timedelta',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None


def test_detection_of_new_event_involving_several_modules(config_with_modules, freezer):
    modules, context = config_with_modules
    solar_event_listener = event_listener.Solar(modules)
    noon = solar_event_listener.location.sun()['noon']
    one_minute = timedelta(minutes=1)
    freezer.move_to(noon - one_minute)
    module_manager = ModuleManager(modules=modules,
      context=context)
    @py_assert1 = module_manager.has_unfinished_tasks
    @py_assert3 = @py_assert1()
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.has_unfinished_tasks\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    module_manager.finish_tasks()
    @py_assert1 = module_manager.has_unfinished_tasks
    @py_assert3 = @py_assert1()
    @py_assert6 = False
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.has_unfinished_tasks\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    freezer.move_to(noon + one_minute)
    @py_assert1 = module_manager.has_unfinished_tasks
    @py_assert3 = @py_assert1()
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.has_unfinished_tasks\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    module_manager.finish_tasks()
    @py_assert1 = module_manager.has_unfinished_tasks
    @py_assert3 = @py_assert1()
    @py_assert6 = False
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.has_unfinished_tasks\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    two_days = timedelta(days=2)
    freezer.move_to(noon + two_days)
    @py_assert1 = module_manager.has_unfinished_tasks
    @py_assert3 = @py_assert1()
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.has_unfinished_tasks\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_that_shell_filter_is_run_from_config_directory(test_config_directory):
    shell_filter_template = Path(__file__).parents[1] / 'templates' / 'shell_filter_working_directory.template'
    shell_filter_template_target = Path('/tmp/astrality/shell_filter_working_directory.template')
    modules = {'A': {'on_startup': {'compile': [
                                      {'content':str(shell_filter_template), 
                                       'target':str(shell_filter_template_target)}]}}}
    module_manager = ModuleManager(modules=modules)
    module_manager.execute(action='compile', block='on_startup')
    with open(shell_filter_template_target) as (compiled):
        @py_assert1 = compiled.read
        @py_assert3 = @py_assert1()
        @py_assert8 = str(test_config_directory)
        @py_assert5 = @py_assert3 == @py_assert8
        if not @py_assert5:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py9)s\n{%(py9)s = %(py6)s(%(py7)s)\n}', ), (@py_assert3, @py_assert8)) % {'py0':@pytest_ar._saferepr(compiled) if 'compiled' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compiled) else 'compiled',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py7':@pytest_ar._saferepr(test_config_directory) if 'test_config_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_config_directory) else 'test_config_directory',  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = None
    os.remove(shell_filter_template_target)


@pytest.yield_fixture
def two_test_file_paths():
    test_file1 = Path('/tmp/astrality/test_file_1')
    test_file2 = Path('/tmp/astrality/test_file_2')
    yield (
     test_file1, test_file2)
    if test_file1.is_file():
        os.remove(test_file1)
    if test_file2.is_file():
        os.remove(test_file2)


def test_that_only_startup_event_block_is_run_on_startup(two_test_file_paths, test_config_directory, freezer):
    thursday = datetime(year=2018,
      month=2,
      day=15,
      hour=12)
    freezer.move_to(thursday)
    test_file1, test_file2 = two_test_file_paths
    modules = {'A': {'event_listener':{'type': 'weekday'}, 
           'on_startup':{'run': [{'shell': 'touch ' + str(test_file1)}]}, 
           'on_event':{'run': [{'shell': 'touch ' + str(test_file2)}]}}}
    module_manager = ModuleManager(modules=modules)
    @py_assert1 = []
    @py_assert3 = test_file1.is_file
    @py_assert5 = @py_assert3()
    @py_assert7 = not @py_assert5
    @py_assert0 = @py_assert7
    if @py_assert7:
        @py_assert10 = test_file2.is_file
        @py_assert12 = @py_assert10()
        @py_assert14 = not @py_assert12
        @py_assert0 = @py_assert14
    if not @py_assert0:
        @py_format8 = 'not %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.is_file\n}()\n}' % {'py2':@pytest_ar._saferepr(test_file1) if 'test_file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_file1) else 'test_file1',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_assert1.append(@py_format8)
        if @py_assert7:
            @py_format15 = 'not %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s.is_file\n}()\n}' % {'py9':@pytest_ar._saferepr(test_file2) if 'test_file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_file2) else 'test_file2',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
            @py_assert1.append(@py_format15)
        @py_format16 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert0 = @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert14 = None
    module_manager.finish_tasks()
    retry = Retry()
    @py_assert1 = lambda : test_file1.is_file()
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = lambda : not test_file2.is_file()
    @py_assert3 = retry(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_trigger_event_module_action(test_config_directory):
    modules = {'A': {'event_listener':{'type': 'weekday'}, 
           'on_startup':{'trigger':[
             {'block': 'on_event'},
             {'block': 'on_exit'},
             {'block':'on_modified', 
              'path':'templateA'}], 
            'run':[
             {'shell': 'echo startup'}]}, 
           'on_event':{'run':[
             {'shell': 'echo on_event'}], 
            'import_context':[
             {'from_path':'context/mercedes.yml', 
              'from_section':'car'}]}, 
           'on_exit':{'run': [{'shell': 'echo exit'}]}, 
           'on_modified':{'templateA': {'run':[
                           {'shell': 'echo modified.templateA'}], 
                          'compile':[
                           {'content': 'templateA'}]}}}}
    module_manager = ModuleManager(config={'modules': {'enabled_modules': [{'name': 'A'}]}},
      modules=modules)
    results = tuple(module_manager.modules['A'].execute(action='run',
      block='on_startup'))
    @py_assert2 = (('echo startup', 'startup'), ('echo on_event', 'on_event'), ('echo exit', 'exit'),
                   ('echo modified.templateA', 'modified.templateA'))
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    module_manager.modules['A'].execute(action='import_context',
      block='on_startup')
    @py_assert0 = module_manager.application_context['car']
    @py_assert3 = {'manufacturer': 'Mercedes'}
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    results = module_manager.modules['A'].execute(action='run',
      block='on_event')
    @py_assert2 = (('echo on_event', 'on_event'), )
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    results = module_manager.modules['A'].execute(action='run',
      block='on_exit')
    @py_assert2 = (('echo exit', 'exit'), )
    @py_assert1 = results == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (results, @py_assert2)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    module_manager.modules['A'].execute(action='import_context',
      block='on_event')
    @py_assert0 = module_manager.application_context['car']
    @py_assert3 = {'manufacturer': 'Mercedes'}
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_not_using_list_when_specifiying_trigger_action(conf_path):
    modules = {'A': {'on_startup':{'trigger': {'block': 'on_event'}}, 
           'on_event':{'run': [{'shell': 'echo on_event'}]}}}
    module_manager = ModuleManager(modules=modules,
      directory=conf_path)
    result = module_manager.modules['A'].execute(action='run',
      block='on_startup')
    @py_assert2 = (('echo on_event', 'on_event'), )
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_defining_on_startup_block_at_root_indentation(caplog):
    """Root indentation actions should be promoted to on_startup."""
    module_config = {'on_startup': {'run': [{'shell': 'echo on_startup'}]}}
    @py_assert1 = Module.prepare_on_startup_block
    @py_assert3 = 'test'
    @py_assert6 = @py_assert1(module_name=@py_assert3, module_config=module_config)
    @py_assert9 = {'on_startup': {'run': [{'shell': 'echo on_startup'}]}}
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.prepare_on_startup_block\n}(module_name=%(py4)s, module_config=%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(Module) if 'Module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Module) else 'Module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(module_config) if 'module_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_config) else 'module_config',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None
    module_config = {'run':[
      {'shell': 'touch stuff'}], 
     'compile':{'source': 'some/path'}}
    @py_assert1 = Module.prepare_on_startup_block
    @py_assert3 = 'test'
    @py_assert6 = @py_assert1(module_name=@py_assert3, module_config=module_config)
    @py_assert9 = {'on_startup': {'run':[{'shell': 'touch stuff'}],  'compile':{'source': 'some/path'}}}
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.prepare_on_startup_block\n}(module_name=%(py4)s, module_config=%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(Module) if 'Module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Module) else 'Module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(module_config) if 'module_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_config) else 'module_config',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None
    caplog.clear()
    module_config = {'run':[
      {'shell': 'echo overwritten'}], 
     'on_startup':{'run': [{'shell': 'echo original'}]}}
    @py_assert1 = Module.prepare_on_startup_block
    @py_assert3 = 'test'
    @py_assert6 = @py_assert1(module_name=@py_assert3, module_config=module_config)
    @py_assert9 = {'on_startup': {'run': [{'shell': 'echo overwritten'}]}}
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.prepare_on_startup_block\n}(module_name=%(py4)s, module_config=%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(Module) if 'Module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Module) else 'Module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(module_config) if 'module_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_config) else 'module_config',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert0 = caplog.record_tuples[0][1]
    @py_assert4 = logging.ERROR
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.ERROR\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(logging) if 'logging' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(logging) else 'logging',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    module_config = {'stow':[
      {'content': 'new_stow'}], 
     'copy':{'content': 'new_copy'}, 
     'on_startup':{'run':[
       {'shell': 'run'}], 
      'stow':{'content': 'old_stow'}, 
      'copy':{'content': 'old_copy'}}, 
     'on_exit':{}}
    @py_assert1 = Module.prepare_on_startup_block
    @py_assert3 = 'test'
    @py_assert6 = @py_assert1(module_name=@py_assert3, module_config=module_config)
    @py_assert9 = {'on_startup':{'run':[
       {'shell': 'run'}], 
      'stow':[{'content': 'new_stow'}],  'copy':{'content': 'new_copy'}}, 
     'on_exit':{}}
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.prepare_on_startup_block\n}(module_name=%(py4)s, module_config=%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(Module) if 'Module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Module) else 'Module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(module_config) if 'module_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_config) else 'module_config',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None
    module_config = {'run':[
      {'shell': 'echo overwritten'}], 
     'on_startup':{'run': [{'shell': 'echo original'}]}}
    module = Module(name='test_module',
      module_config=module_config,
      module_directory=(Path('/')))
    @py_assert1 = module.execute
    @py_assert3 = 'run'
    @py_assert5 = 'on_startup'
    @py_assert7 = @py_assert1(action=@py_assert3, block=@py_assert5)
    @py_assert10 = (('echo overwritten', 'overwritten'), )
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.execute\n}(action=%(py4)s, block=%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(module) if 'module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module) else 'module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None