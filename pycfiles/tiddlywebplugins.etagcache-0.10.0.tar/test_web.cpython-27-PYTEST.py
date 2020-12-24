# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.etagcache/test/test_web.py
# Compiled at: 2013-06-04 06:56:52
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, httplib2
from wsgi_intercept import httplib2_intercept
import wsgi_intercept
from tiddlyweb.web.serve import load_app
from tiddlyweb.config import config
from tiddlyweb.store import Store
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.tiddler import Tiddler
import os, shutil

def setup_module(module):
    try:
        shutil.rmtree('store')
    except OSError:
        pass

    app = load_app()

    def app_fn():
        return app

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('our_test_domain', 8001, app_fn)
    store = Store(config['server_store'][0], config['server_store'][1], environ={'tiddlyweb.config': config})
    bag = Bag('place')
    store.put(bag)
    recipe = Recipe('plaice')
    recipe.set_recipe([('place', '')])
    store.put(recipe)
    tiddler = Tiddler('one', 'place')
    tiddler.text = 'hi'
    store.put(tiddler)
    tiddler = Tiddler('two', 'place')
    tiddler.tags = ['tagged']
    tiddler.text = 'hi'
    store.put(tiddler)
    module.store = store
    module.http = httplib2.Http()


def test_simple_get():
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers/one')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'etag'
    @py_assert2 = @py_assert0 in response
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, response)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    etag = response['etag']
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers/one', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '304'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    tiddler = Tiddler('one', 'place')
    tiddler.text = 'bye'
    store.put(tiddler)
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers/one', headers={'If-None-Match': etag})
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers/one')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'etag'
    @py_assert2 = @py_assert0 in response
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, response)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    etag = response['etag']
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers/one', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '304'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers/one', headers={'If-None-Match': etag, 'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    etag = response['etag']
    tiddler = Tiddler('one', 'place')
    tiddler.text = 'cow'
    store.put(tiddler)
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 != etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert2,), ('%(py1)s != %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    etag = response['etag']
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '304'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 == etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers?select=title:two')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    etag = response['etag']
    tiddler = Tiddler('one', 'place')
    tiddler.text = 'cow'
    store.put(tiddler)
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers?select=title:two', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '304'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 == etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tiddler = Tiddler('two', 'place')
    tiddler.text = 'thief'
    store.put(tiddler)
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers?select=title:two', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 != etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert2,), ('%(py1)s != %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    etag = response['etag']
    response, content = http.request('http://our_test_domain:8001/bags/place/tiddlers?select=title:two', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '304'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 == etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://our_test_domain:8001/search?q=two')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    etag = response['etag']
    tiddler = Tiddler('one', 'place')
    tiddler.text = 'cow'
    store.put(tiddler)
    response, content = http.request('http://our_test_domain:8001/search?q=two', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '304'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 == etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://our_test_domain:8001/search?q=two')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://our_test_domain:8001/search?q=two', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '304'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 == etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://our_test_domain:8001/recipes/plaice/tiddlers/two')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 != etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert2,), ('%(py1)s != %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    etag = response['etag']
    response, content = http.request('http://our_test_domain:8001/recipes/plaice/tiddlers/two', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '304'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://our_test_domain:8001/recipes/plaice/tiddlers')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    etag = response['etag']
    response, content = http.request('http://our_test_domain:8001/recipes/plaice/tiddlers', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '304'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 == etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://our_test_domain:8001/recipes/plaice')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    etag = response['etag']
    response, content = http.request('http://our_test_domain:8001/recipes/plaice', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '304'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 == etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    recipe = Recipe('plaice')
    recipe.desc = 'oh how now'
    store.put(recipe)
    response, content = http.request('http://our_test_domain:8001/recipes/plaice', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 != etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert2,), ('%(py1)s != %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = http.request('http://our_test_domain:8001/recipes')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    etag = response['etag']
    response, content = http.request('http://our_test_domain:8001/recipes', headers={'If-None-Match': etag})
    @py_assert0 = response['status']
    @py_assert3 = '304'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['etag']
    @py_assert2 = @py_assert0 == etag
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, etag)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(etag) if 'etag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(etag) else 'etag'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    recipe = Recipe('plaice')
    recipe.desc = 'oh how now'
    store.put(recipe)
    response, content = http.request('http://our_test_domain:8001/recipes')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    etag = response['etag']
    return


def test_bad_encoding--- This code section failed: ---

 L. 264         0  LOAD_GLOBAL           0  'http'
                3  LOAD_ATTR             1  'request'

 L. 265         6  LOAD_CONST               'http://our_test_domain:8001/search?q=tag:"資訊手記"'
                9  CALL_FUNCTION_1       1  None
               12  UNPACK_SEQUENCE_2     2 
               15  STORE_FAST            0  'response'
               18  STORE_FAST            1  'content'

 L. 266        21  LOAD_FAST             0  'response'
               24  LOAD_CONST               'status'
               27  BINARY_SUBSCR    
               28  LOAD_CONST               '200'
               31  COMPARE_OP            2  ==
               34  POP_JUMP_IF_TRUE     46  'to 46'
               37  LOAD_ASSERT              AssertionError
               40  LOAD_FAST             1  'content'
               43  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_FAST' instruction at offset 40