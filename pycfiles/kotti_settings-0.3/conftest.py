# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/j23d/projects/kotti_settings/kotti_settings/tests/conftest.py
# Compiled at: 2016-02-29 16:48:46
from pytest import fixture
pytest_plugins = 'kotti'

@fixture
def settings_events(config, request):
    """ Sets up event handlers for settings.
    """
    config.scan('kotti_settings.tests.test_events')
    return config