# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gwik/dev/geventhttpclient/src/geventhttpclient/tests/test_ssl.py
# Compiled at: 2016-08-11 17:29:44
# Size of source mod 2**32: 4085 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, six, sys
from contextlib import contextmanager
import pytest, gevent.server, gevent.socket, gevent.ssl, os
from geventhttpclient import HTTPClient
try:
    from ssl import CertificateError
except ImportError:
    from backports.ssl_match_hostname import CertificateError

pytestmark = pytest.mark.skipif(sys.version_info < (2, 7) and os.environ.get('TRAVIS') == 'true', reason='We have issues on travis with the SSL tests')
BASEDIR = os.path.dirname(__file__)
KEY = os.path.join(BASEDIR, 'server.key')
CERT = os.path.join(BASEDIR, 'server.crt')

@contextmanager
def server(handler, backlog=1):
    server = gevent.server.StreamServer(('localhost', 0), backlog=backlog, handle=handler, keyfile=KEY, certfile=CERT)
    server.start()
    try:
        yield (
         server.server_host, server.server_port)
    finally:
        server.stop()


@contextmanager
def timeout_connect_server():
    sock = gevent.socket.socket(gevent.socket.AF_INET, gevent.socket.SOCK_STREAM, 0)
    sock = gevent.ssl.wrap_socket(sock, keyfile=KEY, certfile=CERT)
    sock.setsockopt(gevent.socket.SOL_SOCKET, gevent.socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)

    def run(sock):
        conns = []
        while True:
            conn, addr = sock.accept()
            conns.append(conns)
            conn.recv(1024)
            gevent.sleep(10)

    job = gevent.spawn(run, sock)
    try:
        yield sock.getsockname()
        sock.close()
    finally:
        job.kill()


def simple_ssl_response(sock, addr):
    sock.recv(1024)
    sock.sendall(b'HTTP/1.1 200 Ok\r\nConnection: close\r\n\r\n')
    sock.close()


def test_simple_ssl():
    with server(simple_ssl_response) as (listener):
        http = HTTPClient(*listener, ssl_options={'ca_certs': CERT})
        response = http.get('/')
        @py_assert1 = response.status_code
        @py_assert4 = 200
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        response.read()


def timeout_on_connect(sock, addr):
    sock.recv(1024)
    sock.sendall(b'HTTP/1.1 200 Ok\r\nContent-Length: 0\r\n\r\n')


def test_timeout_on_connect():
    with timeout_connect_server() as (listener):
        http = HTTPClient(*listener, ssl_options={'ca_certs': CERT})

        def run(http, wait_time=100):
            try:
                response = http.get('/')
                gevent.sleep(wait_time)
                response.read()
            except Exception:
                pass

        gevent.spawn(run, http)
        gevent.sleep(0)
        e = None
        try:
            http2 = HTTPClient(*listener, ssl_options={'ca_certs': CERT})
            http2.get('/')
        except gevent.ssl.SSLError as error:
            e = error
        except gevent.socket.timeout as error:
            e = error
        except:
            raise

        @py_assert2 = None
        @py_assert1 = e is not @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (e, @py_assert2)) % {'py0': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = (@pytest_ar._format_assertmsg('should have raised') + '\n>assert %(py5)s') % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        if isinstance(e, gevent.ssl.SSLError):
            @py_assert0 = 'operation timed out'
            @py_assert5 = str(e)
            @py_assert2 = @py_assert0 in @py_assert5
            if not @py_assert2:
                @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e', 'py1': @pytest_ar._saferepr(@py_assert0), 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str'}
                @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert0 = @py_assert2 = @py_assert5 = None


def network_timeout(sock, addr):
    sock.recv(1024)
    gevent.sleep(10)
    sock.sendall(b'HTTP/1.1 200 Ok\r\nContent-Length: 0\r\n\r\n')


def test_network_timeout():
    with server(network_timeout) as (listener):
        http = HTTPClient(*listener, ssl_options={'ca_certs': CERT})
        if six.PY3:
            with pytest.raises(gevent.socket.timeout):
                response = http.get('/')
                @py_assert1 = response.status_code
                @py_assert4 = 0
                @py_assert3 = @py_assert1 == @py_assert4
                if not @py_assert3:
                    @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
                    @py_format8 = (@pytest_ar._format_assertmsg('should have timed out.') + '\n>assert %(py7)s') % {'py7': @py_format6}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format8))
                @py_assert1 = @py_assert3 = @py_assert4 = None
        else:
            with pytest.raises(gevent.ssl.SSLError):
                response = http.get('/')
                @py_assert1 = response.status_code
                @py_assert4 = 0
                @py_assert3 = @py_assert1 == @py_assert4
                if not @py_assert3:
                    @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
                    @py_format8 = (@pytest_ar._format_assertmsg('should have timed out.') + '\n>assert %(py7)s') % {'py7': @py_format6}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format8))
                @py_assert1 = @py_assert3 = @py_assert4 = None


def test_verify_hostname():
    with server(simple_ssl_response) as (listener):
        http = HTTPClient(*listener, ssl_options={'ca_certs': CERT})
        with pytest.raises(CertificateError):
            http.get('/')