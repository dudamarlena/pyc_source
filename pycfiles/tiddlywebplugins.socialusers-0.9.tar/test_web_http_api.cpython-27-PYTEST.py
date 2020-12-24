# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.socialusers/test/test_web_http_api.py
# Compiled at: 2012-10-14 16:14:34
"""
Run through the socialusers API testing what's there.

Read the TESTS variable as document of
the capabilities of the API.

If you run this test file by itself, instead
of as a test it will produce a list of test
requests and some associated information.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, shutil
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2, simplejson, yaml
from base64 import b64encode
from re import match
from tiddlyweb.model.user import User
base_url = 'http://our_test_domain:8001'

def setup_module(module):
    from tiddlyweb.web import serve

    def app_fn():
        return serve.load_app()

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('our_test_domain', 8001, app_fn)
    try:
        shutil.rmtree('store')
    except OSError:
        pass

    module.http = httplib2.Http()


def test_assert_response():
    """
    Make sure our assertion tester is valid.
    """
    response = {'status': '200', 
       'location': 'http://example.com'}
    content = 'Hello World\n'
    status = '200'
    headers = {'location': 'http://example.com'}
    expected = [
     'Hello']
    assert_response(response, content, status, headers, expected)


EMPTY_TEST = {'name': '', 
   'desc': '', 
   'method': 'GET', 
   'url': '', 
   'status': '200', 
   'request_headers': {}, 'response_headers': {}, 'expected': [], 'data': ''}
TESTS = yaml.load(open('test/httptest.yaml'))

def test_the_TESTS():
    """
    Run the entire TEST.
    """
    for test_data in TESTS:
        test = dict(EMPTY_TEST)
        test.update(test_data)
        yield (test['name'], _run_test, test)


def _run_test(test):
    full_url = base_url + test['url']
    if test['method'] == 'GET' or test['method'] == 'DELETE':
        response, content = http.request(full_url, method=test['method'], headers=test['request_headers'])
    else:
        response, content = http.request(full_url, method=test['method'], headers=test['request_headers'], body=test['data'].encode('UTF-8'))
    assert_response(response, content, test['status'], headers=test['response_headers'], expected=test['expected'])


def assert_response(response, content, status, headers=None, expected=None):
    if response['status'] == '500':
        print content
    @py_assert0 = response['status']
    @py_assert3 = '%s'
    @py_assert6 = @py_assert3 % status
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == (%(py4)s %% %(py5)s)', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(status) if 'status' in @py_builtins.locals() is not @py_builtins.globals() else 'status'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert6 = None
    if headers:
        for header in headers:
            @py_assert0 = response[header]
            @py_assert3 = headers[header]
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None

    if expected:
        for expect in expected:
            @py_assert1 = expect.encode
            @py_assert3 = 'UTF-8'
            @py_assert5 = @py_assert1(@py_assert3)
            @py_assert7 = @py_assert5 in content
            if not @py_assert7:
                @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.encode\n}(%(py4)s)\n} in %(py8)s', ), (@py_assert5, content)) % {'py0': @pytest_ar._saferepr(expect) if 'expect' in @py_builtins.locals() is not @py_builtins.globals() else 'expect', 'py8': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() is not @py_builtins.globals() else 'content', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
                @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                raise AssertionError(@pytest_ar._format_explanation(@py_format11))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None

    return


if __name__ == '__main__':
    for test_data in TESTS:
        test = dict(EMPTY_TEST)
        test.update(test_data)
        full_url = base_url + test['url']
        print test['name']
        print '%s %s' % (test['method'], full_url)
        print