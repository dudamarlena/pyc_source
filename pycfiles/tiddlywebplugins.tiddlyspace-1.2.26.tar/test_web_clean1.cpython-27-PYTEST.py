# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_web_clean1.py
# Compiled at: 2013-08-20 13:22:51
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from test.fixtures import make_test_env, make_fake_space, get_auth
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2, simplejson
from tiddlywebplugins.templates import rfc3339, format_modified
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.web.util import encode_name

def setup_module(module):
    make_test_env(module)
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('thing.0.0.0.0', 8080, app_fn)
    make_fake_space(store, 'thing')
    tiddler = Tiddler('ServerSettings', 'thing_public')
    tiddler.text = 'htmltemplate: clean1\n'
    store.put(tiddler)
    tiddler = Tiddler('TestMe', 'thing_public')
    tiddler.text = '# Hi\n\n# one\n# two'
    tiddler.tags = ['alpha', 'beta', '12th monkey']
    store.put(tiddler)
    module.tiddler_modified = tiddler.modified
    module.http = httplib2.Http()


def test_clean1_present():
    match_tiddlers('clean1 template')


def test_clean1_no_core():
    match_tiddlers('TiddlyWebAdaptors', neg=True)


def test_tiddler_modified():
    rfc_time = rfc3339(tiddler_modified)
    http_time = format_modified(tiddler_modified)
    match_tiddler('TestMe', '<time class="modified" datetime="%s">%s</time>' % (
     rfc_time, http_time))


def test_tag_list():
    match_tiddler('TestMe', '<ul class="tags">')
    tiddler = Tiddler('TestMe2', 'thing_public')
    tiddler.text = '# Hi\n\n# one\n# two'
    store.put(tiddler)
    match_tiddler('TestMe2', '<ul class="tags">', neg=True)


def match_tiddler(title, match_string, neg=False):
    response, content = http.request('http://thing.0.0.0.0:8080/%s' % encode_name(title), method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    if neg:
        @py_assert1 = match_string not in content
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py2)s', ), (match_string, content)) % {'py0': @pytest_ar._saferepr(match_string) if 'match_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match_string) else 'match_string', 'py2': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
    else:
        @py_assert1 = match_string in content
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (match_string, content)) % {'py0': @pytest_ar._saferepr(match_string) if 'match_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match_string) else 'match_string', 'py2': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
    return


def match_tiddlers(match_string, neg=False):
    response, content = http.request('http://thing.0.0.0.0:8080/tiddlers', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    if neg:
        @py_assert1 = match_string not in content
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py2)s', ), (match_string, content)) % {'py0': @pytest_ar._saferepr(match_string) if 'match_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match_string) else 'match_string', 'py2': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
    else:
        @py_assert1 = match_string in content
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (match_string, content)) % {'py0': @pytest_ar._saferepr(match_string) if 'match_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match_string) else 'match_string', 'py2': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
    return