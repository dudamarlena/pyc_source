# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/utils/test_configreader.py
# Compiled at: 2017-03-02 15:52:35
# Size of source mod 2**32: 1110 bytes
import os, pytest
from baroque.utils import configreader
from baroque.exceptions.configuration import ConfigurationNotFoundError, ConfigurationParseError

def test_readconfig():
    with pytest.raises(ConfigurationNotFoundError):
        configreader.readconfig('abcdefgh')
        pytest.fail()
    this_file = os.path.realpath(__file__)
    with pytest.raises(ConfigurationParseError):
        configreader.readconfig(this_file)
        pytest.fail()
    this_dir = os.path.dirname(__file__)
    yml_file = os.path.join(os.path.dirname(os.path.dirname(this_dir)), 'baroque.yml')
    conf = configreader.readconfig(yml_file)
    assert isinstance(conf, dict)


def test_read_config_or_default():
    assert isinstance(configreader.read_config_or_default(None), dict)
    with pytest.raises(ConfigurationNotFoundError):
        configreader.readconfig('abcdefgh')
        pytest.fail()