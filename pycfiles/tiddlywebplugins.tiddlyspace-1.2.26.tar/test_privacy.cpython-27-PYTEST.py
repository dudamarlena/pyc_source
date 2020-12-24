# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_privacy.py
# Compiled at: 2013-08-20 13:22:51
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from test.fixtures import make_test_env, make_fake_space, get_auth
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2, simplejson
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.user import User
from tiddlywebplugins.tiddlyspace.spaces import change_space_member

def setup_module(module):
    make_test_env(module)
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('thing.0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('foo.0.0.0.0', 8080, app_fn)
    user = User('thingone')
    user.set_password('how')
    store.put(user)
    user = User('thingtwo')
    user.set_password('how')
    store.put(user)
    module.http = httplib2.Http()


def test_create_spaces():
    cookie = get_auth('thingone', 'how')
    response, content = http.request('http://0.0.0.0:8080/spaces/thing', method='PUT', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie})
    @py_assert0 = response['status']
    @py_assert3 = '201'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://thing.0.0.0.0:8080/bags/thing_private/tiddlers/thingone', method='PUT', headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"' % cookie}, body='{"text": "thingone"}')
    @py_assert0 = response['status']
    @py_assert3 = '204'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    cookie = get_auth('thingtwo', 'how')
    response, content = http.request('http://0.0.0.0:8080/spaces/foo', method='PUT', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie})
    @py_assert0 = response['status']
    @py_assert3 = '201'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://foo.0.0.0.0:8080/bags/foo_private/tiddlers/thingtwo', method='PUT', headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"' % cookie}, body='{"text": "thingtwo"}')
    @py_assert0 = response['status']
    @py_assert3 = '204'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_foo_tiddlers_guest():
    cookie = get_auth('thingone', 'how')
    response, content = http.request('http://foo.0.0.0.0:8080/', method='GET', headers={'Accept': 'application/json'})
    guest_content = content
    response, content = http.request('http://foo.0.0.0.0:8080/', headers={'Accept': 'application/json', 'Cookie': 'tiddlyweb_user="%s"' % cookie})
    user_content = content
    @py_assert1 = guest_content == user_content
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (guest_content, user_content)) % {'py0': @pytest_ar._saferepr(guest_content) if 'guest_content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(guest_content) else 'guest_content', 'py2': @pytest_ar._saferepr(user_content) if 'user_content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(user_content) else 'user_content'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    response, content = http.request('http://thing.0.0.0.0:8080/bags/thing_private/tiddlers', method='GET', headers={'Accept': 'application/json', 'Cookie': 'tiddlyweb_user="%s"' % cookie})
    thing_content = content
    response, content = http.request('http://foo.0.0.0.0:8080/bags/thing_private/tiddlers', method='GET', headers={'Accept': 'application/json', 'Cookie': 'tiddlyweb_user="%s"' % cookie})
    @py_assert0 = response['status']
    @py_assert3 = '404'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://foo.0.0.0.0:8080/bags/thing_private/tiddlers', method='GET', headers={'Accept': 'application/json', 'X-ControlView': 'false', 
       'Cookie': 'tiddlyweb_user="%s"' % cookie})
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://foo.0.0.0.0:8080/bags/thing_private/tiddlers/more', method='PUT', headers={'Content-Type': 'application/json', 'X-ControlView': 'false', 
       'Cookie': 'tiddlyweb_user="%s"' % cookie}, body='{"text": "hi"}')
    @py_assert0 = response['status']
    @py_assert3 = '403'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return