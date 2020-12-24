# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_dev_mark.py
# Compiled at: 2018-01-08 08:08:35
# Size of source mod 2**32: 921 bytes
from flask_dev_mark import DevMark
import pytest
from flask import Flask, Response

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route('/html')
    def html():
        body = '<html><head><title>test</title></head><body>hello</body></html>'
        return Response(body, 200, content_type='text/html')

    @app.route('/json')
    def json():
        body = '{"message":"hello"}'
        return Response(body, 200, content_type='application/json')

    app.wsgi_app = DevMark(app.wsgi_app, 'development')
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_dev_mark_html(app, client):
    r = client.get('/html')
    if not r.status_code == 200:
        raise AssertionError
    elif not r.data.decode('utf-8').count('development') > 0:
        raise AssertionError


def test_dev_mark_json(app, client):
    r = client.get('/json')
    if not r.status_code == 200:
        raise AssertionError
    elif not r.data.decode('utf-8').count('development') == 0:
        raise AssertionError