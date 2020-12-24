# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_tools.py
# Compiled at: 2014-05-04 12:45:31
"""Tools related tests."""
import sys, os, pytest
from mock import Mock
from pyramid.path import package_path
from pyramid.i18n import Localizer
from pyramid.interfaces import ILocalizer
from pyramid_localize.tools import dummy_autotranslate
from pyramid_localize.tools import destination_path
from pyramid_localize.tools import set_localizer
from tests.conftest import web_request as web_request_func

def test_simple(web_request):
    """Simple localizer setting test on a request."""
    set_localizer(web_request)
    assert isinstance(web_request.localizer, Localizer)
    assert hasattr(web_request, '_')


def test_reset(web_request):
    """
    Test resetting localizer capabilites.

    1. localizer gets set on a request.
    2. Reset localizer call gets issued.
    3. New request have new localizer set.
    """
    set_localizer(web_request)
    old_localizer = web_request.localizer
    queried_localizer = web_request.registry.queryUtility(ILocalizer, name=web_request.locale_name)
    assert queried_localizer == web_request.localizer
    set_localizer(web_request, reset=True)
    assert old_localizer == web_request.localizer
    queried_localizer_after_reset = web_request.registry.queryUtility(ILocalizer, name=web_request.locale_name)
    assert queried_localizer_after_reset is not queried_localizer
    request = web_request_func()
    set_localizer(web_request)
    assert old_localizer is not request.localizer


def test_translate(web_request):
    """Simple test for translating method call."""
    msgid = 'Test message'
    set_localizer(web_request)
    assert msgid == web_request._(msgid)


def test_destination_filename():
    """Testing translation fullpath resolve."""
    request = Mock()
    request.registry = {'config': Mock()}
    path = '/some/path/to/translations'
    mock_configuration = {'localize.translation.destination': path}
    request.registry['config'].configure_mock(**mock_configuration)
    result = destination_path(request)
    assert result == path


def test_destination_package():
    """Testing translation package:path resolve."""
    request = Mock()
    request.registry = {'config': Mock()}
    mock_configuration = {'localize.translation.destination': 'tests:translations'}
    request.registry['config'].configure_mock(**mock_configuration)
    result = destination_path(request)
    assert result == os.path.join(package_path(sys.modules['tests']), 'translations')


@pytest.mark.parametrize('kwargs, result', (
 ({'msgid': 'Simple fake text'},
  'Simple fake text'),
 (
  {'msgid': 'test-msgid', 
     'default': 'Simple fake text'},
  'Simple fake text'),
 (
  {'msgid': 'Simple ${what} text', 
     'mapping': {'what': 'fake'}},
  'Simple fake text')))
def test_dummy_message(kwargs, result):
    """Test dummy autotranslate method."""
    assert dummy_autotranslate(**kwargs) == result