# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/test_xdg.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 1982 bytes
"""Tests for astrality.xdg module."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from pathlib import Path
import pytest
from astrality.xdg import XDG

@pytest.mark.dont_patch_xdg
def test_xdg_data_home_default_location(monkeypatch):
    """Default location for XDG_DATA_HOME should be respected."""
    xdg = XDG()
    default_dir = xdg.data_home
    @py_assert3 = '~/.local/share/astrality'
    @py_assert5 = Path(@py_assert3)
    @py_assert7 = @py_assert5.expanduser
    @py_assert9 = @py_assert7()
    @py_assert1 = default_dir == @py_assert9
    if not @py_assert1:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n}.expanduser\n}()\n}', ), (default_dir, @py_assert9)) % {'py0':@pytest_ar._saferepr(default_dir) if 'default_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_dir) else 'default_dir',  'py2':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = default_dir.is_dir
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(default_dir) if 'default_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(default_dir) else 'default_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


@pytest.mark.dont_patch_xdg
def test_xdg_data_home_using_environment_variable(monkeypatch, tmpdir):
    """XDG_DATA_HOME environment variables should be respected."""
    custom_data_home = Path(tmpdir, 'data')
    monkeypatch.setattr(os, 'environ', {'XDG_DATA_HOME': str(custom_data_home)})
    xdg = XDG()
    data_home = xdg.data_home
    @py_assert3 = 'astrality'
    @py_assert5 = custom_data_home / @py_assert3
    @py_assert1 = data_home == @py_assert5
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == (%(py2)s / %(py4)s)', ), (data_home, @py_assert5)) % {'py0':@pytest_ar._saferepr(data_home) if 'data_home' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data_home) else 'data_home',  'py2':@pytest_ar._saferepr(custom_data_home) if 'custom_data_home' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(custom_data_home) else 'custom_data_home',  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = data_home.is_dir
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(data_home) if 'data_home' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data_home) else 'data_home',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_retrieving_data_resource(patch_xdg_directory_standard):
    """The data method should retrieve file resource from data home."""
    xdg = XDG()
    resource = xdg.data('modules/test.tmp')
    @py_assert3 = 'modules'
    @py_assert5 = patch_xdg_directory_standard / @py_assert3
    @py_assert6 = 'test.tmp'
    @py_assert8 = @py_assert5 / @py_assert6
    @py_assert1 = resource == @py_assert8
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == ((%(py2)s / %(py4)s) / %(py7)s)', ), (resource, @py_assert8)) % {'py0':@pytest_ar._saferepr(resource) if 'resource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resource) else 'resource',  'py2':@pytest_ar._saferepr(patch_xdg_directory_standard) if 'patch_xdg_directory_standard' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(patch_xdg_directory_standard) else 'patch_xdg_directory_standard',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = None
    @py_assert1 = resource.exists
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(resource) if 'resource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resource) else 'resource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    resource.write_text('hello')
    refetched_resource = xdg.data('modules/test.tmp')
    @py_assert1 = refetched_resource.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'hello'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(refetched_resource) if 'refetched_resource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(refetched_resource) else 'refetched_resource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_retrieving_data_directory_resource(patch_xdg_directory_standard):
    """The data method should also be able to retrieve directories."""
    xdg = XDG()
    resource = xdg.data(resource='repositories/github',
      directory=True)
    @py_assert3 = 'repositories'
    @py_assert5 = patch_xdg_directory_standard / @py_assert3
    @py_assert6 = 'github'
    @py_assert8 = @py_assert5 / @py_assert6
    @py_assert1 = resource == @py_assert8
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == ((%(py2)s / %(py4)s) / %(py7)s)', ), (resource, @py_assert8)) % {'py0':@pytest_ar._saferepr(resource) if 'resource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resource) else 'resource',  'py2':@pytest_ar._saferepr(patch_xdg_directory_standard) if 'patch_xdg_directory_standard' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(patch_xdg_directory_standard) else 'patch_xdg_directory_standard',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = None
    @py_assert1 = resource.is_dir
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(resource) if 'resource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resource) else 'resource',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    resource_file = resource / 'file'
    resource_file.touch()
    resource = xdg.data(resource='repositories/github',
      directory=True)
    @py_assert1 = resource_file.exists
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(resource_file) if 'resource_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resource_file) else 'resource_file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None