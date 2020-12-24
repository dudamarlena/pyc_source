# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/config/test_expand_path.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 1922 bytes
"""Tests for astrality.config.expand_path."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.config import expand_globbed_path, expand_path

def test_expand_path_method(test_config_directory):
    absolute_path = Path('/dir/ast')
    tilde_path = Path('~/dir')
    relative_path = Path('test')
    @py_assert3 = '/what/ever'
    @py_assert5 = Path(@py_assert3)
    @py_assert7 = expand_path(path=absolute_path, config_directory=@py_assert5)
    @py_assert9 = @py_assert7 == absolute_path
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(path=%(py1)s, config_directory=%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n})\n} == %(py10)s', ), (@py_assert7, absolute_path)) % {'py0':@pytest_ar._saferepr(expand_path) if 'expand_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expand_path) else 'expand_path',  'py1':@pytest_ar._saferepr(absolute_path) if 'absolute_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(absolute_path) else 'absolute_path',  'py2':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(absolute_path) if 'absolute_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(absolute_path) else 'absolute_path'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert3 = '/what/ever'
    @py_assert5 = Path(@py_assert3)
    @py_assert7 = expand_path(path=tilde_path, config_directory=@py_assert5)
    @py_assert11 = Path.home
    @py_assert13 = @py_assert11()
    @py_assert15 = 'dir'
    @py_assert17 = @py_assert13 / @py_assert15
    @py_assert9 = @py_assert7 == @py_assert17
    if not @py_assert9:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(path=%(py1)s, config_directory=%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n})\n} == (%(py14)s\n{%(py14)s = %(py12)s\n{%(py12)s = %(py10)s.home\n}()\n} / %(py16)s)', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(expand_path) if 'expand_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expand_path) else 'expand_path',  'py1':@pytest_ar._saferepr(tilde_path) if 'tilde_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tilde_path) else 'tilde_path',  'py2':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert3 = expand_path(path=relative_path, config_directory=test_config_directory)
    @py_assert7 = 'test'
    @py_assert9 = test_config_directory / @py_assert7
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(path=%(py1)s, config_directory=%(py2)s)\n} == (%(py6)s / %(py8)s)', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(expand_path) if 'expand_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expand_path) else 'expand_path',  'py1':@pytest_ar._saferepr(relative_path) if 'relative_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(relative_path) else 'relative_path',  'py2':@pytest_ar._saferepr(test_config_directory) if 'test_config_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_config_directory) else 'test_config_directory',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(test_config_directory) if 'test_config_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_config_directory) else 'test_config_directory',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_expansion_of_environment_variables(test_config_directory):
    """
    Environment variables should be expanded in paths.

    See pytest.ini for available environment variables.
    """
    @py_assert2 = '${EXAMPLE_ENV_VARIABLE}/recursive'
    @py_assert4 = Path(@py_assert2)
    @py_assert7 = '$EXAMPLE_ENV_VARIABLE'
    @py_assert9 = test_config_directory / @py_assert7
    @py_assert10 = expand_path(path=@py_assert4, config_directory=@py_assert9)
    @py_assert14 = 'test_value'
    @py_assert16 = test_config_directory / @py_assert14
    @py_assert17 = 'test_value'
    @py_assert19 = @py_assert16 / @py_assert17
    @py_assert20 = 'recursive'
    @py_assert22 = @py_assert19 / @py_assert20
    @py_assert12 = @py_assert10 == @py_assert22
    if not @py_assert12:
        @py_format23 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(path=%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, config_directory=(%(py6)s / %(py8)s))\n} == (((%(py13)s / %(py15)s) / %(py18)s) / %(py21)s)', ), (@py_assert10, @py_assert22)) % {'py0':@pytest_ar._saferepr(expand_path) if 'expand_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expand_path) else 'expand_path',  'py1':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(test_config_directory) if 'test_config_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_config_directory) else 'test_config_directory',  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(test_config_directory) if 'test_config_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_config_directory) else 'test_config_directory',  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17),  'py21':@pytest_ar._saferepr(@py_assert20)}
        @py_format25 = 'assert %(py24)s' % {'py24': @py_format23}
        raise AssertionError(@pytest_ar._format_explanation(@py_format25))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = @py_assert19 = @py_assert20 = @py_assert22 = None


def test_expand_globbed_path(test_config_directory):
    """Globbed paths should allow one level of globbing."""
    templates = Path('test_modules', 'using_all_actions')
    paths = expand_globbed_path(path=(templates / '*'),
      config_directory=test_config_directory)
    @py_assert2 = len(paths)
    @py_assert5 = 5
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(paths) if 'paths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paths) else 'paths',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = test_config_directory / templates
    @py_assert3 = 'module.template'
    @py_assert5 = @py_assert2 / @py_assert3
    @py_assert6 = @py_assert5 in paths
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert6,), ('((%(py0)s / %(py1)s) / %(py4)s) in %(py7)s', ), (@py_assert5, paths)) % {'py0':@pytest_ar._saferepr(test_config_directory) if 'test_config_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_config_directory) else 'test_config_directory',  'py1':@pytest_ar._saferepr(templates) if 'templates' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(templates) else 'templates',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(paths) if 'paths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paths) else 'paths'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_expand_recursive_globbed_path(test_config_directory):
    """Globbed paths should allow recursive globbing."""
    templates = Path('test_modules', 'using_all_actions')
    paths = expand_globbed_path(path=(templates / '**' / '*'),
      config_directory=test_config_directory)
    @py_assert2 = len(paths)
    @py_assert5 = 6
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(paths) if 'paths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paths) else 'paths',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = test_config_directory / templates
    @py_assert3 = 'recursive'
    @py_assert5 = @py_assert2 / @py_assert3
    @py_assert6 = 'empty.template'
    @py_assert8 = @py_assert5 / @py_assert6
    @py_assert9 = @py_assert8 in paths
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('(((%(py0)s / %(py1)s) / %(py4)s) / %(py7)s) in %(py10)s', ), (@py_assert8, paths)) % {'py0':@pytest_ar._saferepr(test_config_directory) if 'test_config_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_config_directory) else 'test_config_directory',  'py1':@pytest_ar._saferepr(templates) if 'templates' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(templates) else 'templates',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(paths) if 'paths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(paths) else 'paths'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = @py_assert9 = None