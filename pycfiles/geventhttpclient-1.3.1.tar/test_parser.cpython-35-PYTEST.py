# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gwik/dev/geventhttpclient/src/geventhttpclient/tests/test_parser.py
# Compiled at: 2016-07-05 05:26:31
# Size of source mod 2**32: 4201 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, six
from geventhttpclient.response import HTTPResponse
if six.PY3:
    from http.client import HTTPException
    from io import StringIO
else:
    from httplib import HTTPException
    from cStringIO import StringIO
import pytest
from functools import wraps
import sys
from six.moves import xrange
RESPONSE = 'HTTP/1.1 301 Moved Permanently\r\nLocation: http://www.google.fr/\r\nContent-Type: text/html; charset=UTF-8\r\nDate: Thu, 13 Oct 2011 15:03:12 GMT\r\nExpires: Sat, 12 Nov 2011 15:03:12 GMT\r\nCache-Control: public, max-age=2592000\r\nServer: gws\r\nContent-Length: 218\r\nX-XSS-Protection: 1; mode=block\r\n\r\n<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">\n<TITLE>301 Moved</TITLE></HEAD><BODY>\n<H1>301 Moved</H1>\nThe document has moved\n<A HREF="http://www.google.fr/">here</A>.\r\n</BODY></HTML>\r\n'
gettotalrefcount = getattr(sys, 'gettotalrefcount', None)

def wrap_refcount(method):
    if gettotalrefcount is None:
        return method

    @wraps(method)
    def wrapped(*args, **kwargs):
        import gc
        gc.disable()
        gc.collect()
        deltas = []
        d = None
        try:
            for _ in xrange(4):
                d = gettotalrefcount()
                method(*args, **kwargs)
                if 'urlparse' in sys.modules:
                    sys.modules['urlparse'].clear_cache()
                d = gettotalrefcount() - d
                deltas.append(d)
                if deltas[(-1)] == 0:
                    break
            else:
                raise AssertionError('refcount increased by %r' % (deltas,))

        finally:
            gc.collect()
            gc.enable()

    return wrapped


@wrap_refcount
def test_parse():
    parser = HTTPResponse()
    @py_assert1 = parser.feed
    @py_assert4 = @py_assert1(RESPONSE)
    if not @py_assert4:
        @py_format6 = (@pytest_ar._format_assertmsg(len(RESPONSE)) + '\n>assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.feed\n}(%(py3)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py3': @pytest_ar._saferepr(RESPONSE) if 'RESPONSE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(RESPONSE) else 'RESPONSE', 'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    @py_assert1 = parser.message_begun
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.message_begun\n}') % {'py0': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = parser.headers_complete
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.headers_complete\n}') % {'py0': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = parser.message_complete
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.message_complete\n}') % {'py0': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None


@wrap_refcount
def test_parse_small_blocks():
    parser = HTTPResponse()
    parser.feed(RESPONSE)
    response = StringIO(RESPONSE)
    while not parser.message_complete:
        data = response.read(10)
        parser.feed(data)

    @py_assert1 = parser.message_begun
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.message_begun\n}') % {'py0': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = parser.headers_complete
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.headers_complete\n}') % {'py0': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = parser.message_complete
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.message_complete\n}') % {'py0': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = parser.should_keep_alive
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.should_keep_alive\n}()\n}') % {'py0': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = parser.status_code
    @py_assert4 = 301
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = parser.items
    @py_assert4 = @py_assert2()
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = [
     ('cache-control', 'public, max-age=2592000'), ('content-length', '218'), ('content-type', 'text/html; charset=UTF-8'), ('date', 'Thu, 13 Oct 2011 15:03:12 GMT'), ('expires', 'Sat, 12 Nov 2011 15:03:12 GMT'), ('location', 'http://www.google.fr/'), ('server', 'gws'), ('x-xss-protection', '1; mode=block')]
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.items\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


@wrap_refcount
def test_parse_error():
    response = HTTPResponse()
    try:
        response.feed('HTTP/1.1 asdf\r\n\r\n')
        response.feed('')
        @py_assert1 = response.status_code
        if not @py_assert1:
            @py_format3 = (@pytest_ar._format_assertmsg(0) + '\n>assert %(py2)s\n{%(py2)s = %(py0)s.status_code\n}') % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None
        @py_assert1 = response.message_begun
        if not @py_assert1:
            @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.message_begun\n}') % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None
    except HTTPException as e:
        @py_assert0 = 'invalid HTTP status code'
        @py_assert5 = str(e)
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py4': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e', 'py1': @pytest_ar._saferepr(@py_assert0), 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
    else:
        @py_assert0 = False
        if not @py_assert0:
            @py_format2 = (@pytest_ar._format_assertmsg('should have raised') + '\n>assert %(py1)s') % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None


@wrap_refcount
def test_incomplete_response():
    response = HTTPResponse()
    response.feed('HTTP/1.1 200 Ok\r\nContent-Length:10\r\n\r\n1')
    with pytest.raises(HTTPException):
        response.feed('')
    @py_assert1 = response.should_keep_alive
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.should_keep_alive\n}()\n}') % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = response.should_close
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.should_close\n}()\n}') % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


@wrap_refcount
def test_response_too_long():
    response = HTTPResponse()
    data = 'HTTP/1.1 200 Ok\r\nContent-Length:1\r\n\r\ntoolong'
    with pytest.raises(HTTPException):
        response.feed(data)


@wrap_refcount
def test_on_body_raises():
    response = HTTPResponse()

    def on_body(buf):
        raise RuntimeError('error')

    response._on_body = on_body
    with pytest.raises(RuntimeError):
        response.feed(RESPONSE)


@wrap_refcount
def test_on_message_begin():
    response = HTTPResponse()

    def on_message_begin():
        raise RuntimeError('error')

    response._on_message_begin = on_message_begin
    with pytest.raises(RuntimeError):
        response.feed(RESPONSE)