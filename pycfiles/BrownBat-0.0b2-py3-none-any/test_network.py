# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/tests/test_pipeline/test_network.py
# Compiled at: 2015-07-09 10:52:32
from __future__ import absolute_import, unicode_literals
from mock import Mock, patch
from pytest import raises
from brownant.exceptions import NotSupported
from brownant.pipeline.network import HTTPClientProperty, URLQueryProperty, TextResponseProperty, ResponseProperty, JSONResponseProperty

def test_http_client():
    dinergate = Mock()
    with patch(b'requests.Session') as (Session):
        instance = Session.return_value
        http_client = HTTPClientProperty(session_class=Session)
        assert http_client.provide_value(dinergate) is instance
        Session.assert_called_once_with()


def test_url_query():
    mock = Mock()
    mock.request.args.get.return_value = b'42'
    url_query = URLQueryProperty(name=b'value')
    rv = url_query.provide_value(mock)
    assert rv == b'42'
    mock.request.args.get.assert_called_once_with(b'value', type=None)
    return


def test_url_query_type():
    mock = Mock()
    mock.request.args.get.return_value = 42
    url_query = URLQueryProperty(name=b'value', type=int)
    rv = url_query.provide_value(mock)
    assert rv == 42
    mock.request.args.get.assert_called_once_with(b'value', type=int)


def test_url_query_required():
    mock = Mock()
    mock.request.args.get.return_value = None
    url_query = URLQueryProperty(name=b'value')
    with raises(NotSupported):
        url_query.provide_value(mock)
    return


def test_url_query_optional():
    mock = Mock()
    mock.request.args.get.return_value = None
    url_query = URLQueryProperty(name=b'd', type=float, required=False)
    rv = url_query.provide_value(mock)
    assert rv is None
    mock.request.args.get.assert_called_once_with(b'd', type=float)
    return


def test_url_query_required_boundary_condition():
    mock = Mock()
    mock.request.args.get.return_value = 0
    url_query = URLQueryProperty(name=b'num')
    rv = url_query.provide_value(mock)
    assert rv == 0
    mock.request.args.get.assert_called_once_with(b'num', type=None)
    return


def test_base_response():
    response = Mock()
    response.text = b'OK'
    mock = Mock()
    mock.url = b'http://example.com'
    mock.http_client.request.return_value = response
    response = ResponseProperty()
    with raises(KeyError):
        response.provide_value(mock)


def test_text_response():

    class HTTPError(Exception):
        pass

    response = Mock()
    response.text = b'OK'
    response.raise_for_status.side_effect = [None, HTTPError()]
    mock = Mock()
    mock.url = b'http://example.com'
    mock.http_client.request.return_value = response
    text = TextResponseProperty(method=b'POST')
    rv = text.provide_value(mock)
    assert rv == b'OK'
    response.raise_for_status.assert_called_once_with()
    mock.http_client.request.assert_called_once_with(method=b'POST', url=b'http://example.com')
    with raises(HTTPError):
        text.provide_value(mock)
    return


def test_json_response():

    class HTTPError(Exception):
        pass

    response = Mock()
    response.json.return_value = {b'a': 1, b'b': {b'c': 2, b'd': 3}}
    response.raise_for_status.side_effect = [None, HTTPError()]
    mock = Mock()
    mock.url = b'http://example.com'
    mock.http_client.request.return_value = response
    json = JSONResponseProperty(method=b'POST')
    rv = json.provide_value(mock)
    assert rv == {b'a': 1, 
       b'b': {b'c': 2, 
              b'd': 3}}
    response.raise_for_status.assert_called_once_with()
    mock.http_client.request.assert_called_once_with(method=b'POST', url=b'http://example.com')
    with raises(HTTPError):
        json.provide_value(mock)
    return