# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/conftest.py
# Compiled at: 2019-10-07 13:43:57
# Size of source mod 2**32: 3743 bytes
"""
The entry point for the sqlalchemy test suite.

Command line args are added and the test collector
is modified to check them.
 """
from sqlalchemy.dialects import registry
from sqlalchemy.testing import config
from sqlalchemy.testing.plugin import pytestplugin
from sqlalchemy.testing.plugin import plugin_base
from sqlalchemy.testing.plugin.pytestplugin import *
from sqlalchemy.testing.plugin.pytestplugin import pytest, inspect
registry.register('hawq', 'sqlalchemy_hawq.dialect', 'HawqDialect')
registry.register('hawq+psycopq2', 'sqlalchemy_hawq.dialect', 'HawqDialect')

def pytest_addoption(parser):
    """
    Adds custom args, then calls the sqlalchemy pytest_addoption method to handle the rest
    """
    parser.addoption('--custom-only',
      action='store_true',
      default=False,
      help='run only sqlalchemy_hawq custom tests')
    parser.addoption('--unit-only',
      action='store_true',
      default=False,
      help='run only sqlalchemy_hawq custom unit tests')
    parser.addoption('--sqla-only',
      action='store_true', default=False, help='run only the sqlalchemy test suite')
    parser.addoption('--offline-only',
      action='store_true',
      default=False,
      help="run only the tests that don't require a live connection")
    pytestplugin.pytest_addoption(parser)


def pytest_sessionstart(session):
    if plugin_base.options.offline_only:
        for fn in plugin_base.post_configure:
            if fn.__qualname__ == '_engine_uri':
                continue
            fn(plugin_base.options, plugin_base.file_config)

    else:
        pytestplugin.pytest_sessionstart(session)


def pytest_pycollect_makeitem(collector, name, obj):
    """
    Decides which tests not to run, then passes the rest of the work to
    the sqla method with the same name
    """
    if plugin_base.options.offline_only:
        if collector.name == 'test_suite.py':
            return []
            if collector.name == 'test_live_connection.py':
                return []
        else:
            if inspect.isclass(obj):
                if name.startswith('Test'):
                    return pytest.Class(name, parent=collector)
            if inspect.isfunction(obj) and name.startswith('test_'):
                return pytest.Function(name, parent=collector)
        return []
    if inspect.isclass(obj):
        if plugin_base.want_class(obj):
            if config.options.custom_only:
                if collector.name == 'test_suite.py':
                    return []
            else:
                if config.options.unit_only:
                    if collector.name == 'test_suite.py':
                        return []
                    if collector.name == 'test_live_connection.py':
                        return []
                if config.options.sqla_only and collector.name != 'test_suite.py':
                    return []
            return pytestplugin.pytest_pycollect_makeitem(collector, name, obj)
    return pytestplugin.pytest_pycollect_makeitem(collector, name, obj)


def pytest_runtest_setup(item):
    if plugin_base.options.offline_only:
        return
    pytestplugin.pytest_runtest_setup(item)


def pytest_runtest_teardown(item):
    if plugin_base.options.offline_only:
        return
    pytestplugin.pytest_runtest_teardown(item)


def pytest_sessionfinish(session):
    if plugin_base.options.offline_only:
        return
    plugin_base.final_process_cleanup()