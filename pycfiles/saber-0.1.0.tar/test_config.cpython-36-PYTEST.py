# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_config.py
# Compiled at: 2018-12-17 16:56:04
# Size of source mod 2**32: 7128 bytes
"""Contains any and all unit tests for the config.Config class (saber/config.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from .. import config
from .resources.dummy_constants import *
from .resources.helpers import *

@pytest.fixture
def config_no_cli_args():
    """Returns an instance of a config.Config object after parsing the dummy config file with no command
    line interface (CLI) args."""
    dummy_config = config.Config(PATH_TO_DUMMY_CONFIG)
    return dummy_config


@pytest.fixture
def config_with_cli_args():
    """Returns an instance of a config.config.Config object after parsing the dummy config file with command line
    interface (CLI) args."""
    dummy_config = config.Config(PATH_TO_DUMMY_CONFIG)
    dummy_config.cli_args = DUMMY_COMMAND_LINE_ARGS
    dummy_config.harmonize_args(DUMMY_COMMAND_LINE_ARGS)
    return dummy_config


def test_process_args_no_cli_args(config_no_cli_args):
    """Asserts the config.Config.config object contains the expected attributes after initializing a config.Config
    object without CLI args."""
    @py_assert1 = config_no_cli_args.filepath
    @py_assert3 = @py_assert1 == PATH_TO_DUMMY_CONFIG
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.filepath\n} == %(py4)s', ), (@py_assert1, PATH_TO_DUMMY_CONFIG)) % {'py0':@pytest_ar._saferepr(config_no_cli_args) if 'config_no_cli_args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_no_cli_args) else 'config_no_cli_args',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(PATH_TO_DUMMY_CONFIG) if 'PATH_TO_DUMMY_CONFIG' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(PATH_TO_DUMMY_CONFIG) else 'PATH_TO_DUMMY_CONFIG'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    config = config_no_cli_args.config
    for section in CONFIG_SECTIONS:
        for arg, value in config[section].items():
            @py_assert2 = DUMMY_ARGS_NO_PROCESSING[arg]
            @py_assert1 = value == @py_assert2
            if not @py_assert1:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert2 = None

    @py_assert1 = config_no_cli_args.cli_args
    @py_assert4 = {}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.cli_args\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(config_no_cli_args) if 'config_no_cli_args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_no_cli_args) else 'config_no_cli_args',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_process_args_with_cli_args(config_with_cli_args):
    """Asserts the config.Config.config object contains the expected attributes after initializing a config.Config
    object with CLI args."""
    @py_assert1 = config_with_cli_args.filepath
    @py_assert5 = os.path
    @py_assert7 = @py_assert5.join
    @py_assert10 = os.path
    @py_assert12 = @py_assert10.dirname
    @py_assert15 = os.path
    @py_assert17 = @py_assert15.os
    @py_assert19 = @py_assert17.path
    @py_assert21 = @py_assert19.abspath
    @py_assert24 = @py_assert21(__file__)
    @py_assert26 = @py_assert12(@py_assert24)
    @py_assert29 = @py_assert7(@py_assert26, PATH_TO_DUMMY_CONFIG)
    @py_assert3 = @py_assert1 == @py_assert29
    if not @py_assert3:
        @py_format31 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.filepath\n} == %(py30)s\n{%(py30)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.path\n}.join\n}(%(py27)s\n{%(py27)s = %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s.path\n}.dirname\n}(%(py25)s\n{%(py25)s = %(py22)s\n{%(py22)s = %(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = %(py14)s.path\n}.os\n}.path\n}.abspath\n}(%(py23)s)\n})\n}, %(py28)s)\n}',), (@py_assert1, @py_assert29)) % {'py0':@pytest_ar._saferepr(config_with_cli_args) if 'config_with_cli_args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_with_cli_args) else 'config_with_cli_args',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py9':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py23':@pytest_ar._saferepr(__file__) if '__file__' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(__file__) else '__file__',  'py25':@pytest_ar._saferepr(@py_assert24),  'py27':@pytest_ar._saferepr(@py_assert26),  'py28':@pytest_ar._saferepr(PATH_TO_DUMMY_CONFIG) if 'PATH_TO_DUMMY_CONFIG' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(PATH_TO_DUMMY_CONFIG) else 'PATH_TO_DUMMY_CONFIG',  'py30':@pytest_ar._saferepr(@py_assert29)}
        @py_format33 = ('' + 'assert %(py32)s') % {'py32': @py_format31}
        raise AssertionError(@pytest_ar._format_explanation(@py_format33))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert24 = @py_assert26 = @py_assert29 = None
    config = config_with_cli_args.config
    for section in CONFIG_SECTIONS:
        for arg, value in config[section].items():
            @py_assert2 = DUMMY_ARGS_NO_PROCESSING[arg]
            @py_assert1 = value == @py_assert2
            if not @py_assert1:
                @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
                @py_format6 = ('' + 'assert %(py5)s') % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert2 = None

    @py_assert1 = config_with_cli_args.cli_args
    @py_assert3 = @py_assert1 == DUMMY_COMMAND_LINE_ARGS
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.cli_args\n} == %(py4)s',), (@py_assert1, DUMMY_COMMAND_LINE_ARGS)) % {'py0':@pytest_ar._saferepr(config_with_cli_args) if 'config_with_cli_args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_with_cli_args) else 'config_with_cli_args',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DUMMY_COMMAND_LINE_ARGS) if 'DUMMY_COMMAND_LINE_ARGS' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_COMMAND_LINE_ARGS) else 'DUMMY_COMMAND_LINE_ARGS'}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_config_attributes_no_cli_args(config_no_cli_args):
    """Asserts that the class attributes of a config.Config object are of the expected value/type after
    objects initialization, with NO command line arguments.
    """
    for arg, value in DUMMY_ARGS_NO_CLI_ARGS.items():
        @py_assert5 = getattr(config_no_cli_args, arg)
        @py_assert1 = value == @py_assert5
        if not @py_assert1:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py6)s\n{%(py6)s = %(py2)s(%(py3)s, %(py4)s)\n}', ), (value, @py_assert5)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py2':@pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr',  'py3':@pytest_ar._saferepr(config_no_cli_args) if 'config_no_cli_args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_no_cli_args) else 'config_no_cli_args',  'py4':@pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg',  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert5 = None


def test_config_attributes_with_cli_args(config_with_cli_args):
    """Asserts that the class attributes of a config.Config object are of the expected value/type after
    object initialization, taking into account command line arguments, which take precedence over
    config arguments.
    """
    for arg, value in DUMMY_ARGS_WITH_CLI_ARGS.items():
        @py_assert5 = getattr(config_with_cli_args, arg)
        @py_assert1 = value == @py_assert5
        if not @py_assert1:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py6)s\n{%(py6)s = %(py2)s(%(py3)s, %(py4)s)\n}', ), (value, @py_assert5)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py2':@pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr',  'py3':@pytest_ar._saferepr(config_with_cli_args) if 'config_with_cli_args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config_with_cli_args) else 'config_with_cli_args',  'py4':@pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg',  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert5 = None


def test_resolve_filepath(config_no_cli_args):
    """Asserts that `Config._resolve_filepath()` returns the expected values.
    """
    filepath_none_cli_args_none_expected = resource_filename(config.__name__, constants.CONFIG_FILENAME)
    filepath_none_cli_args_none_actual = config_no_cli_args._resolve_filepath(filepath=None, cli_args={})
    filepath_none_cli_args_expected = 'arbitrary/filepath/to/config.ini'
    dummy_cli_args = {'config_filepath': filepath_none_cli_args_expected}
    filepath_none_cli_args_actual = config_no_cli_args._resolve_filepath(filepath=None, cli_args=dummy_cli_args)
    filepath_cli_args_none_expected = filepath_none_cli_args_expected
    filepath_cli_args_none_actual = config_no_cli_args._resolve_filepath(filepath=filepath_cli_args_none_expected, cli_args={})
    filepath_cli_args_expected = filepath_none_cli_args_expected
    filepath_cli_args_actual = config_no_cli_args._resolve_filepath(filepath=filepath_cli_args_expected, cli_args=dummy_cli_args)
    @py_assert1 = filepath_none_cli_args_none_expected == filepath_none_cli_args_none_actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filepath_none_cli_args_none_expected, filepath_none_cli_args_none_actual)) % {'py0':@pytest_ar._saferepr(filepath_none_cli_args_none_expected) if 'filepath_none_cli_args_none_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filepath_none_cli_args_none_expected) else 'filepath_none_cli_args_none_expected',  'py2':@pytest_ar._saferepr(filepath_none_cli_args_none_actual) if 'filepath_none_cli_args_none_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filepath_none_cli_args_none_actual) else 'filepath_none_cli_args_none_actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = filepath_none_cli_args_expected == filepath_none_cli_args_actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filepath_none_cli_args_expected, filepath_none_cli_args_actual)) % {'py0':@pytest_ar._saferepr(filepath_none_cli_args_expected) if 'filepath_none_cli_args_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filepath_none_cli_args_expected) else 'filepath_none_cli_args_expected',  'py2':@pytest_ar._saferepr(filepath_none_cli_args_actual) if 'filepath_none_cli_args_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filepath_none_cli_args_actual) else 'filepath_none_cli_args_actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = filepath_cli_args_none_expected == filepath_cli_args_none_actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filepath_cli_args_none_expected, filepath_cli_args_none_actual)) % {'py0':@pytest_ar._saferepr(filepath_cli_args_none_expected) if 'filepath_cli_args_none_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filepath_cli_args_none_expected) else 'filepath_cli_args_none_expected',  'py2':@pytest_ar._saferepr(filepath_cli_args_none_actual) if 'filepath_cli_args_none_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filepath_cli_args_none_actual) else 'filepath_cli_args_none_actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = filepath_cli_args_expected == filepath_cli_args_actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (filepath_cli_args_expected, filepath_cli_args_actual)) % {'py0':@pytest_ar._saferepr(filepath_cli_args_expected) if 'filepath_cli_args_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filepath_cli_args_expected) else 'filepath_cli_args_expected',  'py2':@pytest_ar._saferepr(filepath_cli_args_actual) if 'filepath_cli_args_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filepath_cli_args_actual) else 'filepath_cli_args_actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_key_error(tmpdir):
    """Assert that a KeyError is raised when Config object is initialized with a value for
    `filepath` that does does contain a valid *.ini file.
    """
    with pytest.raises(KeyError):
        dummy_config = config.Config(tmpdir.strpath)


def test_save_no_cli_args(config_no_cli_args, tmpdir):
    """Asserts that a saved config file contains the correct arguments and values."""
    config_no_cli_args.save(tmpdir.strpath)
    saved_config = load_saved_config(tmpdir.strpath)
    unprocessed_args = unprocess_args(DUMMY_ARGS_NO_CLI_ARGS)
    for section in CONFIG_SECTIONS:
        for arg, value in saved_config[section].items():
            @py_assert2 = unprocessed_args[arg]
            @py_assert1 = value == @py_assert2
            if not @py_assert1:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert2 = None


def test_save_with_cli_args(config_with_cli_args, tmpdir):
    """Asserts that a saved config file contains the correct arguments and values, taking into
    account command line arguments, which take precedence over config arguments.
    """
    config_with_cli_args.save(tmpdir.strpath)
    saved_config = load_saved_config(tmpdir.strpath)
    unprocessed_args = unprocess_args(DUMMY_ARGS_WITH_CLI_ARGS)
    for section in CONFIG_SECTIONS:
        for arg, value in saved_config[section].items():
            @py_assert2 = unprocessed_args[arg]
            @py_assert1 = value == @py_assert2
            if not @py_assert1:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert2 = None