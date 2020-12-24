# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/config/test_config.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 6669 bytes
"""Tests for locating and parsing YAML configuration files."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from pathlib import Path
from shutil import rmtree
import pytest
from astrality.config import ASTRALITY_DEFAULT_GLOBAL_SETTINGS, create_config_directory, infer_config_location, resolve_config_directory, user_configuration
from astrality.context import Context
from astrality.utils import compile_yaml, dump_yaml

@pytest.fixture
def dummy_config():
    """Return dummy configuration YAML file."""
    test_conf = Path(__file__).parents[1] / 'test_config' / 'test.yml'
    return compile_yaml(path=test_conf,
      context=(Context()))


class TestAllConfigFeaturesFromDummyConfig:
    __doc__ = 'Tests for .utils.compile_yaml.'

    def test_normal_variable(self, dummy_config):
        """String literals should be interpreted without modifications."""
        @py_assert0 = dummy_config['section1']['var1']
        @py_assert3 = 'value1'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = dummy_config['section1']['var2']
        @py_assert3 = 'value1/value2'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = dummy_config['section2']['var3']
        @py_assert3 = 'value1'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_empty_string_variable(self, dummy_config):
        """Empty strings  should be representable."""
        @py_assert0 = dummy_config['section2']['empty_string_var']
        @py_assert3 = ''
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_non_existing_variable(self, dummy_config):
        """Non-existing keys should not have defaults but raise instead."""
        with pytest.raises(KeyError):
            @py_assert0 = dummy_config['section2']['not_existing_option']
            @py_assert3 = None
            @py_assert2 = @py_assert0 is @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_environment_variable_interpolation(self, dummy_config):
        """Environment variables should be interpolated with Jinja syntax."""
        @py_assert0 = dummy_config['section3']['env_variable']
        @py_assert3 = 'test_value, hello'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None


class TestResolveConfigDirectory:
    __doc__ = 'Tests for .config.resolve_config_directory.'

    def test_setting_directory_using_application_env_variable(self, monkeypatch):
        """ASTRALITY_CONFIG_HOME should override XDG_CONFIG_HOME."""
        monkeypatch.setattr(os, 'environ', {'ASTRALITY_CONFIG_HOME':'/test/dir', 
         'XDG_CONFIG_HOME':'/xdg/dir'})
        @py_assert1 = resolve_config_directory()
        @py_assert5 = '/test/dir'
        @py_assert7 = Path(@py_assert5)
        @py_assert3 = @py_assert1 == @py_assert7
        if not @py_assert3:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(resolve_config_directory) if 'resolve_config_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resolve_config_directory) else 'resolve_config_directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_setting_directory_using_xdg_directory_standard(self, monkeypatch):
        """The XDG_CONFIG_HOME environment variable should be respected."""
        monkeypatch.setattr(os, 'environ', {'XDG_CONFIG_HOME': '/xdg/dir'})
        @py_assert1 = resolve_config_directory()
        @py_assert5 = '/xdg/dir/astrality'
        @py_assert7 = Path(@py_assert5)
        @py_assert3 = @py_assert1 == @py_assert7
        if not @py_assert3:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(resolve_config_directory) if 'resolve_config_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resolve_config_directory) else 'resolve_config_directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_using_standard_config_dir_when_nothing_else_is_specified(self, monkeypatch):
        """In the absence of XDG_CONFIG_HOME, the standard location is used."""
        monkeypatch.setattr(os, 'environ', {})
        @py_assert1 = resolve_config_directory()
        @py_assert5 = '~/.config/astrality'
        @py_assert7 = Path(@py_assert5)
        @py_assert9 = @py_assert7.expanduser
        @py_assert11 = @py_assert9()
        @py_assert3 = @py_assert1 == @py_assert11
        if not @py_assert3:
            @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}.expanduser\n}()\n}', ), (@py_assert1, @py_assert11)) % {'py0':@pytest_ar._saferepr(resolve_config_directory) if 'resolve_config_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resolve_config_directory) else 'resolve_config_directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
            @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


class TestCreateConfigDirectory:
    __doc__ = 'Tests for creating configuration content, used be the CLI entrypoint.'

    def test_creation_of_empty_config_directory(self):
        """An empty configuration directory can be created."""
        config_path = Path('/tmp/config_test')
        config_dir = create_config_directory(path=config_path, empty=True)
        @py_assert1 = config_path == config_dir
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (config_path, config_dir)) % {'py0':@pytest_ar._saferepr(config_path) if 'config_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_path) else 'config_path',  'py2':@pytest_ar._saferepr(config_dir) if 'config_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_dir) else 'config_dir'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert1 = config_dir.is_dir
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(config_dir) if 'config_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_dir) else 'config_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        @py_assert3 = config_dir.iterdir
        @py_assert5 = @py_assert3()
        @py_assert7 = list(@py_assert5)
        @py_assert9 = len(@py_assert7)
        @py_assert12 = 0
        @py_assert11 = @py_assert9 == @py_assert12
        if not @py_assert11:
            @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.iterdir\n}()\n})\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(config_dir) if 'config_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_dir) else 'config_dir',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
            @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
        config_dir.rmdir()

    def test_creation_of_infered_config_directory(self, monkeypatch):
        """When no directory is specified, it is inferred instead."""
        config_path = Path('/tmp/astrality_config')
        monkeypatch.setattr(os, 'environ', {'ASTRALITY_CONFIG_HOME': str(config_path)})
        created_config_dir = create_config_directory(empty=True)
        @py_assert1 = created_config_dir == config_path
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (created_config_dir, config_path)) % {'py0':@pytest_ar._saferepr(created_config_dir) if 'created_config_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_config_dir) else 'created_config_dir',  'py2':@pytest_ar._saferepr(config_path) if 'config_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_path) else 'config_path'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        created_config_dir.rmdir()

    def test_creation_of_config_directory_with_example_content(self):
        """Test copying example configuration contents."""
        config_path = Path('/tmp/astrality_config_with_contents')
        created_config_dir = create_config_directory(config_path)
        @py_assert1 = created_config_dir == config_path
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (created_config_dir, config_path)) % {'py0':@pytest_ar._saferepr(created_config_dir) if 'created_config_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_config_dir) else 'created_config_dir',  'py2':@pytest_ar._saferepr(config_path) if 'config_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_path) else 'config_path'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        dir_contents = tuple(file.name for file in created_config_dir.iterdir())
        @py_assert0 = 'astrality.yml'
        @py_assert2 = @py_assert0 in dir_contents
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, dir_contents)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(dir_contents) if 'dir_contents' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dir_contents) else 'dir_contents'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'modules'
        @py_assert2 = @py_assert0 in dir_contents
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, dir_contents)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(dir_contents) if 'dir_contents' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dir_contents) else 'dir_contents'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        rmtree(created_config_dir)


class TestInferConfigLocation:
    __doc__ = 'Tests for config.infer_config_location().'

    def test_that_empty_config_location_still_return_paths(self, monkeypatch, caplog):
        """
        A lack of astrality.yml should not change the result.

        When astrality.yml is not found in the configuration directory, a
        warning should be logged, but the path should still be returned.
        The remaining logic should use default values for astrality.yml instead.
        """
        config_path = Path('/tmp/astrality_config')
        monkeypatch.setattr(os, 'environ', {'ASTRALITY_CONFIG_HOME': str(config_path)})
        caplog.clear()
        directory, config_file = infer_config_location()
        @py_assert1 = directory == config_path
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (directory, config_path)) % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(config_path) if 'config_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_path) else 'config_path'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert3 = 'astrality.yml'
        @py_assert5 = config_path / @py_assert3
        @py_assert1 = config_file == @py_assert5
        if not @py_assert1:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == (%(py2)s / %(py4)s)', ), (config_file, @py_assert5)) % {'py0':@pytest_ar._saferepr(config_file) if 'config_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_file) else 'config_file',  'py2':@pytest_ar._saferepr(config_path) if 'config_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_path) else 'config_path',  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'not found'
        @py_assert3 = caplog.record_tuples[0][2]
        @py_assert2 = @py_assert0 in @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None


class TestUserConfiguration:
    __doc__ = 'Tests for config.user_configuration().'

    def test_missing_global_configuration_file(self, monkeypatch, tmpdir):
        """Missing astrality.yml should result in default values."""
        config_home = Path(tmpdir)
        monkeypatch.setattr(os, 'environ', {'ASTRALITY_CONFIG_HOME': str(config_home)})
        @py_assert3 = config_home.iterdir
        @py_assert5 = @py_assert3()
        @py_assert7 = list(@py_assert5)
        @py_assert9 = len(@py_assert7)
        @py_assert12 = 0
        @py_assert11 = @py_assert9 == @py_assert12
        if not @py_assert11:
            @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.iterdir\n}()\n})\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(config_home) if 'config_home' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_home) else 'config_home',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
            @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
        modules = {'A': {'enabled': False}}
        dump_yaml(path=(config_home / 'modules.yml'), data=modules)
        context = {'section': {'key': 'value'}}
        dump_yaml(path=(config_home / 'context.yml'), data=context)
        global_config, global_modules, global_context, inferred_path = user_configuration()
        @py_assert1 = global_config == ASTRALITY_DEFAULT_GLOBAL_SETTINGS
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (global_config, ASTRALITY_DEFAULT_GLOBAL_SETTINGS)) % {'py0':@pytest_ar._saferepr(global_config) if 'global_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_config) else 'global_config',  'py2':@pytest_ar._saferepr(ASTRALITY_DEFAULT_GLOBAL_SETTINGS) if 'ASTRALITY_DEFAULT_GLOBAL_SETTINGS' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ASTRALITY_DEFAULT_GLOBAL_SETTINGS) else 'ASTRALITY_DEFAULT_GLOBAL_SETTINGS'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert1 = global_modules == modules
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (global_modules, modules)) % {'py0':@pytest_ar._saferepr(global_modules) if 'global_modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_modules) else 'global_modules',  'py2':@pytest_ar._saferepr(modules) if 'modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(modules) else 'modules'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert1 = global_context == context
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (global_context, context)) % {'py0':@pytest_ar._saferepr(global_context) if 'global_context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(global_context) else 'global_context',  'py2':@pytest_ar._saferepr(context) if 'context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context) else 'context'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert1 = inferred_path == config_home
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (inferred_path, config_home)) % {'py0':@pytest_ar._saferepr(inferred_path) if 'inferred_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inferred_path) else 'inferred_path',  'py2':@pytest_ar._saferepr(config_home) if 'config_home' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_home) else 'config_home'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None