# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_put_hash.py
# Compiled at: 2013-08-20 13:22:51
"""
Test so-called "friendly" uris: links to tiddlers
in the current space from the root.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from fixtures import make_test_env
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2, simplejson
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag

def setup_module(module):
    make_test_env(module)
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    module.http = httplib2.Http()


def test_hash():
    bag = Bag('one')
    store.put(bag)
    tiddler = Tiddler('hi', 'one')
    tiddler.text = 'fancy'
    store.put(tiddler)
    tiddler = store.get(tiddler)
    @py_assert0 = '_hash'
    @py_assert4 = tiddler.fields
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.fields\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    response, content = http.request('http://0.0.0.0:8080/bags/one/tiddlers/hi.json', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    info = simplejson.loads(content)
    @py_assert0 = info['fields']['_hash']
    @py_assert3 = tiddler.fields['_hash']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    info['text'] = 'not fancy'
    body = simplejson.dumps(info)
    response, content = http.request('http://0.0.0.0:8080/bags/one/tiddlers/hi', headers={'Content-type': 'application/json'}, body=body, method='PUT')
    @py_assert0 = response['status']
    @py_assert3 = '204'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    tiddler = Tiddler('hi', 'one')
    tiddler = store.get(tiddler)
    @py_assert1 = tiddler.text
    @py_assert4 = info['text']
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = tiddler.fields['_hash']
    @py_assert3 = info['fields']['_hash']
    @py_assert2 = @py_assert0 != @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert2,), ('%(py1)s != %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return