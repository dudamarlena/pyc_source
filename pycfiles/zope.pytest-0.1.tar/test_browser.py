# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uli/WorkShop/devel/zope/zope.pytest/tags/0.1/src/zope/pytest/tests/sample_fixtures/browser/mypkg3/tests/test_browser.py
# Compiled at: 2011-03-05 10:41:26
import pytest, mypkg3
from webob import Request
from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest
from zope.pytest import configure, create_app
from mypkg3.app import SampleApp

def pytest_funcarg__apps(request):
    app = SampleApp()
    return (app, create_app(request, app))


def pytest_funcarg__config(request):
    return configure(request, mypkg3, 'ftesting.zcml')


def test_view_sampleapp(config, apps):
    (zope_app, wsgi_app) = apps
    view = getMultiAdapter((
     zope_app, TestRequest()), name='index.html')
    rendered_view = view()
    assert view() == 'Hello from SampleAppView!'


def test_browser(config, apps):
    (zope_app, wsgi_app) = apps
    http_request = Request.blank('http://localhost/test/index.html')
    response = http_request.get_response(wsgi_app)
    assert response.body == 'Hello from SampleAppView!'
    assert response.status == '200 Ok'


@pytest.mark.xfail('sys.version_info < (2,6)')
def test_infrae_browser(config, apps):
    from infrae.testbrowser.browser import Browser
    (zope_app, wsgi_app) = apps
    browser = Browser(wsgi_app)
    browser.open('http://localhost/test/index.html')
    assert browser.contents == 'Hello from SampleAppView!'
    assert browser.status == '200 Ok'