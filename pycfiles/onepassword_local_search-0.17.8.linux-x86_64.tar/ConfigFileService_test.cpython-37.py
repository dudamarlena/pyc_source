# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/services/ConfigFileService_test.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 880 bytes
import pytest, os, json
from pytest_mock import mocker
import onepassword_local_search.services.ConfigFileService as ConfigFileService

def test_without_env_var(mocker):
    mocker.patch.object(ConfigFileService, '_get_local_config')
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'config'), 'r') as (f):
        config = f.read()
        f.close()
    ConfigFileService._get_local_config.return_value = json.loads(config)
    config_file_service = ConfigFileService()
    assert config_file_service.latest_signin == 'onepassword_local_search'


def test_with_env_var(monkeypatch):
    monkeypatch.setenv('ONEPASSWORD_CONFIG_FILE_PATH', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'config'))
    config_file_service = ConfigFileService()
    assert config_file_service.latest_signin == 'onepassword_local_search'