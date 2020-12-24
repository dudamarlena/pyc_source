# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_jsonp.py
# Compiled at: 2013-11-11 13:24:25
"""
Test the JSONP functionality
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from fixtures import make_test_env, make_fake_space, get_auth
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2
from tiddlyweb.model.user import User
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.config import config
from tiddlywebplugins.utils import get_store
base_url = 'http://0.0.0.0:8080'

def setup_module(module):
    make_test_env(module)
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('foo.0.0.0.0', 8080, app_fn)
    module.http = httplib2.Http()
    user = User('foo')
    user.set_password('foobar')
    store.put(user)
    make_fake_space(store, 'foo')


def test_call_jsonp():
    """
    test that we can get some stuff as JSONP
    """
    tiddler = Tiddler('public')
    tiddler.bag = 'foo_public'
    tiddler.text = 'some text'
    store.put(tiddler)
    user_cookie = get_auth('foo', 'foobar')
    callback = 'callback'
    response, content = http.request('http://foo.0.0.0.0:8080/bags/foo_public/tiddlers/public?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = content.startswith
    @py_assert3 = '%s('
    @py_assert6 = @py_assert3 % callback
    @py_assert7 = @py_assert1(@py_assert6)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}((%(py4)s %% %(py5)s))\n}' % {'py0': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(callback) if 'callback' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(callback) else 'callback'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert7 = None
    @py_assert0 = content[-1:]
    @py_assert3 = ')'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/bags/foo_public/tiddlers/public?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = content.startswith
    @py_assert3 = '%s('
    @py_assert6 = @py_assert3 % callback
    @py_assert7 = @py_assert1(@py_assert6)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}((%(py4)s %% %(py5)s))\n}' % {'py0': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(callback) if 'callback' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(callback) else 'callback'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert7 = None
    @py_assert0 = content[-1:]
    @py_assert3 = ')'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_drop_privs():
    """
    test that privileges are dropped when jsonp is requested
    so that we cannot get private data
    """
    tiddler = Tiddler('private')
    tiddler.bag = 'foo_private'
    tiddler.text = 'some text'
    store.put(tiddler)
    user_cookie = get_auth('foo', 'foobar')
    callback = 'callback'
    response, _ = http.request('http://foo.0.0.0.0:8080/bags/foo_private/tiddlers/private?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://foo.0.0.0.0:8080/recipes/foo_private/tiddlers/private?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://foo.0.0.0.0:8080/bags/foo_private?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://foo.0.0.0.0:8080/recipes/foo_private?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://foo.0.0.0.0:8080/bags/foo_private/tiddlers?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://foo.0.0.0.0:8080/recipes/foo_private/tiddlers?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://foo.0.0.0.0:8080/bags/foo_private/tiddlers/private', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_no_subdomain():
    """
    As it's JSONP, we need to protect the tiddlyspace.com domain as well
    (and not just the subdomains).

    This includes bags, recipes and search.
    """
    tiddler = Tiddler('private')
    tiddler.bag = 'foo_private'
    tiddler.text = 'some text'
    store.put(tiddler)
    user_cookie = get_auth('foo', 'foobar')
    callback = 'callback'
    response, _ = http.request('http://0.0.0.0:8080/bags/foo_private/tiddlers/private?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://0.0.0.0:8080/recipes/foo_private/tiddlers/private?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://0.0.0.0:8080/bags/foo_private?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://0.0.0.0:8080/recipes/foo_private?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://0.0.0.0:8080/bags/foo_private/tiddlers?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://0.0.0.0:8080/recipes/foo_private/tiddlers?callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, _ = http.request('http://0.0.0.0:8080/bags/foo_private/tiddlers/private', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/search?q=bag:foo_private&callback=%s' % callback, method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % user_cookie, 
       'Accept': 'application/json'})
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert2 = 'callback([])'
    @py_assert1 = content == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return