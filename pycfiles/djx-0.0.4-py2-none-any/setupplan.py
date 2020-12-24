# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/pytest/_pytest/setupplan.py
# Compiled at: 2019-02-14 00:35:47
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pytest

def pytest_addoption(parser):
    group = parser.getgroup('debugconfig')
    group.addoption('--setupplan', '--setup-plan', action='store_true', help="show what fixtures and tests would be executed but don't execute anything.")


@pytest.hookimpl(tryfirst=True)
def pytest_fixture_setup(fixturedef, request):
    if request.config.option.setupplan:
        fixturedef.cached_result = (None, None, None)
        return fixturedef.cached_result
    else:
        return


@pytest.hookimpl(tryfirst=True)
def pytest_cmdline_main(config):
    if config.option.setupplan:
        config.option.setuponly = True
        config.option.setupshow = True