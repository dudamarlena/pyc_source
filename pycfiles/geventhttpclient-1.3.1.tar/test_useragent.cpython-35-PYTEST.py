# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gwik/dev/geventhttpclient/src/geventhttpclient/tests/test_useragent.py
# Compiled at: 2016-08-11 17:29:44
# Size of source mod 2**32: 3746 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, gevent.pywsgi, os, pytest, six, tempfile
from contextlib import contextmanager
from geventhttpclient.useragent import UserAgent, BadStatusCode

@contextmanager
def wsgiserver(handler):
    server = gevent.pywsgi.WSGIServer(('127.0.0.1', 54323), handler)
    server.start()
    try:
        yield
    finally:
        server.stop()


def check_upload(body, headers=None):

    def wsgi_handler(env, start_response):
        if headers:
            if six.PY2:
                env >= headers
            else:
                @py_assert1 = six.viewitems
                @py_assert4 = @py_assert1(env)
                @py_assert8 = six.viewitems
                @py_assert11 = @py_assert8(headers)
                @py_assert6 = @py_assert4 >= @py_assert11
                if not @py_assert6:
                    @py_format13 = @pytest_ar._call_reprcompare(('>=',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.viewitems\n}(%(py3)s)\n} >= %(py12)s\n{%(py12)s = %(py9)s\n{%(py9)s = %(py7)s.viewitems\n}(%(py10)s)\n}',), (@py_assert4, @py_assert11)) % {'py7': @pytest_ar._saferepr(six) if 'six' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(six) else 'six', 'py0': @pytest_ar._saferepr(six) if 'six' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(six) else 'six', 'py3': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env', 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(@py_assert8), 'py10': @pytest_ar._saferepr(headers) if 'headers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(headers) else 'headers', 
                     'py12': @pytest_ar._saferepr(@py_assert11), 'py2': @pytest_ar._saferepr(@py_assert1)}
                    @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format15))
                @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = None
            @py_assert2 = env['wsgi.input']
            @py_assert4 = @py_assert2.read
            @py_assert6 = @py_assert4()
            @py_assert1 = body == @py_assert6
            if not @py_assert1:
                @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.read\n}()\n}',), (body, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(body) if 'body' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(body) else 'body', 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(@py_assert2)}
                @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert1 = @py_assert2 = @py_assert4 = @py_assert6 = None
            start_response('200 OK', [])
            return []

    return wsgi_handler


def internal_server_error():

    def wsgi_handler(env, start_response):
        start_response('500 Internal Server Error', [])
        return []

    return wsgi_handler


def check_redirect():

    def wsgi_handler(env, start_response):
        if env.get('PATH_INFO') == '/':
            start_response('301 Moved Permanently', [('Location', 'http://127.0.0.1:54323/redirected')])
            return []
        else:
            @py_assert1 = env.get
            @py_assert3 = 'PATH_INFO'
            @py_assert5 = @py_assert1(@py_assert3)
            @py_assert8 = '/redirected'
            @py_assert7 = @py_assert5 == @py_assert8
            if not @py_assert7:
                @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8)}
                @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
                raise AssertionError(@pytest_ar._format_explanation(@py_format12))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
            start_response('200 OK', [])
            return [b'redirected']

    return wsgi_handler


def test_file_post():
    body = tempfile.NamedTemporaryFile('a+b', delete=False)
    name = body.name
    try:
        body.write(b'123456789')
        body.close()
        headers = {'CONTENT_LENGTH': '9', 'CONTENT_TYPE': 'application/octet-stream'}
        with wsgiserver(check_upload(b'123456789', headers)):
            useragent = UserAgent()
            with open(name, 'rb') as (body):
                useragent.urlopen('http://127.0.0.1:54323/', method='POST', payload=body)
    finally:
        os.remove(name)


def test_unicode_post():
    byte_string = b'\xc8\xb9\xc8\xbc\xc9\x85'
    unicode_string = byte_string.decode('utf-8')
    headers = {'CONTENT_LENGTH': str(len(byte_string)), 'CONTENT_TYPE': 'text/plain; charset=utf-8'}
    with wsgiserver(check_upload(byte_string, headers)):
        useragent = UserAgent()
        useragent.urlopen('http://127.0.0.1:54323/', method='POST', payload=unicode_string)


def test_bytes_post():
    headers = {'CONTENT_LENGTH': '5', 'CONTENT_TYPE': 'application/octet-stream'}
    with wsgiserver(check_upload(b'12345', headers)):
        useragent = UserAgent()
        useragent.urlopen('http://127.0.0.1:54323/', method='POST', payload=b'12345')


def test_redirect():
    with wsgiserver(check_redirect()):
        useragent = UserAgent()
        @py_assert0 = b'redirected'
        @py_assert4 = useragent.urlopen
        @py_assert6 = 'http://127.0.0.1:54323/'
        @py_assert8 = @py_assert4(@py_assert6)
        @py_assert10 = @py_assert8.read
        @py_assert12 = @py_assert10()
        @py_assert2 = @py_assert0 == @py_assert12
        if not @py_assert2:
            @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.urlopen\n}(%(py7)s)\n}.read\n}()\n}', ), (@py_assert0, @py_assert12)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(useragent) if 'useragent' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(useragent) else 'useragent', 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py13': @pytest_ar._saferepr(@py_assert12)}
            @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_server_error_with_bytes():
    with wsgiserver(internal_server_error()):
        useragent = UserAgent()
        with pytest.raises(BadStatusCode):
            useragent.urlopen('http://127.0.0.1:54323/', method='POST', payload=b'12345')


def test_server_error_with_unicode():
    with wsgiserver(internal_server_error()):
        useragent = UserAgent()
        with pytest.raises(BadStatusCode):
            useragent.urlopen('http://127.0.0.1:54323/', method='POST', payload='12345')


def test_server_error_with_file():
    body = tempfile.NamedTemporaryFile('a+b', delete=False)
    name = body.name
    try:
        body.write(b'123456789')
        body.close()
        with wsgiserver(internal_server_error()):
            useragent = UserAgent()
            with pytest.raises(BadStatusCode):
                with open(name, 'rb') as (body):
                    useragent.urlopen('http://127.0.0.1:54323/', method='POST', payload=body)
    finally:
        os.remove(name)