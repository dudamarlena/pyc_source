# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_configuration.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 5276 bytes
"""Tests for configuraition dictionary management."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from astrality.module import GlobalModulesConfig, ModuleManager

def test_modules_config_explicitly_enabled_modules(test_config_directory):
    global_modules_config_dict = {'modules_directory':'test_modules', 
     'enabled_modules':[
      {'name': 'burma::burma'},
      {'name': 'india'}]}
    global_modules_config = GlobalModulesConfig(config=global_modules_config_dict,
      config_directory=test_config_directory)
    for source in global_modules_config.external_module_sources:
        source.modules({})

    @py_assert0 = 'burma::burma'
    @py_assert4 = global_modules_config.enabled_modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.enabled_modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_modules_config) if 'global_modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_modules_config) else 'global_modules_config',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'india'
    @py_assert4 = global_modules_config.enabled_modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.enabled_modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_modules_config) if 'global_modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_modules_config) else 'global_modules_config',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'whatever'
    @py_assert4 = global_modules_config.enabled_modules
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s.enabled_modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_modules_config) if 'global_modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_modules_config) else 'global_modules_config',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_modules_config_implicitly_enabled_modules(test_config_directory):
    global_modules_config_dict = {'modules_directory':'test_modules', 
     'enabled_modules':[
      {'name': 'burma::*'},
      {'name': 'india'}]}
    global_modules_config = GlobalModulesConfig(config=global_modules_config_dict,
      config_directory=test_config_directory)
    for source in global_modules_config.external_module_sources:
        source.modules({})

    @py_assert0 = 'burma::burma'
    @py_assert4 = global_modules_config.enabled_modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.enabled_modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_modules_config) if 'global_modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_modules_config) else 'global_modules_config',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'india'
    @py_assert4 = global_modules_config.enabled_modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.enabled_modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_modules_config) if 'global_modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_modules_config) else 'global_modules_config',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'burma::only_defined_accepted'
    @py_assert4 = global_modules_config.enabled_modules
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s.enabled_modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_modules_config) if 'global_modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_modules_config) else 'global_modules_config',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_modules_config_several_implicitly_enabled_modules(test_config_directory):
    global_modules_config_dict = {'modules_directory':'test_modules', 
     'enabled_modules':[
      {'name': 'two_modules::*'},
      {'name': 'india'}]}
    global_modules_config = GlobalModulesConfig(config=global_modules_config_dict,
      config_directory=test_config_directory)
    for source in global_modules_config.external_module_sources:
        source.modules({})

    @py_assert0 = 'two_modules::bhutan'
    @py_assert4 = global_modules_config.enabled_modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.enabled_modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_modules_config) if 'global_modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_modules_config) else 'global_modules_config',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'two_modules::bangladesh'
    @py_assert4 = global_modules_config.enabled_modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.enabled_modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_modules_config) if 'global_modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_modules_config) else 'global_modules_config',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_modules_config_where_all_modules_are_enabled(test_config_directory):
    global_modules_config_dict = {'modules_directory':str(test_config_directory / 'test_modules'), 
     'enabled_modules':[
      {'name': '*::*'},
      {'name': '*'}]}
    global_modules_config = GlobalModulesConfig(config=global_modules_config_dict,
      config_directory=test_config_directory)
    global_modules_config.compile_config_files({'module': {'setting': 'whatever'}})
    @py_assert0 = 'two_modules::bhutan'
    @py_assert4 = global_modules_config.enabled_modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.enabled_modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_modules_config) if 'global_modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_modules_config) else 'global_modules_config',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'two_modules::bangladesh'
    @py_assert4 = global_modules_config.enabled_modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.enabled_modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(global_modules_config) if 'global_modules_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_modules_config) else 'global_modules_config',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_enabling_of_modules_defined_different_places():
    application_config = {'modules': {'modules_directory':'freezed_modules', 
                 'enabled_modules':[
                  {'name': 'south_america::brazil'},
                  {'name': 'india'}]}}
    modules = {'india':{},  'pakistan':{}}
    module_manager = ModuleManager(config=application_config,
      modules=modules)
    @py_assert2 = module_manager.modules
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 2
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.modules\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = 'south_america::brazil'
    @py_assert4 = module_manager.modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'india'
    @py_assert4 = module_manager.modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_enabling_of_all_modules():
    application_config = {'modules': {'modules_directory': 'freezed_modules'}}
    modules = {'india':{},  'pakistan':{}}
    module_manager = ModuleManager(config=application_config,
      modules=modules)
    @py_assert2 = module_manager.modules
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 5
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.modules\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = 'india'
    @py_assert4 = module_manager.modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'pakistan'
    @py_assert4 = module_manager.modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'north_america::USA'
    @py_assert4 = module_manager.modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'south_america::brazil'
    @py_assert4 = module_manager.modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'south_america::argentina'
    @py_assert4 = module_manager.modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@pytest.mark.slow
def test_using_three_different_module_sources(test_config_directory):
    modules_directory = test_config_directory / 'freezed_modules'
    application_config = {'modules': {'modules_directory':str(modules_directory), 
                 'enabled_modules':[
                  {'name': 'north_america::*'},
                  {'name': 'github::jakobgm/test-module.astrality'},
                  {'name': 'italy'}]}}
    modules = {'italy':{},  'spain':{}}
    module_manager = ModuleManager(config=application_config,
      modules=modules)
    @py_assert2 = module_manager.modules
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 4
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.modules\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = 'north_america::USA'
    @py_assert4 = module_manager.modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'github::jakobgm/test-module.astrality::botswana'
    @py_assert4 = module_manager.modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'github::jakobgm/test-module.astrality::ghana'
    @py_assert4 = module_manager.modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'italy'
    @py_assert4 = module_manager.modules
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.modules\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None