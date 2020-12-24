# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.etagcache/test/test_stress.py
# Compiled at: 2011-02-18 10:27:46
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, httplib2
from wsgi_intercept import httplib2_intercept
import wsgi_intercept
from tiddlyweb.web.serve import load_app
from tiddlyweb.config import config
from tiddlyweb.store import Store
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
import os, shutil, time

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
    for i in range(1, 10):
        tiddler = Tiddler('tiddler%s' % i, 'place')
        tiddler.text = 'hi%s'
        store.put(tiddler)

    module.http = httplib2.Http()


def test_time():
    make_time(8001)


def make_time(port):
    response, content = http.request('http://our_test_domain:%s/bags/place/tiddlers/tiddler5' % port)
    etag = response['etag']
    start = time.time()
    for i in range(1, 200):
        response, content = http.request('http://our_test_domain:%s/bags/place/tiddlers/tiddler5' % port, headers={'If-None-Match': etag})
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

    finish = time.time()
    print start, finish, finish - start
    response, content = http.request('http://our_test_domain:%s/bags/place/tiddlers' % port)
    etag = response['etag']
    start = time.time()
    for i in range(1, 50):
        response, content = http.request('http://our_test_domain:%s/bags/place/tiddlers' % port, headers={'If-None-Match': etag})
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

    finish = time.time()
    print start, finish, finish - start
    return