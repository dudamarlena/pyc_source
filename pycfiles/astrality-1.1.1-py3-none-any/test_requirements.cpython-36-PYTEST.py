# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/test_requirements.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 4600 bytes
"""Tests for requirements module."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.requirements import Requirement
from astrality.module import Module

def test_null_object_pattern():
    """Empty requirements should be considered satisfied."""
    successful_shell_requirement = Requirement(requirements={}, directory=(Path('/')))
    if not successful_shell_requirement:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(successful_shell_requirement) if 'successful_shell_requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(successful_shell_requirement) else 'successful_shell_requirement'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))


def test_shell_command_requirement():
    """Requirement should be truthy when command returns 0 exit code."""
    successful_shell_requirement = Requirement(requirements={'shell': 'command -v ls'},
      directory=(Path('/')))
    if not successful_shell_requirement:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(successful_shell_requirement) if 'successful_shell_requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(successful_shell_requirement) else 'successful_shell_requirement'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    unsuccessful_shell_requirement = Requirement(requirements={'shell': 'command -v does_not_exist'},
      directory=(Path('/')))
    @py_assert1 = not unsuccessful_shell_requirement
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(unsuccessful_shell_requirement) if 'unsuccessful_shell_requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(unsuccessful_shell_requirement) else 'unsuccessful_shell_requirement'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None


def test_that_shell_commands_are_run_in_correct_diretory():
    """All shell commands should be run from 'directory'"""
    successful_shell_requirement = Requirement(requirements={'shell': 'ls tmp'},
      directory=(Path('/')))
    if not successful_shell_requirement:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(successful_shell_requirement) if 'successful_shell_requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(successful_shell_requirement) else 'successful_shell_requirement'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    unsuccessful_shell_requirement = Requirement(requirements={'shell': 'ls does_not_exist'},
      directory=(Path('/')))
    @py_assert1 = not unsuccessful_shell_requirement
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(unsuccessful_shell_requirement) if 'unsuccessful_shell_requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(unsuccessful_shell_requirement) else 'unsuccessful_shell_requirement'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None


def test_shell_command_timeout():
    """Shell commands can time out."""
    default_times_out = Requirement(requirements={'shell': 'sleep 0.1'},
      directory=(Path('/')),
      timeout=0.01)
    @py_assert1 = not default_times_out
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(default_times_out) if 'default_times_out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_times_out) else 'default_times_out'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None
    default_does_not_timeout = Requirement(requirements={'shell': 'sleep 0.1'},
      directory=(Path('/')),
      timeout=0.2)
    if not default_does_not_timeout:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(default_does_not_timeout) if 'default_does_not_timeout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_does_not_timeout) else 'default_does_not_timeout'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    specifed_does_not_timeout = Requirement(requirements={'shell':'sleep 0.1', 
     'timeout':0.2},
      directory=(Path('/')),
      timeout=0.5)
    if not specifed_does_not_timeout:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(specifed_does_not_timeout) if 'specifed_does_not_timeout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(specifed_does_not_timeout) else 'specifed_does_not_timeout'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    specified_does_timeout = Requirement(requirements={'shell':'sleep 0.1', 
     'timeout':0.05},
      directory=(Path('/')),
      timeout=1000)
    @py_assert1 = not specified_does_timeout
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(specified_does_timeout) if 'specified_does_timeout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(specified_does_timeout) else 'specified_does_timeout'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None


def test_environment_variable_requirement():
    """Requirement should be truthy when environment variable is available."""
    successful_env_requirement = Requirement(requirements={'env': 'EXAMPLE_ENV_VARIABLE'},
      directory=(Path('/')))
    if not successful_env_requirement:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(successful_env_requirement) if 'successful_env_requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(successful_env_requirement) else 'successful_env_requirement'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    unsuccessful_env_requirement = Requirement(requirements={'env': 'THIS_IS_NOT_SET'},
      directory=(Path('/')))
    @py_assert1 = not unsuccessful_env_requirement
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(unsuccessful_env_requirement) if 'unsuccessful_env_requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(unsuccessful_env_requirement) else 'unsuccessful_env_requirement'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None


def test_installed_requirement():
    """Requirement should be truthy when value is in $PATH."""
    successful_installed_requirement = Requirement(requirements={'installed': 'ls'},
      directory=(Path('/')))
    if not successful_installed_requirement:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(successful_installed_requirement) if 'successful_installed_requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(successful_installed_requirement) else 'successful_installed_requirement'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    unsuccessful_installed_requirement = Requirement(requirements={'installed': 'does_not_exist'},
      directory=(Path('/')))
    @py_assert1 = not unsuccessful_installed_requirement
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(unsuccessful_installed_requirement) if 'unsuccessful_installed_requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(unsuccessful_installed_requirement) else 'unsuccessful_installed_requirement'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None


def test_requiring_a_global_module():
    """You should be able to require global modules."""
    moduleA = Module(name='A',
      module_config={'requires': [{'module': 'B'}]},
      module_directory=(Path(__file__).parent))
    @py_assert1 = moduleA.depends_on
    @py_assert4 = ('B', )
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.depends_on\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(moduleA) if 'moduleA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(moduleA) else 'moduleA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    moduleB = Module(name='B',
      module_config={'run': {'shell': 'echo hi!'}},
      module_directory=(Path(__file__).parent))
    @py_assert1 = moduleB.depends_on
    @py_assert5 = tuple()
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.depends_on\n} == %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(moduleB) if 'moduleB' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(moduleB) else 'moduleB',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    moduleC = Module(name='C',
      module_config={'requires': [{'module': 'D'}]},
      module_directory=(Path(__file__).parent))
    @py_assert1 = moduleC.depends_on
    @py_assert4 = ('D', )
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.depends_on\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(moduleC) if 'moduleC' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(moduleC) else 'moduleC',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = Requirement.pop_missing_module_dependencies
    @py_assert3 = {'A':moduleA, 
     'B':moduleB,  'C':moduleC}
    @py_assert5 = @py_assert1(modules=@py_assert3)
    @py_assert8 = {'A':moduleA, 
     'B':moduleB}
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.pop_missing_module_dependencies\n}(modules=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(Requirement) if 'Requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Requirement) else 'Requirement',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_recursive_module_requirements():
    """Missing dependencies should propagate."""
    moduleA = Module(name='A',
      module_config={'requires': [{'module': 'B'}]},
      module_directory=(Path(__file__).parent))
    moduleB = Module(name='B',
      module_config={'requires': [{'module': 'C'}]},
      module_directory=(Path(__file__).parent))
    moduleC = Module(name='C',
      module_config={'requires': [{'module': 'D'}]},
      module_directory=(Path(__file__).parent))
    @py_assert1 = Requirement.pop_missing_module_dependencies
    @py_assert3 = {'A':moduleA, 
     'B':moduleB,  'C':moduleC}
    @py_assert5 = @py_assert1(modules=@py_assert3)
    @py_assert8 = {}
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.pop_missing_module_dependencies\n}(modules=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(Requirement) if 'Requirement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Requirement) else 'Requirement',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None