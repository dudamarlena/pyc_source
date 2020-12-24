# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.virtualhosting/test/test_simple.py
# Compiled at: 2011-05-16 08:03:34
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, tiddlywebplugins.virtualhosting
from tiddlyweb.web.util import server_host_url
from tiddlyweb.config import config

def test_http_host():
    environ = {'tiddlyweb.config': config}
    url = server_host_url(environ)
    @py_assert2 = 'http://0.0.0.0:8080'
    @py_assert1 = url == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (url, @py_assert2)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() is not @py_builtins.globals() else 'url', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    environ['HTTP_HOST'] = 'fancy.virtual.domain:9090'
    environ['wsgi.url_scheme'] = 'https'
    url = server_host_url(environ)
    @py_assert2 = 'https://fancy.virtual.domain:9090'
    @py_assert1 = url == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (url, @py_assert2)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() is not @py_builtins.globals() else 'url', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return