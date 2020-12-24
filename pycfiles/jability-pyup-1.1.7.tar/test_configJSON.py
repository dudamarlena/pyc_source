# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/test_configJSON.py
# Compiled at: 2013-05-25 04:38:30
import configJSON
from configJSON import *
import os.path
test_cfg_file = os.path.join(os.path.dirname(__file__), 'tests/test.json')
notexisting_cfg_file = os.path.join(os.path.dirname(__file__), 'tests/notexisting.json')
dir_cfg_file = os.path.join(os.path.dirname(__file__), 'tests/')
temp_cfg_file = os.path.join(os.path.dirname(__file__), 'tests/temp/test.json')

def test_exists():
    cfg = ConfigJSON(test_cfg_file)
    assert cfg.exists() == True
    cfg = ConfigJSON(notexisting_cfg_file)
    assert cfg.exists() == False
    cfg = ConfigJSON(dir_cfg_file)
    assert cfg.exists() == False


def test_load():
    cfg = ConfigJSON(test_cfg_file)
    assert not cfg.load() == None
    cfg = ConfigJSON(dir_cfg_file)
    assert cfg.load() == None
    return


def test_parse():
    cfg = ConfigJSON(test_cfg_file)
    conf = cfg.load()
    assert conf['configuration1']['liste1'] == ['a', 'b', 'c']


def test_save():
    cfg = ConfigJSON(test_cfg_file)
    conf = cfg.load()
    conf['configuration1']['key1'] = 'NewValue'
    cfg.save(conf, temp_cfg_file)
    cfg2 = ConfigJSON(temp_cfg_file)
    assert cfg2.exists() == True
    conf2 = cfg2.load()
    assert conf2['configuration1']['key1'] == 'NewValue'
    os.remove(temp_cfg_file)
    assert cfg2.exists() == False


def test_update():
    cfg = ConfigJSON(test_cfg_file)
    assert cfg.exists() == True
    conf = cfg.load()
    cfg.save(conf, temp_cfg_file)
    assert cfg.version == '0.1'
    assert conf['configuration1'].has_key('foo2') == False
    assert conf['configuration1'].has_key('todelete') == True
    cfg.update()
    assert cfg.version == '1.2.0'
    print conf['configuration1']['foo2']
    assert conf['configuration1']['foo2'] == [1, 2, 3]
    assert conf['configuration1'].has_key('todelete') == False


if __name__ == '__main__':
    import doctest
    doctest.testmod(configJSON)
    try:
        import nose
        nose.main()
    except ImportError:
        pass