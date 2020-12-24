# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_web.py
# Compiled at: 2012-06-21 12:27:37
"""
Test web utillity functions that aren't otherwise covered.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlywebplugins.tiddlyspace.web import determine_host

def test_determine_host_common_port():
    server_host = {}
    config = {'server_host': server_host}
    environ = {'tiddlyweb.config': config}
    server_host.update({'scheme': 'http', 
       'host': 'example.com', 
       'port': '80'})
    http_host, host_url = determine_host(environ)
    @py_assert2 = 'example.com'
    @py_assert1 = http_host == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (http_host, @py_assert2)) % {'py0': @pytest_ar._saferepr(http_host) if 'http_host' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(http_host) else 'http_host', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 'example.com'
    @py_assert1 = host_url == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (host_url, @py_assert2)) % {'py0': @pytest_ar._saferepr(host_url) if 'host_url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(host_url) else 'host_url', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    environ['HTTP_HOST'] = 'something.example.com'
    http_host, host_url = determine_host(environ)
    @py_assert2 = 'something.example.com'
    @py_assert1 = http_host == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (http_host, @py_assert2)) % {'py0': @pytest_ar._saferepr(http_host) if 'http_host' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(http_host) else 'http_host', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 'example.com'
    @py_assert1 = host_url == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (host_url, @py_assert2)) % {'py0': @pytest_ar._saferepr(host_url) if 'host_url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(host_url) else 'host_url', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    server_host['port'] = '443'
    http_host, host_url = determine_host(environ)
    @py_assert2 = 'something.example.com'
    @py_assert1 = http_host == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (http_host, @py_assert2)) % {'py0': @pytest_ar._saferepr(http_host) if 'http_host' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(http_host) else 'http_host', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 'example.com'
    @py_assert1 = host_url == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (host_url, @py_assert2)) % {'py0': @pytest_ar._saferepr(host_url) if 'host_url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(host_url) else 'host_url', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    environ['HTTP_HOST'] = 'something.example.com:8080'
    server_host['port'] = '8080'
    http_host, host_url = determine_host(environ)
    @py_assert2 = 'something.example.com:8080'
    @py_assert1 = http_host == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (http_host, @py_assert2)) % {'py0': @pytest_ar._saferepr(http_host) if 'http_host' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(http_host) else 'http_host', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 'example.com:8080'
    @py_assert1 = host_url == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (host_url, @py_assert2)) % {'py0': @pytest_ar._saferepr(host_url) if 'host_url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(host_url) else 'host_url', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    environ['HTTP_HOST'] = 'something.example.com:8080'
    server_host['port'] = '80'
    http_host, host_url = determine_host(environ)
    @py_assert2 = 'something.example.com:8080'
    @py_assert1 = http_host == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (http_host, @py_assert2)) % {'py0': @pytest_ar._saferepr(http_host) if 'http_host' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(http_host) else 'http_host', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 'example.com'
    @py_assert1 = host_url == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (host_url, @py_assert2)) % {'py0': @pytest_ar._saferepr(host_url) if 'host_url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(host_url) else 'host_url', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    environ['HTTP_HOST'] = 'something.example.com:80'
    server_host['port'] = '80'
    http_host, host_url = determine_host(environ)
    @py_assert2 = 'something.example.com'
    @py_assert1 = http_host == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (http_host, @py_assert2)) % {'py0': @pytest_ar._saferepr(http_host) if 'http_host' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(http_host) else 'http_host', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 'example.com'
    @py_assert1 = host_url == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (host_url, @py_assert2)) % {'py0': @pytest_ar._saferepr(host_url) if 'host_url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(host_url) else 'host_url', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return