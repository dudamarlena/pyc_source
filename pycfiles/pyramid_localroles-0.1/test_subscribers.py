# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_subscribers.py
# Compiled at: 2014-05-04 12:45:31
__doc__ = 'Subscribers related tests.'
import pytest
from pyramid import testing
from pyramid.request import Request
from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from pyramid.i18n import Localizer

@pytest.fixture
def request_i18n():
    """New request with i18n subscribers on."""
    config = testing.setUp()
    config.scan('pyramid_localize.subscribers.i18n')
    request = Request({})
    request.registry = config.registry
    return request


def test_i18n_new_request(request_i18n):
    """Test if method are being added to request."""
    request_i18n.registry.notify(NewRequest(request_i18n))
    assert isinstance(request_i18n.localizer, Localizer)
    assert hasattr(request_i18n, '_')


def test_i18n_before_render(request_i18n):
    """Test if appropriate methods are being added to render context."""
    before_render_event = BeforeRender({'request': request_i18n}, {})
    request_i18n.registry.notify(before_render_event)
    assert 'localizer' in before_render_event
    assert '_' in before_render_event


def test_i18n_before_render_and_request(request_i18n):
    """Test if appropriate methods are being added to both context and request."""
    request_i18n.registry.notify(NewRequest(request_i18n))
    before_render_event = BeforeRender({'request': request_i18n}, {})
    request_i18n.registry.notify(before_render_event)
    assert 'localizer' in before_render_event
    assert '_' in before_render_event


@pytest.fixture
def request_fake():
    """New request with fake i18n subscribers on."""
    config = testing.setUp()
    config.scan('pyramid_localize.subscribers.fake')
    request = Request({})
    request.registry = config.registry
    return request


def test_fake_new_request(request_fake):
    """Test if method are being added to request."""
    request_fake.registry.notify(NewRequest(request_fake))
    assert hasattr(request_fake, '_')


def test_fake_before_render(request_fake):
    """Test if appropriate methods are being added to both context and request."""
    request_fake.registry.notify(NewRequest(request_fake))
    before_render_event = BeforeRender({'request': request_fake}, {})
    request_fake.registry.notify(before_render_event)
    assert '_' in before_render_event


def test_fake_before_render_norequest(request_fake):
    """Test if appropriate methods are being added to render context."""
    before_render_event = BeforeRender({'request': request_fake}, {})
    request_fake.registry.notify(before_render_event)
    assert '_' in before_render_event