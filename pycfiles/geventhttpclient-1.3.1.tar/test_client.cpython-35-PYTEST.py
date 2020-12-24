# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gwik/dev/geventhttpclient/src/geventhttpclient/tests/test_client.py
# Compiled at: 2016-08-11 17:29:44
# Size of source mod 2**32: 8578 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys, tempfile, pytest, json
from contextlib import contextmanager
from geventhttpclient import HTTPClient
from gevent.ssl import SSLError
import gevent.pool, gevent.server, gevent.pywsgi
from six.moves import xrange
listener = ('127.0.0.1', 54323)

@contextmanager
def server(handler):
    server = gevent.server.StreamServer(listener, handle=handler)
    server.start()
    try:
        yield
    finally:
        server.stop()


@contextmanager
def wsgiserver(handler):
    server = gevent.pywsgi.WSGIServer(('127.0.0.1', 54323), handler)
    server.start()
    try:
        yield
    finally:
        server.stop()


def test_client_simple():
    client = HTTPClient('www.google.fr')
    @py_assert1 = client.port
    @py_assert4 = 80
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(client) if 'client' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(client) else 'client', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    response = client.get('/')
    @py_assert1 = response.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    body = response.read()
    @py_assert2 = len(body)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(body) if 'body' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(body) else 'body', 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None


def test_client_without_leading_slash():
    client = HTTPClient('www.google.fr')
    with client.get('') as (response):
        @py_assert1 = response.status_code
        @py_assert4 = 200
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
    with client.get('maps') as (response):
        @py_assert1 = response.status_code
        @py_assert4 = (200, 301, 302)
        @py_assert3 = @py_assert1 in @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} in %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None


test_headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17'}

def test_client_with_default_headers():
    client = HTTPClient.from_url('www.google.fr/', headers=test_headers)


def test_request_with_headers():
    client = HTTPClient('www.google.fr')
    response = client.get('/', headers=test_headers)
    @py_assert1 = response.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


client = HTTPClient('www.heise.de')
raw_req_cmp = client._build_request('GET', '/tp/')

def test_build_request_relative_uri():
    raw_req = client._build_request('GET', 'tp/')
    @py_assert1 = raw_req == raw_req_cmp
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (raw_req, raw_req_cmp)) % {'py0': @pytest_ar._saferepr(raw_req) if 'raw_req' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raw_req) else 'raw_req', 'py2': @pytest_ar._saferepr(raw_req_cmp) if 'raw_req_cmp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raw_req_cmp) else 'raw_req_cmp'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_build_request_absolute_uri():
    raw_req = client._build_request('GET', '/tp/')
    @py_assert1 = raw_req == raw_req_cmp
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (raw_req, raw_req_cmp)) % {'py0': @pytest_ar._saferepr(raw_req) if 'raw_req' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raw_req) else 'raw_req', 'py2': @pytest_ar._saferepr(raw_req_cmp) if 'raw_req_cmp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raw_req_cmp) else 'raw_req_cmp'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_build_request_full_url():
    raw_req = client._build_request('GET', 'http://www.heise.de/tp/')
    @py_assert1 = raw_req == raw_req_cmp
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (raw_req, raw_req_cmp)) % {'py0': @pytest_ar._saferepr(raw_req) if 'raw_req' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raw_req) else 'raw_req', 'py2': @pytest_ar._saferepr(raw_req_cmp) if 'raw_req_cmp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raw_req_cmp) else 'raw_req_cmp'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_build_request_invalid_host():
    with pytest.raises(ValueError):
        client._build_request('GET', 'http://www.spiegel.de/')


def test_response_context_manager():
    client = HTTPClient.from_url('http://www.google.fr/')
    r = None
    with client.get('/') as (response):
        @py_assert1 = response.status_code
        @py_assert4 = 200
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        r = response
    @py_assert1 = r._sock
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._sock\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.skipif(os.environ.get('TRAVIS') == 'true', reason='We have issues on travis with the SSL tests')
def test_client_ssl():
    client = HTTPClient('www.google.fr', ssl=True)
    @py_assert1 = client.port
    @py_assert4 = 443
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(client) if 'client' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(client) else 'client', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    response = client.get('/')
    @py_assert1 = response.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    body = response.read()
    @py_assert2 = len(body)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(body) if 'body' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(body) else 'body', 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None


@pytest.mark.skipif(sys.version_info < (2, 7) and os.environ.get('TRAVIS') == 'true', reason='We have issues on travis with the SSL tests')
def test_ssl_fail_invalid_certificate():
    certs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'oncert.pem')
    client = HTTPClient('www.google.fr', ssl_options={'ca_certs': certs})
    @py_assert1 = client.port
    @py_assert4 = 443
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(client) if 'client' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(client) else 'client', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    with pytest.raises(SSLError):
        client.get('/')


def test_multi_queries_greenlet_safe():
    client = HTTPClient('www.google.fr', concurrency=3)
    group = gevent.pool.Group()
    event = gevent.event.Event()

    def run(i):
        event.wait()
        response = client.get('/')
        return (response, response.read())

    count = 0
    gevent.spawn_later(0.2, event.set)
    for response, content in group.imap_unordered(run, xrange(5)):
        @py_assert1 = response.status_code
        @py_assert4 = 200
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert2 = len(content)
        if not @py_assert2:
            @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content', 'py3': @pytest_ar._saferepr(@py_assert2)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert2 = None
        count += 1

    @py_assert2 = 5
    @py_assert1 = count == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (count, @py_assert2)) % {'py0': @pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


class StreamTestIterator(object):

    def __init__(self, sep, count):
        lines = [json.dumps({'index': i, 'title': 'this is line %d' % i}) for i in xrange(0, count)]
        self.buf = (sep.join(lines) + sep).encode()

    def __len__(self):
        return len(self.buf)

    def __iter__(self):
        self.cursor = 0
        return self

    def next(self):
        if self.cursor >= len(self.buf):
            raise StopIteration()
        gevent.sleep(0)
        pos = self.cursor + 10
        data = self.buf[self.cursor:pos]
        self.cursor = pos
        return data

    def __next__(self):
        return self.next()


def readline_iter(sock, addr):
    sock.recv(1024)
    iterator = StreamTestIterator('\n', 100)
    sock.sendall(b'HTTP/1.1 200 Ok\r\nConnection: close\r\n\r\n')
    for block in iterator:
        sock.sendall(block)


def test_readline():
    with server(readline_iter):
        client = HTTPClient(*listener, block_size=1)
        response = client.get('/')
        lines = []
        while True:
            line = response.readline(b'\n')
            if not line:
                break
            data = json.loads(line[:-1].decode())
            lines.append(data)

        @py_assert2 = len(lines)
        @py_assert5 = 100
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = [x['index'] for x in lines]
        @py_assert3 = [x for x in range(0, 100)]
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None


def readline_multibyte_sep(sock, addr):
    sock.recv(1024)
    iterator = StreamTestIterator('\r\n', 100)
    sock.sendall(b'HTTP/1.1 200 Ok\r\nConnection: close\r\n\r\n')
    for block in iterator:
        sock.sendall(block)


def test_readline_multibyte_sep():
    with server(readline_multibyte_sep):
        client = HTTPClient(*listener, block_size=1)
        response = client.get('/')
        lines = []
        while True:
            line = response.readline(b'\r\n')
            if not line:
                break
            data = json.loads(line[:-1].decode())
            lines.append(data)

        @py_assert2 = len(lines)
        @py_assert5 = 100
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = [x['index'] for x in lines]
        @py_assert3 = [x for x in range(0, 100)]
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None


def readline_multibyte_splitsep(sock, addr):
    sock.recv(1024)
    sock.sendall(b'HTTP/1.1 200 Ok\r\nConnection: close\r\n\r\n')
    sock.sendall(b'{"a": 1}\r')
    gevent.sleep(0)
    sock.sendall(b'\n{"a": 2}\r\n{"a": 3}\r\n')


def test_readline_multibyte_splitsep():
    with server(readline_multibyte_splitsep):
        client = HTTPClient(*listener, block_size=1)
        response = client.get('/')
        lines = []
        last_index = 0
        while True:
            line = response.readline(b'\r\n')
            if not line:
                break
            data = json.loads(line[:-2].decode())
            @py_assert0 = data['a']
            @py_assert4 = 1
            @py_assert6 = last_index + @py_assert4
            @py_assert2 = @py_assert0 == @py_assert6
            if not @py_assert2:
                @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == (%(py3)s + %(py5)s)', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(last_index) if 'last_index' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(last_index) else 'last_index'}
                @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
            last_index = data['a']

        len(lines) == 3


def internal_server_error(sock, addr):
    sock.recv(1024)
    head = 'HTTP/1.1 500 Internal Server Error\r\nConnection: close\r\nContent-Type: text/html\r\nContent-Length: 135\r\n\r\n'
    body = '<html>\n  <head>\n    <title>Internal Server Error</title>\n  </head>\n  <body>\n    <h1>Internal Server Error</h1>\n    \n  </body>\n</html>\n\n'
    sock.sendall((head + body).encode())
    sock.close()


def test_internal_server_error():
    with server(internal_server_error):
        client = HTTPClient(*listener)
        response = client.get('/')
        @py_assert1 = response.should_keep_alive
        @py_assert3 = @py_assert1()
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.should_keep_alive\n}()\n}') % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = response.should_close
        @py_assert3 = @py_assert1()
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.should_close\n}()\n}') % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
        body = response.read()
        @py_assert2 = len(body)
        @py_assert6 = response.content_length
        @py_assert4 = @py_assert2 == @py_assert6
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py7)s\n{%(py7)s = %(py5)s.content_length\n}', ), (@py_assert2, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(body) if 'body' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(body) else 'body', 'py5': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None


def check_upload(body, body_length):

    def wsgi_handler(env, start_response):
        @py_assert2 = env.get
        @py_assert4 = 'CONTENT_LENGTH'
        @py_assert6 = @py_assert2(@py_assert4)
        @py_assert8 = int(@py_assert6)
        @py_assert10 = @py_assert8 == body_length
        if not @py_assert10:
            @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}(%(py5)s)\n})\n} == %(py11)s',), (@py_assert8, body_length)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py1': @pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(body_length) if 'body_length' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(body_length) else 'body_length'}
            @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
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


def test_file_post():
    body = tempfile.NamedTemporaryFile('a+b', delete=False)
    name = body.name
    try:
        body.write(b'123456789')
        body.close()
        with wsgiserver(check_upload(b'123456789', 9)):
            client = HTTPClient(*listener)
            with open(name, 'rb') as (body):
                client.post('/', body)
    finally:
        os.remove(name)


def test_bytes_post():
    with wsgiserver(check_upload(b'12345', 5)):
        client = HTTPClient(*listener)
        client.post('/', b'12345')


def test_string_post():
    with wsgiserver(check_upload('12345', 5)):
        client = HTTPClient(*listener)
        client.post('/', '12345')


def test_unicode_post():
    byte_string = b'\xc8\xb9\xc8\xbc\xc9\x85'
    unicode_string = byte_string.decode('utf-8')
    with wsgiserver(check_upload(byte_string, len(byte_string))):
        client = HTTPClient(*listener)
        client.post('/', unicode_string)