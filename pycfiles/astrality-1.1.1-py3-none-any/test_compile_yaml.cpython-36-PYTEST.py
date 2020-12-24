# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/utils/test_compile_yaml.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 1493 bytes
"""Tests for compiling YAML jinja2 templates."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from pathlib import Path
import pytest
from astrality.config import user_configuration
from astrality.utils import compile_yaml

@pytest.yield_fixture
def dir_with_compilable_files(tmpdir):
    """Create some temporary YAML files which can be compiled."""
    config_dir = Path(tmpdir)
    config_file = config_dir / 'astrality.yml'
    config_file.write_text('key1: {{ env.EXAMPLE_ENV_VARIABLE }}\nkey2: {{ "echo test" | shell }}')
    module_file = config_dir / 'modules.yml'
    module_file.write_text('key1: {{ env.EXAMPLE_ENV_VARIABLE }}\nkey2: {{ "echo test" | shell }}')
    yield config_dir
    os.remove(config_file)
    os.remove(module_file)
    config_dir.rmdir()


class TestUsingConfigFilesWithPlaceholders:

    def test_dict_from_config_file(self, dir_with_compilable_files):
        """Placeholders should be properly substituted."""
        config = compile_yaml(path=(dir_with_compilable_files / 'astrality.yml'),
          context={})
        @py_assert2 = {'key1':'test_value', 
         'key2':'test'}
        @py_assert1 = config == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (config, @py_assert2)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    def test_get_user_configuration(self, dir_with_compilable_files):
        """user_configuration should use compile_yaml properly."""
        user_conf, *_ = user_configuration(dir_with_compilable_files)
        @py_assert0 = user_conf['key1']
        @py_assert3 = 'test_value'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = user_conf['key2']
        @py_assert3 = 'test'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None