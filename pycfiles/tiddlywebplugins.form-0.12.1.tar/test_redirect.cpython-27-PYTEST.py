# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.form/test/test_redirect.py
# Compiled at: 2014-05-21 17:45:45
"""
tests to ensure that the optional redirect works properly
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from setup_test import setup_store, setup_web
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.config import config
import httplib2
config['system_plugins'] = [
 'tiddlywebplugins.form']

def test_post_redirect():
    """
    add a tiddler, specifying a url to redirect to on success
    """
    store = setup_store()
    setup_web()
    http = httplib2.Http()
    http.follow_redirects = False
    response = http.request('http://test_domain:8001/recipes/foobar/tiddlers?redirect=/bags/foo/tiddlers', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body='title=HelloWorld&text=Hi%20There')[0]
    @py_assert1 = response.status
    @py_assert4 = 303
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['location'].split('?')[0]
    @py_assert3 = '/bags/foo/tiddlers'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    tiddler = Tiddler('HelloWorld', 'bar')
    try:
        store.get(tiddler)
    except NoTiddlerError:
        raise AssertionError('tiddler was not put into store')

    @py_assert1 = tiddler.title
    @py_assert4 = 'HelloWorld'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.text
    @py_assert4 = 'Hi There'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.fields
    @py_assert3 = @py_assert1.get
    @py_assert5 = 'redirect'
    @py_assert8 = @py_assert3(@py_assert5, None)
    @py_assert10 = @py_assert8 == None
    if not @py_assert10:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.fields\n}.get\n}(%(py6)s, %(py7)s)\n} == %(py11)s',), (@py_assert8, None)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py7': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None
    return


def test_post_redirect_in_body():
    """
    add a tiddler, specifying a url to redirect to in the body of the post
    """
    store = setup_store()
    setup_web()
    http = httplib2.Http()
    http.follow_redirects = False
    response = http.request('http://test_domain:8001/recipes/foobar/tiddlers', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body='title=HelloWorld&text=Hi%20There&redirect=/bags/foo/tiddlers')[0]
    @py_assert1 = response.status
    @py_assert4 = 303
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['location'].split('?')[0]
    @py_assert3 = '/bags/foo/tiddlers'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    tiddler = Tiddler('HelloWorld', 'bar')
    tiddler = store.get(tiddler)
    @py_assert1 = tiddler.title
    @py_assert4 = 'HelloWorld'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.text
    @py_assert4 = 'Hi There'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.fields
    @py_assert3 = @py_assert1.get
    @py_assert5 = 'redirect'
    @py_assert8 = @py_assert3(@py_assert5, None)
    @py_assert10 = @py_assert8 == None
    if not @py_assert10:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.fields\n}.get\n}(%(py6)s, %(py7)s)\n} == %(py11)s',), (@py_assert8, None)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py7': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None
    return


def test_unicode_redirect():
    """
    redirect to a unicode url
    """
    store = setup_store()
    setup_web()
    http = httplib2.Http()
    http.follow_redirects = False
    response = http.request('http://test_domain:8001/recipes/foobar/tiddlers?redirect=/bags/foo/tiddlers/%E2%82%AC%E2%88%91%C2%AA%C2%A8~%C3%9F', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body='title=HelloWorld&text=Hi%20There')[0]
    @py_assert1 = response.status
    @py_assert4 = 303
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return