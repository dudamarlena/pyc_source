# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_config_parser.py
# Compiled at: 2019-05-16 13:41:33
from insights.core import IniConfigFile, ConfigParser
from insights.tests import context_wrap
from insights.contrib.ConfigParser import NoOptionError
from insights.parsers import SkipException
import pytest
CONFIG_FILE = ('\n[global]\nkeynospace=valuenospaces\nkey with spaces = value with spaces\nkey with continued value = value1\n                           value2\n[comment tricks]\n; semicolon comment = should not be found\n# hash comment = should not be found\ncomment # in key = value still found\ncomment in value = value includes # sign\n\n[value overwriting]\nkey = value1\nkey = value2\nkey = value3\nkey = this one should be picked\n\n#[commented section]\n#this key = should not be found either\n\n[value checks]\npositive integer value = 14\nnegative integer value = -993\npositive float value = 3.791\nnegative float value = -91.2e6\ntrue boolean value = yes\nfalse boolean value = off\n').strip()

def test_ini_config_file_parser():
    ini = IniConfigFile(context_wrap(CONFIG_FILE))
    assert list(ini.sections()) == [
     'global', 'comment tricks', 'value overwriting', 'value checks']
    assert dict(ini.items('global')) == {'keynospace': 'valuenospaces', 'key with spaces': 'value with spaces', 
       'key with continued value': 'value1\nvalue2'}
    assert dict(ini.items('comment tricks')) == {'comment # in key': 'value still found', 'comment in value': 'value includes # sign'}
    assert dict(ini.items('value overwriting')) == {'key': 'this one should be picked'}
    assert ini.get('global', 'keynospace') == 'valuenospaces'
    assert ini.get('global', 'key with spaces') == 'value with spaces'
    assert ini.get('global', 'key with continued value') == 'value1\nvalue2'
    with pytest.raises(NoOptionError):
        assert ini.get('global', 'key') is None
    assert ini.get('comment tricks', 'comment # in key') == 'value still found'
    assert ini.get('comment tricks', 'comment in value') == 'value includes # sign'
    assert ini.get('value overwriting', 'key') == 'this one should be picked'
    assert ini.getint('value checks', 'positive integer value') == 14
    assert ini.getint('value checks', 'negative integer value') == -993
    assert ini.getfloat('value checks', 'positive float value') == 3.791
    assert ini.getfloat('value checks', 'negative float value') == -91200000.0
    assert ini.getboolean('value checks', 'true boolean value')
    assert not ini.getboolean('value checks', 'false boolean value')
    assert ini.has_option('global', 'key with spaces')
    assert ini.has_option('comment tricks', 'comment in value')
    with pytest.raises(NoOptionError):
        assert ini.get('comment tricks', 'semicolon comment') is None
    assert not ini.has_option('comment tricks', 'semicolon comment')
    with pytest.raises(NoOptionError):
        assert ini.get('comment tricks', 'hash comment') is None
    assert not ini.has_option('comment tricks', 'hash comment')
    assert not ini.has_option('commented section', 'this key')
    assert 'global' in ini
    assert 'value checks' in ini
    return


def test_config_parser_empty():
    with pytest.raises(SkipException):
        assert ConfigParser(context_wrap('')) is None
    with pytest.raises(SkipException):
        assert IniConfigFile(context_wrap('')) is None
    return