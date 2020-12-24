# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.methodhack/test/test_post_form.py
# Compiled at: 2013-01-29 10:58:09
"""
mahemoff identified a problem with methodhack
when dealing with form encoded input coming in
on a POST attempting to a be a PUT. The system
tries to read wsgi.input twice and hangs.

By moving methodhack before Query, this should
fix it. But we'll see.

This test isn't really a test, it is a bug replication.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys
sys.path.insert(0, '')
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2
from tiddlyweb.config import config
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.store import Store

def setup_module(module):
    config['system_plugins'] = [
     'tiddlywebplugins.methodhack']
    from tiddlyweb.web import serve

    def app_fn():
        return serve.load_app()

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('our_test_domain', 8001, app_fn)
    module.store = Store(config['server_store'][0], config['server_store'][1], {'tiddlyweb.config': config})


def test_post_a_form_put():
    store.put(Bag('foo'))
    content = 'name=News&resources=http%3A%2F%2Fbbc.co.uk%0D%0Ahttp%3A%2F%2Fnews.google.com%0D%0Ahttp%3A%2F%2Fmemeorandum.com%0D%0A%0D%0A'
    http = httplib2.Http()
    response, output = http.request('http://our_test_domain:8001/bags/foo/tiddlers/bar?http_method=PUT', method='POST', headers={'Content-Type': 'application/x-www-form-urlencoded'}, body=content)
    @py_assert0 = response['status']
    @py_assert3 = '204'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    tiddler = store.get(Tiddler('bar', 'foo'))
    @py_assert1 = tiddler.text
    @py_assert3 = @py_assert1 == content
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s', ), (@py_assert1, content)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() is not @py_builtins.globals() else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() is not @py_builtins.globals() else 'content'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    return