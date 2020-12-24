# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/dovetail/test_config.py
# Compiled at: 2012-08-13 23:01:16
"""py.test tests for config.py"""
from dovetail.config import Option, apply_config_to_args, apply_config_to_environ, load_config_file
from dovetail.util.exception import InvalidEnvironment
from tempfile import mkdtemp
from shutil import rmtree
import os, pytest, ConfigParser
TEMP_DIR = None
DOVETAIL = 'Dovetail'
DOVETAIL_OPT = {'virtualenv': '/path/to/virtualenv', 'clear': 'True', 
   'build_file': '/path/to/build', 
   'task': 'task1 task2 task3', 
   'loglevel': 'debug', 
   'nested': 'True', 
   'reports': 'tree modules slow'}
INI_DOVETAIL = ('[{0}]\n').format(DOVETAIL)
for name, value in DOVETAIL_OPT.iteritems():
    INI_DOVETAIL += ('{0}={1}\n').format(name, value)

ENVIRONMENT = 'Environment'
VALUES = {'VAR1': 'one', 'var2': 'two'}
INI_ENVIRON = ('[{0}]\n').format(ENVIRONMENT)
for name, value in VALUES.iteritems():
    INI_ENVIRON += ('{0}={1}\n').format(name, value)

SIMPLE_INI = INI_DOVETAIL + '\n' + INI_ENVIRON
INI_NAME = None

def write_file(file_name, content):
    global TEMP_DIR
    full_name = os.path.join(TEMP_DIR, file_name)
    file = open(full_name, 'w')
    file.write(content)
    file.close()
    return full_name


def setup_module():
    global INI_NAME
    global TEMP_DIR
    TEMP_DIR = mkdtemp()
    INI_NAME = write_file('test_load.ini', SIMPLE_INI)


def teardown_module():
    rmtree(TEMP_DIR, ignore_errors=True)


class TestConfig(object):

    def test_load(self):
        parser = load_config_file(INI_NAME)
        for name, value in VALUES.iteritems():
            assert parser.get(ENVIRONMENT, name) == value

    def test_load_negative(self):
        with pytest.raises(InvalidEnvironment):
            load_config_file(os.path.dirname(__file__))

    def test_load_missing(self):
        assert load_config_file('doesnt_exist') is None
        return

    def test_load_not_config(self):
        with pytest.raises(ConfigParser.Error):
            load_config_file(__file__)

    def test_apply_environment(self):
        parser = load_config_file(INI_NAME)
        for name, value in VALUES.iteritems():
            assert os.environ.get(name) is None

        apply_config_to_environ(parser)
        for name, value in VALUES.iteritems():
            assert os.environ[name] == value

        return

    def test_clear(self):
        option = Option.lookup('clear')
        assert option is not None
        assert option.map('T') == True
        assert option.map('t') == True
        assert option.map('True') == True
        assert option.map('TRUE') == True
        assert option.map('1') == True
        assert option.map('on') == True
        assert option.map('F') == False
        assert option.map('f') == False
        assert option.map('FALSE') == False
        assert option.map('False') == False
        assert option.map('0') == False
        assert option.map('off') == False
        with pytest.raises(ValueError):
            option.map('')
        with pytest.raises(ValueError):
            option.map('wrong')
        return

    def test_nested(self):
        option = Option.lookup('nested')
        assert option is not None
        assert option.map('T') == True
        assert option.map('t') == True
        assert option.map('True') == True
        assert option.map('TRUE') == True
        assert option.map('1') == True
        assert option.map('on') == True
        assert option.map('F') == False
        assert option.map('f') == False
        assert option.map('FALSE') == False
        assert option.map('False') == False
        assert option.map('0') == False
        assert option.map('off') == False
        with pytest.raises(ValueError):
            option.map('')
        with pytest.raises(ValueError):
            option.map('wrong')
        return

    def test_task(self):
        option = Option.lookup('task')
        assert option is not None
        assert option.map('') == []
        assert option.map('one') == ['one']
        assert option.map('one two') == ['one', 'two']
        assert option.map('one two three') == ['one', 'two', 'three']
        return

    def test_reports(self):
        option = Option.lookup('reports')
        assert option is not None
        assert option.map('') == []
        assert option.map('one') == ['one']
        assert option.map('one two') == ['one', 'two']
        assert option.map('one two three') == ['one', 'two', 'three']
        return

    def test_build_file(self):
        option = Option.lookup('build_file')
        assert option is not None
        assert option.map('') == ''
        assert option.map('/path/to/file') == '/path/to/file'
        assert option.map('one two') == 'one two'
        return

    def test_virtualenv(self):
        option = Option.lookup('virtualenv')
        assert option is not None
        assert option.map('') == ''
        assert option.map('/path/to/file') == '/path/to/file'
        assert option.map('one two') == 'one two'
        return

    def test_logger(self):
        option = Option.lookup('loglevel')
        assert option is not None
        option.map('debug')
        option.map('iNfO')
        option.map('major')
        option.map('WARN')
        option.map('ERROR')
        with pytest.raises(ValueError):
            option.map('No')
        with pytest.raises(ValueError):
            option.map('')
        return

    def test_illegal_option(self):
        with pytest.raises(KeyError):
            Option.lookup('doesnt-exist')

    def test_illegal_file(self):
        args = {}
        parser = load_config_file(INI_NAME)
        parser.set(DOVETAIL, 'clear', 'invalid')
        with pytest.raises(InvalidEnvironment):
            apply_config_to_args(parser, args)
        parser = load_config_file(INI_NAME)
        parser.set(DOVETAIL, 'illegal', 'unknown')
        with pytest.raises(InvalidEnvironment):
            apply_config_to_args(parser, args)

    def test_apply_args(self):
        args = {}
        parser = load_config_file(INI_NAME)
        apply_config_to_args(parser, args)
        assert len(args) == len(DOVETAIL_OPT)
        for name, value in DOVETAIL_OPT.iteritems():
            assert args[name] == Option.lookup(name).map(value)