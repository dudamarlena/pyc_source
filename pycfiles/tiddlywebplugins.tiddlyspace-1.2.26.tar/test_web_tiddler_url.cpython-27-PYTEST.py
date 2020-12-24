# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_web_tiddler_url.py
# Compiled at: 2013-08-20 13:22:51
"""
Watch out for presentation bugs with bags that are not
considered valid.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlywebplugins.tiddlyspace.fixups import web_tiddler_url
from tiddlyweb.model.tiddler import Tiddler
ENVIRON = {'tiddlyweb.config': {'server_host': {'host': 'tiddlyspace.com', 
                                        'port': '80'}}, 
   'HTTP_HOST': 'tapas.tiddlyspace.com', 
   'wsgi.url_scheme': 'http'}

def test_space_bag():
    tiddler = Tiddler('monkey', 'tapas_public')
    uri = web_tiddler_url(ENVIRON, tiddler)
    @py_assert2 = 'http://tapas.tiddlyspace.com/bags/tapas_public/tiddlers/monkey'
    @py_assert1 = uri == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (uri, @py_assert2)) % {'py0': @pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_nonspace_bag():
    tiddler = Tiddler('monkey', 'tapas_extra')
    uri = web_tiddler_url(ENVIRON, tiddler)
    @py_assert2 = 'http://tiddlyspace.com/bags/tapas_extra/tiddlers/monkey'
    @py_assert1 = uri == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (uri, @py_assert2)) % {'py0': @pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_core_bag():
    tiddler = Tiddler('monkey', 'common')
    uri = web_tiddler_url(ENVIRON, tiddler)
    @py_assert2 = 'http://tiddlyspace.com/bags/common/tiddlers/monkey'
    @py_assert1 = uri == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (uri, @py_assert2)) % {'py0': @pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_friendly_space():
    tiddler = Tiddler('monkey', 'tapas_public')
    uri = web_tiddler_url(ENVIRON, tiddler, friendly=True)
    @py_assert2 = 'http://tapas.tiddlyspace.com/monkey'
    @py_assert1 = uri == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (uri, @py_assert2)) % {'py0': @pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_friendly_nonspace():
    tiddler = Tiddler('monkey', 'tapas_extra')
    uri = web_tiddler_url(ENVIRON, tiddler, friendly=True)
    @py_assert2 = 'http://tiddlyspace.com/bags/tapas_extra/tiddlers/monkey'
    @py_assert1 = uri == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (uri, @py_assert2)) % {'py0': @pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_friendly_core():
    tiddler = Tiddler('monkey', 'common')
    uri = web_tiddler_url(ENVIRON, tiddler, friendly=True)
    @py_assert2 = 'http://tiddlyspace.com/bags/common/tiddlers/monkey'
    @py_assert1 = uri == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (uri, @py_assert2)) % {'py0': @pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_friendly_port():
    ENVIRON['tiddlyweb.config']['server_host']['port'] = 8080
    tiddler = Tiddler('monkey', 'tapas_public')
    uri = web_tiddler_url(ENVIRON, tiddler, friendly=True)
    @py_assert2 = 'http://tapas.tiddlyspace.com:8080/monkey'
    @py_assert1 = uri == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (uri, @py_assert2)) % {'py0': @pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return