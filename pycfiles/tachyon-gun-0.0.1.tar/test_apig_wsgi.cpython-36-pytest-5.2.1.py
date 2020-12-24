# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py
# Compiled at: 2019-08-19 08:53:11
# Size of source mod 2**32: 6898 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys
from base64 import b64encode
from io import BytesIO
import pytest
from apig_wsgi import make_lambda_handler

@pytest.fixture()
def simple_app():

    def app(environ, start_response):
        app.environ = environ
        start_response('200 OK', app.headers, app.exc_info)
        return BytesIO(app.response)

    app.headers = [
     ('Content-Type', 'text/plain')]
    app.response = b'Hello World\n'
    app.handler = make_lambda_handler(app)
    app.exc_info = None
    yield app


parametrize_text_content_type = pytest.mark.parametrize('text_content_type', ['text/plain', 'text/html', 'application/json'])

def make_event(method='GET', qs_params=None, headers=None, body='', binary=False, request_context=None):
    if headers is None:
        headers = {'Host': 'example.com'}
    else:
        event = {'httpMethod':method, 
         'path':'/', 
         'queryStringParameters':qs_params, 
         'headers':headers}
        if binary:
            event['body'] = b64encode(body.encode('utf-8'))
            event['isBase64Encoded'] = True
        else:
            event['body'] = body
    if request_context is not None:
        event['requestContext'] = request_context
    return event


def test_get(simple_app):
    response = simple_app.handler(make_event(), None)
    @py_assert2 = {'statusCode':200, 
     'headers':{'Content-Type': 'text/plain'},  'body':'Hello World\n'}
    @py_assert1 = response == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=62)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (response, @py_assert2)) % {'py0':@pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_get_missing_content_type(simple_app):
    simple_app.headers = []
    response = simple_app.handler(make_event(), None)
    @py_assert2 = {'statusCode':200, 
     'headers':{},  'body':'Hello World\n'}
    @py_assert1 = response == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=74)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (response, @py_assert2)) % {'py0':@pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@parametrize_text_content_type
def test_get_binary_support_text(simple_app, text_content_type):
    simple_app.handler = make_lambda_handler(simple_app, binary_support=True)
    simple_app.headers = [('Content-Type', text_content_type)]
    response = simple_app.handler(make_event(), None)
    @py_assert2 = {'statusCode':200,  'headers':{'Content-Type': text_content_type},  'body':'Hello World\n'}
    @py_assert1 = response == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=83)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (response, @py_assert2)) % {'py0':@pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_get_binary_support_binary(simple_app):
    simple_app.handler = make_lambda_handler(simple_app, binary_support=True)
    simple_app.headers = [('Content-Type', 'application/octet-stream')]
    simple_app.response = b'\x137'
    response = simple_app.handler(make_event(), None)
    @py_assert2 = {'statusCode':200, 
     'headers':{'Content-Type': 'application/octet-stream'},  'body':b64encode(b'\x137').decode('utf-8'),  'isBase64Encoded':True}
    @py_assert1 = response == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=97)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (response, @py_assert2)) % {'py0':@pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@parametrize_text_content_type
def test_get_binary_support_binary_text_with_gzip_content_encoding(simple_app, text_content_type):
    simple_app.handler = make_lambda_handler(simple_app, binary_support=True)
    simple_app.headers = [
     (
      'Content-Type', text_content_type),
     ('Content-Encoding', 'gzip')]
    simple_app.response = b'\x137'
    response = simple_app.handler(make_event(), None)
    @py_assert2 = {'statusCode':200, 
     'headers':{'Content-Type':text_content_type,  'Content-Encoding':'gzip'},  'body':b64encode(b'\x137').decode('utf-8'),  'isBase64Encoded':True}
    @py_assert1 = response == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=118)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (response, @py_assert2)) % {'py0':@pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_get_binary_support_no_content_type(simple_app):
    simple_app.handler = make_lambda_handler(simple_app, binary_support=True)
    simple_app.headers = []
    simple_app.response = b'\x137'
    response = simple_app.handler(make_event(), None)
    @py_assert2 = {'statusCode':200, 
     'headers':{},  'body':b64encode(b'\x137').decode('utf-8'),  'isBase64Encoded':True}
    @py_assert1 = response == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=133)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (response, @py_assert2)) % {'py0':@pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_post(simple_app):
    event = make_event(method='POST', body='The World is Large')
    response = simple_app.handler(event, None)
    @py_assert0 = simple_app.environ['wsgi.input']
    @py_assert2 = @py_assert0.read
    @py_assert4 = @py_assert2()
    @py_assert7 = b'The World is Large'
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=146)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.read\n}()\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = simple_app.environ['CONTENT_LENGTH']
    @py_assert5 = b'The World is Large'
    @py_assert7 = len(@py_assert5)
    @py_assert9 = str(@py_assert7)
    @py_assert2 = @py_assert0 == @py_assert9
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=147)
    if not @py_assert2:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py10)s\n{%(py10)s = %(py3)s(%(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n})\n}', ), (@py_assert0, @py_assert9)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert2 = {'statusCode':200,  'headers':{'Content-Type': 'text/plain'},  'body':'Hello World\n'}
    @py_assert1 = response == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=148)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (response, @py_assert2)) % {'py0':@pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_post_binary_support(simple_app):
    simple_app.handler = make_lambda_handler(simple_app)
    event = make_event(method='POST', body='dogfood', binary=True)
    response = simple_app.handler(event, None)
    @py_assert0 = simple_app.environ['wsgi.input']
    @py_assert2 = @py_assert0.read
    @py_assert4 = @py_assert2()
    @py_assert7 = b'dogfood'
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=161)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.read\n}()\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = simple_app.environ['CONTENT_LENGTH']
    @py_assert5 = b'dogfood'
    @py_assert7 = len(@py_assert5)
    @py_assert9 = str(@py_assert7)
    @py_assert2 = @py_assert0 == @py_assert9
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=162)
    if not @py_assert2:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py10)s\n{%(py10)s = %(py3)s(%(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n})\n}', ), (@py_assert0, @py_assert9)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert2 = {'statusCode':200,  'headers':{'Content-Type': 'text/plain'},  'body':'Hello World\n'}
    @py_assert1 = response == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=163)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (response, @py_assert2)) % {'py0':@pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_querystring_none(simple_app):
    event = make_event()
    simple_app.handler(event, None)
    @py_assert0 = simple_app.environ['QUERY_STRING']
    @py_assert3 = ''
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=175)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_querystring_empty(simple_app):
    event = make_event(qs_params={})
    simple_app.handler(event, None)
    @py_assert0 = simple_app.environ['QUERY_STRING']
    @py_assert3 = ''
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=183)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_querystring_one(simple_app):
    event = make_event(qs_params={'foo': 'bar'})
    simple_app.handler(event, None)
    @py_assert0 = simple_app.environ['QUERY_STRING']
    @py_assert3 = 'foo=bar'
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=191)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_plain_header(simple_app):
    event = make_event(headers={'Test-Header': 'foobar'})
    simple_app.handler(event, None)
    @py_assert0 = simple_app.environ['HTTP_TEST_HEADER']
    @py_assert3 = 'foobar'
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=199)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_special_headers(simple_app):
    event = make_event(headers={'Content-Type':'text/plain', 
     'Host':'example.com', 
     'X-Forwarded-For':'1.2.3.4, 5.6.7.8', 
     'X-Forwarded-Proto':'https', 
     'X-Forwarded-Port':'123'})
    simple_app.handler(event, None)
    @py_assert0 = simple_app.environ['CONTENT_TYPE']
    @py_assert3 = 'text/plain'
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=215)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = simple_app.environ['SERVER_NAME']
    @py_assert3 = 'example.com'
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=216)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = simple_app.environ['REMOTE_ADDR']
    @py_assert3 = '1.2.3.4'
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=217)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = simple_app.environ['wsgi.url_scheme']
    @py_assert3 = 'https'
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=218)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = simple_app.environ['SERVER_PORT']
    @py_assert3 = '123'
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=219)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_no_headers(simple_app):
    event = make_event()
    del event['headers']
    simple_app.handler(event, None)


def test_headers_None(simple_app):
    event = make_event()
    event['headers'] = None
    simple_app.handler(event, None)


def test_exc_info(simple_app):
    try:
        raise ValueError('Example exception')
    except ValueError:
        simple_app.exc_info = sys.exc_info()

    with pytest.raises(ValueError) as (excinfo):
        simple_app.handler(make_event(), None)
    @py_assert2 = excinfo.value
    @py_assert4 = str(@py_assert2)
    @py_assert7 = 'Example exception'
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=247)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.value\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_request_context(simple_app):
    context = {'authorizer': {'user': 'test@example.com'}}
    event = make_event(request_context=context)
    simple_app.handler(event, None)
    @py_assert0 = simple_app.environ['apig_wsgi.request_context']
    @py_assert2 = @py_assert0 == context
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/chainz/Documents/Projects/apig-wsgi/tests/test_apig_wsgi.py', lineno=256)
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, context)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(context) if 'context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context) else 'context'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None