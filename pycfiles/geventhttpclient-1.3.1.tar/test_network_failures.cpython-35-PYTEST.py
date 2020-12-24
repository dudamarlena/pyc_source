# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gwik/dev/geventhttpclient/src/geventhttpclient/tests/test_network_failures.py
# Compiled at: 2016-07-05 05:26:31
# Size of source mod 2**32: 4322 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, six, pytest
if six.PY2:
    from httplib import HTTPException
else:
    from http.client import HTTPException
from geventhttpclient import HTTPClient
import gevent.server, gevent.socket
from contextlib import contextmanager
CRLF = '\r\n'
listener = ('127.0.0.1', 54326)

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


def test_exception():
    with server(wrong_response_status_line):
        connection = HTTPClient(*listener)
        with pytest.raises(HTTPException):
            connection.get('/')


def close(sock, addr):
    sock.close()


def test_close():
    with server(close):
        client = HTTPClient(*listener)
        with pytest.raises(HTTPException):
            client.get('/')


def close_after_recv(sock, addr):
    sock.recv(4096)
    sock.close()


def test_close_after_recv():
    with server(close_after_recv):
        client = HTTPClient(*listener)
        with pytest.raises(HTTPException):
            client.get('/')


def timeout_recv(sock, addr):
    sock.recv(4096)
    gevent.sleep(1)


def test_timeout_recv():
    with server(timeout_recv):
        connection = HTTPClient(*listener, network_timeout=0.1)
        with pytest.raises(gevent.socket.timeout):
            connection.request('GET', '/')


def timeout_send(sock, addr):
    gevent.sleep(1)


def test_timeout_send():
    with server(timeout_send):
        connection = HTTPClient(*listener, network_timeout=0.1)
        with pytest.raises(gevent.socket.timeout):
            connection.request('GET', '/')


def close_during_content(sock, addr):
    sock.recv(4096)
    sock.sendall(b'HTTP/1.1 200 Ok\r\nContent-Length: 100\r\n\r\n')
    sock.close()


def test_close_during_content():
    with server(close_during_content):
        client = HTTPClient(*listener, block_size=1)
        response = client.get('/')
        with pytest.raises(HTTPException):
            response.read()


def content_too_small(sock, addr):
    sock.recv(4096)
    sock.sendall(b'HTTP/1.1 200 Ok\r\nContent-Length: 100\r\n\r\ncontent')
    gevent.sleep(10)


def test_content_too_small():
    with server(content_too_small):
        client = HTTPClient(*listener, network_timeout=0.2)
        with pytest.raises(gevent.socket.timeout):
            response = client.get('/')
            response.read()


def close_during_chuncked_readline(sock, addr):
    sock.recv(4096)
    sock.sendall(b'HTTP/1.1 200 Ok\r\nTransfer-Encoding: chunked\r\n\r\n')
    chunks = [
     'This is the data in the first chunk\r\n',
     'and this is the second one\r\n',
     'con\r\n']
    for chunk in chunks:
        gevent.sleep(0.1)
        sock.sendall((hex(len(chunk))[2:] + CRLF + chunk + CRLF).encode())

    sock.close()


def test_close_during_chuncked_readline():
    with server(close_during_chuncked_readline):
        client = HTTPClient(*listener)
        response = client.get('/')
        @py_assert0 = response['transfer-encoding']
        @py_assert3 = 'chunked'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        chunks = []
        with pytest.raises(HTTPException):
            data = 'enter_loop'
            while data:
                data = response.readline()
                chunks.append(data)

        @py_assert2 = len(chunks)
        @py_assert5 = 3
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(chunks) if 'chunks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chunks) else 'chunks', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None


def timeout_during_chuncked_readline(sock, addr):
    sock.recv(4096)
    sock.sendall(b'HTTP/1.1 200 Ok\r\nTransfer-Encoding: chunked\r\n\r\n')
    chunks = [
     'This is the data in the first chunk\r\n',
     'and this is the second one\r\n',
     'con\r\n']
    for chunk in chunks:
        sock.sendall((hex(len(chunk))[2:] + CRLF + chunk + CRLF).encode())

    gevent.sleep(2)
    sock.close()


def test_timeout_during_chuncked_readline():
    with server(timeout_during_chuncked_readline):
        client = HTTPClient(*listener, network_timeout=0.1)
        response = client.get('/')
        @py_assert0 = response['transfer-encoding']
        @py_assert3 = 'chunked'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        chunks = []
        with pytest.raises(gevent.socket.timeout):
            data = 'enter_loop'
            while data:
                data = response.readline()
                chunks.append(data)

        @py_assert2 = len(chunks)
        @py_assert5 = 3
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(chunks) if 'chunks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chunks) else 'chunks', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None