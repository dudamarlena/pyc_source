# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_module_requires.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 2696 bytes
"""Tests for module requirements."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, logging
from pathlib import Path
from astrality.module import Module, ModuleManager
from astrality.tests.utils import RegexCompare

def test_module_requires_option(caplog):
    """Test that modules are disabled when they don't satisfy `requires`."""
    does_satisfy_requiremnets = {'enabled':True, 
     'requires':{'shell': 'command -v cd'}}
    @py_assert1 = Module.valid_module
    @py_assert3 = 'satisfies'
    @py_assert6 = 1
    @py_assert9 = '/'
    @py_assert11 = Path(@py_assert9)
    @py_assert13 = @py_assert1(name=@py_assert3, config=does_satisfy_requiremnets, requires_timeout=@py_assert6, requires_working_directory=@py_assert11)
    if not @py_assert13:
        @py_format15 = ('' + 'assert %(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.valid_module\n}(name=%(py4)s, config=%(py5)s, requires_timeout=%(py7)s, requires_working_directory=%(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n})\n}') % {'py0':@pytest_ar._saferepr(Module) if 'Module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Module) else 'Module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(does_satisfy_requiremnets) if 'does_satisfy_requiremnets' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(does_satisfy_requiremnets) else 'does_satisfy_requiremnets',  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = None
    does_not_satisfy_requirements = {'requires': {'shell': 'command -v does_not_exist'}}
    @py_assert1 = Module.valid_module
    @py_assert3 = 'does_not_satisfy'
    @py_assert6 = 1
    @py_assert9 = '/'
    @py_assert11 = Path(@py_assert9)
    @py_assert13 = @py_assert1(name=@py_assert3, config=does_not_satisfy_requirements, requires_timeout=@py_assert6, requires_working_directory=@py_assert11)
    @py_assert15 = not @py_assert13
    if not @py_assert15:
        @py_format16 = ('' + 'assert not %(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.valid_module\n}(name=%(py4)s, config=%(py5)s, requires_timeout=%(py7)s, requires_working_directory=%(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n})\n}') % {'py0':@pytest_ar._saferepr(Module) if 'Module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Module) else 'Module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(does_not_satisfy_requirements) if 'does_not_satisfy_requirements' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(does_not_satisfy_requirements) else 'does_not_satisfy_requirements',  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert0 = (
     'astrality.module', logging.WARNING, '[module/does_not_satisfy] Module requirements: Unsuccessful command: "command -v does_not_exist", !')
    @py_assert4 = caplog.record_tuples
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.record_tuples\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    does_not_satisfy_one_requirement = {'requires': [
                  {'shell': 'command -v cd'},
                  {'shell': 'command -v does_not_exist'}]}
    caplog.clear()
    @py_assert1 = Module.valid_module
    @py_assert3 = 'does_not_satisfy'
    @py_assert6 = 1
    @py_assert9 = '/'
    @py_assert11 = Path(@py_assert9)
    @py_assert13 = @py_assert1(name=@py_assert3, config=does_not_satisfy_one_requirement, requires_timeout=@py_assert6, requires_working_directory=@py_assert11)
    @py_assert15 = not @py_assert13
    if not @py_assert15:
        @py_format16 = ('' + 'assert not %(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.valid_module\n}(name=%(py4)s, config=%(py5)s, requires_timeout=%(py7)s, requires_working_directory=%(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n})\n}') % {'py0':@pytest_ar._saferepr(Module) if 'Module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Module) else 'Module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(does_not_satisfy_one_requirement) if 'does_not_satisfy_one_requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(does_not_satisfy_one_requirement) else 'does_not_satisfy_one_requirement',  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert0 = (
     'astrality.module', logging.WARNING, RegexCompare('\\[module/does_not_satisfy\\] Module requirements: .+ Unsuccessful command: "command -v does_not_exist", !'))
    @py_assert4 = caplog.record_tuples
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.record_tuples\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_module_module_dependencies():
    """ModuleManager should remove modules with missing module dependencies."""
    config = {'modules': {'modules_directory':'freezed_modules', 
                 'enabled_modules':[
                  {'name': 'north_america::*'},
                  {'name': 'A'},
                  {'name': 'B'},
                  {'name': 'C'}]}}
    modules = {'A':{'requires': {'module': 'north_america::USA'}}, 
     'B':{'requires': [{'module': 'A'}]}, 
     'C':{'requires': [{'module': 'D'}]}}
    module_manager = ModuleManager(config=config,
      modules=modules)
    @py_assert2 = module_manager.modules
    @py_assert4 = @py_assert2.keys
    @py_assert6 = @py_assert4()
    @py_assert8 = sorted(@py_assert6)
    @py_assert12 = [
     'A', 'B', 'north_america::USA']
    @py_assert14 = sorted(@py_assert12)
    @py_assert10 = @py_assert8 == @py_assert14
    if not @py_assert10:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.modules\n}.keys\n}()\n})\n} == %(py15)s\n{%(py15)s = %(py11)s(%(py13)s)\n}', ), (@py_assert8, @py_assert14)) % {'py0':@pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py1':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None