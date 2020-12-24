# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gwik/dev/geventhttpclient/src/geventhttpclient/tests/test_headers.py
# Compiled at: 2016-07-05 05:26:31
# Size of source mod 2**32: 7715 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, six
from six.moves import xrange
import gevent, gevent.monkey
gevent.monkey.patch_all()
import pytest
if six.PY2:
    from cookielib import CookieJar
    from urllib2 import Request
else:
    from http.cookiejar import CookieJar
    from urllib.request import Request
import string, random, time
from geventhttpclient.response import HTTPResponse
from geventhttpclient.header import Headers
MULTI_COOKIE_RESPONSE = '\nHTTP/1.1 200 OK\nServer: nginx\nDate: Fri, 21 Sep 2012 18:49:35 GMT\nContent-Type: text/html; charset=windows-1251\nConnection: keep-alive\nX-Powered-By: PHP/5.2.17\nSet-Cookie: bb_lastvisit=1348253375; expires=Sat, 21-Sep-2013 18:49:35 GMT; path=/\nSet-Cookie: bb_lastactivity=0; expires=Sat, 21-Sep-2013 18:49:35 GMT; path=/\nCache-Control: private\nPragma: private\nSet-Cookie: bb_sessionhash=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=/\nSet-Cookie: bb_referrerid=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=/\nSet-Cookie: bb_userid=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=/\nSet-Cookie: bb_password=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=/\nSet-Cookie: bb_lastvisit=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=/\nSet-Cookie: bb_lastactivity=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=/\nSet-Cookie: bb_threadedmode=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=/\nSet-Cookie: bb_userstyleid=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=/\nSet-Cookie: bb_languageid=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=/\nSet-Cookie: bb_fbaccesstoken=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=/\nSet-Cookie: bb_fbprofilepicurl=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=/\nSet-Cookie: bb_sessionhash=abcabcabcabcabcabcabcabcabcabcab; path=/; HttpOnly\nSet-Cookie: tapatalk_redirect3=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: bb_sessionhash=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: __utma=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: __utmb=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: __utmc=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: __utmz=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: vbulletin_collapse=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: bb_referrerid=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: bb_userid=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: bb_password=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: bb_lastvisit=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: bb_lastactivity=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: bb_threadedmode=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: bb_userstyleid=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: bb_languageid=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: bb_fbaccesstoken=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nSet-Cookie: bb_fbprofilepicurl=deleted; expires=Thu, 22-Sep-2011 18:49:34 GMT; path=1; domain=forum.somewhere.com\nContent-Encoding: gzip\nContent-Length: 26186\n\n'.lstrip().replace('\n', '\r\n')

def test_create_from_kwargs():
    h = Headers(ab=1, cd=2, ef=3, gh=4)
    @py_assert2 = len(h)
    @py_assert5 = 4
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = 'ab'
    @py_assert2 = @py_assert0 in h
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, h)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_create_from_iterator():
    h = Headers((x, x * 5) for x in string.ascii_lowercase)
    @py_assert2 = len(h)
    @py_assert7 = string.ascii_lowercase
    @py_assert9 = len(@py_assert7)
    @py_assert4 = @py_assert2 == @py_assert9
    if not @py_assert4:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py10)s\n{%(py10)s = %(py5)s(%(py8)s\n{%(py8)s = %(py6)s.ascii_lowercase\n})\n}',), (@py_assert2, @py_assert9)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py6': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 
         'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = None


def test_create_from_dict():
    h = Headers(dict(ab=1, cd=2, ef=3, gh=4))
    @py_assert2 = len(h)
    @py_assert5 = 4
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = 'ab'
    @py_assert2 = @py_assert0 in h
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, h)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_create_from_list():
    h = Headers([('ab', 'A'), ('cd', 'B'), ('cookie', 'C'), ('cookie', 'D'), ('cookie', 'E')])
    @py_assert2 = len(h)
    @py_assert5 = 5
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = 'ab'
    @py_assert2 = @py_assert0 in h
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, h)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert1 = h['cookie']
    @py_assert3 = len(@py_assert1)
    @py_assert6 = 3
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = h['cookie'][0]
    @py_assert3 = 'C'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = h['cookie'][(-1)]
    @py_assert3 = 'E'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_case_insensitivity():
    h = Headers({'Content-Type': 'text/plain'})
    h.add('Content-Encoding', 'utf8')
    for val in ('content-type', 'content-encoding'):
        @py_assert1 = val.upper
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 in h
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('in',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.upper\n}()\n} in %(py6)s',), (@py_assert3, h)) % {'py0': @pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = val.lower
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 in h
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('in',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.lower\n}()\n} in %(py6)s',), (@py_assert3, h)) % {'py0': @pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = val.capitalize
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 in h
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('in',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.capitalize\n}()\n} in %(py6)s',), (@py_assert3, h)) % {'py0': @pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = h.get
        @py_assert4 = val.lower
        @py_assert6 = @py_assert4()
        @py_assert8 = @py_assert1(@py_assert6)
        @py_assert13 = h.get
        @py_assert16 = val.upper
        @py_assert18 = @py_assert16()
        @py_assert20 = @py_assert13(@py_assert18)
        @py_assert10 = @py_assert8 == @py_assert20
        @py_assert23 = h.get
        @py_assert26 = val.capitalize
        @py_assert28 = @py_assert26()
        @py_assert30 = @py_assert23(@py_assert28)
        @py_assert11 = @py_assert20 == @py_assert30
        if not (@py_assert10 and @py_assert11):
            @py_format32 = @pytest_ar._call_reprcompare(('==', '=='), (@py_assert10, @py_assert11), ('%(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.get\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.lower\n}()\n})\n} == %(py21)s\n{%(py21)s = %(py14)s\n{%(py14)s = %(py12)s.get\n}(%(py19)s\n{%(py19)s = %(py17)s\n{%(py17)s = %(py15)s.upper\n}()\n})\n}', '%(py21)s\n{%(py21)s = %(py14)s\n{%(py14)s = %(py12)s.get\n}(%(py19)s\n{%(py19)s = %(py17)s\n{%(py17)s = %(py15)s.upper\n}()\n})\n} == %(py31)s\n{%(py31)s = %(py24)s\n{%(py24)s = %(py22)s.get\n}(%(py29)s\n{%(py29)s = %(py27)s\n{%(py27)s = %(py25)s.capitalize\n}()\n})\n}'), (@py_assert8, @py_assert20, @py_assert30)) % {'py17': @pytest_ar._saferepr(@py_assert16), 'py14': @pytest_ar._saferepr(@py_assert13), 'py19': @pytest_ar._saferepr(@py_assert18), 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py24': @pytest_ar._saferepr(@py_assert23), 'py31': @pytest_ar._saferepr(@py_assert30), 'py29': @pytest_ar._saferepr(@py_assert28), 'py7': @pytest_ar._saferepr(@py_assert6), 'py21': @pytest_ar._saferepr(@py_assert20), 'py0': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py22': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py3': @pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val', 'py9': @pytest_ar._saferepr(@py_assert8), 'py27': @pytest_ar._saferepr(@py_assert26), 'py12': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py15': @pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val', 'py25': @pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val'}
            @py_format34 = ('' + 'assert %(py33)s') % {'py33': @py_format32}
            raise AssertionError(@pytest_ar._format_explanation(@py_format34))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert23 = @py_assert26 = @py_assert28 = @py_assert30 = None
        del h[val.upper()]
        @py_assert1 = val.lower
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 not in h
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('not in',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.lower\n}()\n} not in %(py6)s',), (@py_assert3, h)) % {'py0': @pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None


def test_read_multiple_header():
    parser = HTTPResponse()
    parser.feed(MULTI_COOKIE_RESPONSE)
    headers = parser._headers_index
    @py_assert1 = headers['set-cookie']
    @py_assert3 = len(@py_assert1)
    @py_assert7 = MULTI_COOKIE_RESPONSE.count
    @py_assert9 = 'Set-Cookie'
    @py_assert11 = @py_assert7(@py_assert9)
    @py_assert5 = @py_assert3 == @py_assert11
    if not @py_assert5:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py6)s.count\n}(%(py10)s)\n}', ), (@py_assert3, @py_assert11)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(MULTI_COOKIE_RESPONSE) if 'MULTI_COOKIE_RESPONSE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MULTI_COOKIE_RESPONSE) else 'MULTI_COOKIE_RESPONSE', 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3), 'py12': @pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert0 = headers['set-cookie'][0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'bb_lastvisit'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = headers['set-cookie'][(-1)]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'bb_fbprofilepicurl'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_cookielib_compatibility():
    cj = CookieJar()
    cj._now = cj._policy._now = time.mktime((2012, 1, 1, 0, 0, 0, 0, 0, 0))
    request = Request('http://test.com')
    parser = HTTPResponse()
    parser.feed(MULTI_COOKIE_RESPONSE)
    cookies = cj.make_cookies(parser, request)
    for cookie in cookies:
        if cj._policy.set_ok(cookie, request):
            cj.set_cookie(cookie)

    @py_assert3 = list(cj)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(cj) if 'cj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cj) else 'cj', 'py9': @pytest_ar._saferepr(@py_assert8), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_compatibility_with_previous_API_read():
    parser = HTTPResponse()
    parser.feed(MULTI_COOKIE_RESPONSE)
    for single_item in ('content-encoding', 'content-type', 'content-length', 'cache-control', 'connection'):
        @py_assert1 = parser[single_item]
        @py_assert4 = six.string_types
        @py_assert6 = isinstance(@py_assert1, @py_assert4)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py2)s, %(py5)s\n{%(py5)s = %(py3)s.string_types\n})\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py3': @pytest_ar._saferepr(six) if 'six' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(six) else 'six', 'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert4 = @py_assert6 = None
        @py_assert2 = parser.get
        @py_assert5 = @py_assert2(single_item)
        @py_assert8 = six.string_types
        @py_assert10 = isinstance(@py_assert5, @py_assert8)
        if not @py_assert10:
            @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}(%(py4)s)\n}, %(py9)s\n{%(py9)s = %(py7)s.string_types\n})\n}') % {'py7': @pytest_ar._saferepr(six) if 'six' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(six) else 'six', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py1': @pytest_ar._saferepr(parser) if 'parser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parser) else 'parser', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2), 'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(single_item) if 'single_item' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_item) else 'single_item'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert2 = @py_assert5 = @py_assert8 = @py_assert10 = None


def test_compatibility_with_previous_API_write():
    h = Headers()
    h['asdf'] = 'jklm'
    h['asdf'] = 'dfdf'
    @py_assert0 = h['asdf']
    @py_assert3 = 'dfdf'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_copy():
    rnd_txt = lambda length: ''.join(random.choice(string.ascii_letters) for _ in xrange(length))
    h = Headers((rnd_txt(10), rnd_txt(50)) for _ in xrange(100))
    c = h.copy()
    @py_assert1 = h is not c
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is not',), (@py_assert1,), ('%(py0)s is not %(py2)s',), (h, c)) % {'py0': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py2': @pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c'}
        @py_format5 = ('' + 'assert %(py4)s') % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert2 = len(h)
    @py_assert7 = len(c)
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}',), (@py_assert2, @py_assert7)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py6': @pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 
         'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert2 = h.keys
    @py_assert4 = @py_assert2()
    @py_assert6 = set(@py_assert4)
    @py_assert11 = c.keys
    @py_assert13 = @py_assert11()
    @py_assert15 = set(@py_assert13)
    @py_assert8 = @py_assert6 == @py_assert15
    if not @py_assert8:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} == %(py16)s\n{%(py16)s = %(py9)s(%(py14)s\n{%(py14)s = %(py12)s\n{%(py12)s = %(py10)s.keys\n}()\n})\n}',), (@py_assert6, @py_assert15)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py14': @pytest_ar._saferepr(@py_assert13), 'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py1': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py16': @pytest_ar._saferepr(@py_assert15), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 
         'py10': @pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c', 'py12': @pytest_ar._saferepr(@py_assert11)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert1 = h == c
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py2)s',), (h, c)) % {'py0': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py2': @pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c'}
        @py_format5 = ('' + 'assert %(py4)s') % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert2 = type(h)
    @py_assert7 = type(c)
    @py_assert4 = @py_assert2 is @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('is',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} is %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}',), (@py_assert2, @py_assert7)) % {'py0': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type', 'py1': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py6': @pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type', 
         'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    for _ in xrange(100):
        rnd_key = rnd_txt(9)
        c[rnd_key] = rnd_txt(10)
        @py_assert1 = rnd_key in c
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py2)s',), (rnd_key, c)) % {'py0': @pytest_ar._saferepr(rnd_key) if 'rnd_key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rnd_key) else 'rnd_key', 'py2': @pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c'}
            @py_format5 = ('' + 'assert %(py4)s') % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert1 = rnd_key not in h
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('not in',), (@py_assert1,), ('%(py0)s not in %(py2)s',), (rnd_key, h)) % {'py0': @pytest_ar._saferepr(rnd_key) if 'rnd_key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rnd_key) else 'rnd_key', 'py2': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h'}
            @py_format5 = ('' + 'assert %(py4)s') % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None


def test_fieldname_string_enforcement():
    with pytest.raises(Exception):
        Headers({3: 3})
    h = Headers()
    with pytest.raises(Exception):
        h[3] = 5
    with pytest.raises(Exception):
        h.add(3, 4)
    with pytest.raises(Exception):
        del h[3]


def test_header_replace():
    d = {}
    d['Content-Type'] = 'text/plain'
    d['content-type'] = 'text/html'
    @py_assert0 = d['content-type']
    @py_assert3 = 'text/html'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_compat_dict():
    h = Headers(D='asdf')
    h.add('E', 'd')
    h.add('E', 'f')
    h.add('Cookie', 'd')
    h.add('Cookie', 'e')
    h.add('Cookie', 'f')
    d = h.compatible_dict()
    for x in ('Cookie', 'D', 'E'):
        @py_assert1 = x in d
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (x, d)) % {'py0': @pytest_ar._saferepr(x) if 'x' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(x) else 'x', 'py2': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    @py_assert0 = d['D']
    @py_assert3 = 'asdf'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = d['E']
    @py_assert3 = 'd, f'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = d['Cookie']
    @py_assert3 = 'd, e, f'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


if __name__ == '__main__':
    test_copy()
    test_compat_dict()
    test_cookielib_compatibility()