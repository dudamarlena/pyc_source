# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_space_uri.py
# Compiled at: 2010-11-24 00:13:20
"""
Test that space_uri generates the correct URI for a space.
This _does_not_ check for a correct space when an alien_domain
is involved, because we don't have support for that yet.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlywebplugins.tiddlyspace.spaces import space_uri

def testspace_uri():
    environ = {}
    environ['tiddlyweb.config'] = {}
    environ['tiddlyweb.config']['server_host'] = {'host': 'example.com', 
       'scheme': 'http', 
       'port': '8080'}
    server_host = environ['tiddlyweb.config']['server_host']
    space_name = 'howdy'
    @py_assert3 = space_uri(environ, space_name)
    @py_assert6 = 'http://howdy.example.com:8080/'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(space_uri) if 'space_uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space_uri) else 'space_uri', 'py1': @pytest_ar._saferepr(environ) if 'environ' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(environ) else 'environ', 'py2': @pytest_ar._saferepr(space_name) if 'space_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space_name) else 'space_name', 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    server_host['port'] = '80'
    @py_assert3 = space_uri(environ, space_name)
    @py_assert6 = 'http://howdy.example.com/'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(space_uri) if 'space_uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space_uri) else 'space_uri', 'py1': @pytest_ar._saferepr(environ) if 'environ' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(environ) else 'environ', 'py2': @pytest_ar._saferepr(space_name) if 'space_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space_name) else 'space_name', 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    server_host['port'] = '443'
    server_host['scheme'] = 'https'
    @py_assert3 = space_uri(environ, space_name)
    @py_assert6 = 'https://howdy.example.com/'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(space_uri) if 'space_uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space_uri) else 'space_uri', 'py1': @pytest_ar._saferepr(environ) if 'environ' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(environ) else 'environ', 'py2': @pytest_ar._saferepr(space_name) if 'space_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space_name) else 'space_name', 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    server_host['port'] = '9443'
    @py_assert3 = space_uri(environ, space_name)
    @py_assert6 = 'https://howdy.example.com:9443/'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(space_uri) if 'space_uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space_uri) else 'space_uri', 'py1': @pytest_ar._saferepr(environ) if 'environ' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(environ) else 'environ', 'py2': @pytest_ar._saferepr(space_name) if 'space_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space_name) else 'space_name', 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    return