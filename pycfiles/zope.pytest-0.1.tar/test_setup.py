# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uli/WorkShop/devel/zope/zope.pytest/tags/0.1/src/zope/pytest/tests/test_setup.py
# Compiled at: 2011-03-05 10:41:26
"""Tests for the `setup` module.
"""
import zope.pytest.tests
from zope.app.wsgi import WSGIPublisherApplication
from zope.publisher.browser import TestRequest
from zope.configuration.interfaces import IConfigurationContext
from zope.pytest.setup import create_app, configure, setup_config, teardown_config, setup_db, teardown_db, setup_connection, teardown_connection, setup_root, teardown_root

def pytest_funcarg__conf_request(request):
    return request


def test_configure(conf_request):
    result = configure(conf_request, zope.pytest.tests, 'minimal.zcml')
    assert IConfigurationContext.providedBy(result)


def test_create_app(conf_request):
    config = setup_config(zope.pytest.tests, 'ftesting.zcml')
    app = create_app(conf_request, None)
    teardown_config(config)
    assert isinstance(app, WSGIPublisherApplication)
    return