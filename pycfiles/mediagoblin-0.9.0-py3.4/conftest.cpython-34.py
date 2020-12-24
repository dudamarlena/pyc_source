# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/conftest.py
# Compiled at: 2013-09-23 12:05:53
# Size of source mod 2**32: 1387 bytes
import pytest
from mediagoblin.tests import tools
from mediagoblin.tools.testing import _activate_testing

@pytest.fixture()
def test_app(request):
    """
    py.test fixture to pass sandboxed mediagoblin applications into tests that
    want them.

    You could make a local version of this method for your own tests
    to override the paste and config files being used by passing them
    in differently to get_app.
    """
    return tools.get_app(request)


@pytest.fixture()
def pt_fixture_enable_testing():
    """
    py.test fixture to enable testing mode in tools.
    """
    _activate_testing()