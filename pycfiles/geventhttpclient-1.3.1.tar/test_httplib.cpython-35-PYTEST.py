# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gwik/dev/geventhttpclient/src/geventhttpclient/tests/test_httplib.py
# Compiled at: 2016-07-05 05:26:31
# Size of source mod 2**32: 1873 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, six, pytest
if six.PY2:
    from httplib import HTTPException
else:
    from http.client import HTTPException
from geventhttpclient.httplib import HTTPConnection
import gevent.server
from contextlib import contextmanager
listener = ('127.0.0.1', 54322)

@contextmanager
def server(handler):
    server = gevent.server.StreamServer(listener, handle=handler)
    server.start()
    try:
        yield
    finally:
        server.stop()


def wrong_response_status_line(sock, addr):
    sock.recv(4096)
    sock.sendall(b'HTTP/1.1 apfais df0 asdf\r\n\r\n')


def test_httplib_exception():
    with server(wrong_response_status_line):
        connection = HTTPConnection(*listener)
        connection.request('GET', '/')
        with pytest.raises(HTTPException):
            connection.getresponse()


def success_response(sock, addr):
    sock.recv(4096)
    sock.sendall(b'HTTP/1.1 200 Ok\r\nContent-Type: text/plain\r\nSet-Cookie: foo=bar\r\nSet-Cookie: baz=bar\r\nContent-Length: 12\r\n\r\nHello World!')


def test_success_response():
    with server(success_response):
        connection = HTTPConnection(*listener)
        connection.request('GET', '/')
        response = connection.getresponse()
        @py_assert1 = response.should_keep_alive
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.should_keep_alive\n}()\n}') % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = response.message_complete
        if not @py_assert1:
            @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.message_complete\n}') % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None
        @py_assert1 = response.should_close
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.should_close\n}()\n}') % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = response.read
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3.decode
        @py_assert7 = @py_assert5()
        @py_assert10 = 'Hello World!'
        @py_assert9 = @py_assert7 == @py_assert10
        if not @py_assert9:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n}.decode\n}()\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
        @py_assert1 = response.content_length
        @py_assert4 = 12
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.content_length\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None


def test_msg():
    with server(success_response):
        connection = HTTPConnection(*listener)
        connection.request('GET', '/')
        response = connection.getresponse()
        @py_assert0 = response.msg['Set-Cookie']
        @py_assert3 = 'foo=bar, baz=bar'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = response.msg['Content-Type']
        @py_assert3 = 'text/plain'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None