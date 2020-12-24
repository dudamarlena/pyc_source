# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_sysconfig_options.py
# Compiled at: 2019-05-16 13:41:33
from insights.core import SysconfigOptions
from insights.tests import context_wrap
STANDARD_CONFIG = '\n# This is a standard, but made up, config file example\nOPTIONS="-x -g"\n\nUSER=root\nHOST=192.168.0.100\nPORT=1066\n'
TRICKY_CONFIG = '\n# COMMENTED_OUT=1\nSELECTOR=\'and all that\'\n     SPACES_IN_FRONT=yes\nCOMMENT_SPACE_OK=value_with_#\nSPACE_COMMENT_IGNORED=value_with #nothing else\nCOMMENT_NOSPACE_OK=value_with_#_in_it\nCOMMENT_QUOTED_IN_VALUE="This value should have a # character in it"\nMANY_QUOTES="this "\'is\'" valid"\nQUOTE_HANDLING="single \' allowed"\nOPTION_WITH_NO_VALUE=\nDOUBLE_EQUALS==included\n  # blank lines with a comment are ignored\n\n# blank lines without comments are ignored too.\n# Comments with apostrophes shouldn\'t fool the dequoting process\nVALUE_ON_QUOTE_COMMENT_LINE=this_is_OK # but this hasn\'t been read\nthis line should be in unparsed lines afterward\nAND = \'so should this\'\n' + 'SPACES_AFTER_VALUE=should_be_ignored    \n' + '  \n'

def test_standard_config():
    config = SysconfigOptions(context_wrap(STANDARD_CONFIG))
    assert 'OPTIONS' in config.data
    assert 'USER' in config.data
    assert 'HOST' in config.data
    assert 'PORT' in config.data
    assert config.data['OPTIONS'] == '-x -g'
    assert config.data['USER'] == 'root'
    assert config.data['HOST'] == '192.168.0.100'
    assert config.data['PORT'] == '1066'
    assert sorted(config.keys()) == sorted(['OPTIONS', 'USER', 'HOST', 'PORT'])
    assert 'OPTIONS' in config
    assert 'USER' in config
    assert 'HOST' in config
    assert 'PORT' in config
    assert config['OPTIONS'] == '-x -g'
    assert config['USER'] == 'root'
    assert config['HOST'] == '192.168.0.100'
    assert config['PORT'] == '1066'
    assert config.get('OPTIONS', 'wrong') == '-x -g'
    assert config.get('NO_KEY', 'value') == 'value'


def test_tricky_config():
    config = SysconfigOptions(context_wrap(TRICKY_CONFIG))
    assert sorted(config.data.keys()) == sorted([
     'SELECTOR', 'SPACES_IN_FRONT', 'SPACES_AFTER_VALUE',
     'COMMENT_SPACE_OK', 'SPACE_COMMENT_IGNORED', 'COMMENT_NOSPACE_OK',
     'COMMENT_QUOTED_IN_VALUE', 'MANY_QUOTES', 'QUOTE_HANDLING',
     'OPTION_WITH_NO_VALUE', 'DOUBLE_EQUALS',
     'VALUE_ON_QUOTE_COMMENT_LINE'])
    assert config.data['SELECTOR'] == 'and all that'
    assert config.data['SPACES_IN_FRONT'] == 'yes'
    assert config.data['SPACES_AFTER_VALUE'] == 'should_be_ignored'
    assert config.data['COMMENT_SPACE_OK'] == 'value_with_#'
    assert config.data['SPACE_COMMENT_IGNORED'] == 'value_with'
    assert config.data['COMMENT_NOSPACE_OK'] == 'value_with_#_in_it'
    assert config.data['COMMENT_QUOTED_IN_VALUE'] == 'This value should have a # character in it'
    assert config.data['MANY_QUOTES'] == 'this is valid'
    assert config.data['QUOTE_HANDLING'] == "single ' allowed"
    assert config.data['OPTION_WITH_NO_VALUE'] == ''
    assert config.data['DOUBLE_EQUALS'] == '=included'
    assert config.data['VALUE_ON_QUOTE_COMMENT_LINE'] == 'this_is_OK'
    assert config.unparsed_lines == [
     'this line should be in unparsed lines afterward',
     "AND = 'so should this'"]