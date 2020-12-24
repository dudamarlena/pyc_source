# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_space_handler.py
# Compiled at: 2013-08-20 13:22:51
"""
Test and flesh a /spaces handler-space.

GET /spaces: list all spaces
GET /spaces/{space_name}: 204 if exist
GET /spaces/{space_name}/members: list all members
PUT /spaces/{space_name}: create a space
PUT /spaces/{space_name}/members/{member_name}: add a member
DELETE /spaces/{space_name}/members/{member_name}: remove a member
POST /spaces/{space_name}: Handle subscription, the data package is
  JSON as {"subscriptions": ["space1", "space2", "space3"]}
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, simplejson, httplib2, wsgi_intercept, py.test
from wsgi_intercept import httplib2_intercept
from httpexceptor import HTTP409
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.user import User
from tiddlywebplugins.tiddlyspace.spaces import _update_policy, _make_policy
from test.fixtures import make_test_env, make_fake_space, get_auth
SYSTEM_SPACES = [
 'system-plugins', 'system-info', 'system-images',
 'system-theme', 'system-applications']
SYSTEM_URLS = ['http://system-plugins.0.0.0.0:8080/',
 'http://system-info.0.0.0.0:8080/', 'http://system-applications.0.0.0.0:8080/',
 'http://system-images.0.0.0.0:8080/', 'http://system-theme.0.0.0.0:8080/']

def setup_module(module):
    make_test_env(module)
    httplib2_intercept.install()
    from tiddlyweb.config import config
    config['blacklisted_spaces'] = ['scrappy']
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('cdent.0.0.0.0', 8080, app_fn)
    wsgi_intercept.add_wsgi_intercept('extra.0.0.0.0', 8080, app_fn)
    make_fake_space(module.store, 'cdent')
    user = User('cdent')
    user.set_password('cow')
    module.store.put(user)
    user = User('fnd')
    user.set_password('bird')
    module.store.put(user)
    user = User('psd')
    user.set_password('cat')
    module.store.put(user)


def test_spaces_list():
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/spaces', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['cache-control']
    @py_assert3 = 'no-cache, no-transform'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    info = simplejson.loads(content)
    uris = [ uri for _, uri in [ item.values() for item in info ] ]
    names = [ name for name, _ in [ item.values() for item in info ] ]
    expected_uris = ['http://0.0.0.0:8080/', 'http://cdent.0.0.0.0:8080/']
    expected_uris.extend(SYSTEM_URLS)
    expected_names = ['cdent', 'frontpage']
    expected_names.extend(SYSTEM_SPACES)
    @py_assert2 = sorted(uris)
    @py_assert7 = sorted(expected_uris)
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}',), (@py_assert2, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(uris) if 'uris' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uris) else 'uris', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py6': @pytest_ar._saferepr(expected_uris) if 'expected_uris' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_uris) else 'expected_uris'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert2 = sorted(names)
    @py_assert7 = sorted(expected_names)
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}',), (@py_assert2, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(names) if 'names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(names) else 'names', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py6': @pytest_ar._saferepr(expected_names) if 'expected_names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_names) else 'expected_names'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    make_fake_space(store, 'fnd')
    response, content = http.request('http://0.0.0.0:8080/spaces', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    info = simplejson.loads(content)
    uris = [ uri for _, uri in [ item.values() for item in info ] ]
    @py_assert0 = 'http://cdent.0.0.0.0:8080/'
    @py_assert2 = @py_assert0 in uris
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in',), (@py_assert2,), ('%(py1)s in %(py3)s',), (@py_assert0, uris)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(uris) if 'uris' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uris) else 'uris'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'http://fnd.0.0.0.0:8080/'
    @py_assert2 = @py_assert0 in uris
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in',), (@py_assert2,), ('%(py1)s in %(py3)s',), (@py_assert0, uris)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(uris) if 'uris' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uris) else 'uris'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_space_exist():
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/spaces/cdent', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '204'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert2 = ''
    @py_assert1 = content == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/spaces/nancy', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '404'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'There is nothing at this address.'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_space_members():
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/spaces/cdent/members', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    cookie = get_auth('cdent', 'cow')
    response, content = http.request('http://0.0.0.0:8080/spaces/cdent/members', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['cache-control']
    @py_assert3 = 'no-cache, no-transform'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    info = simplejson.loads(content)
    @py_assert2 = ['cdent']
    @py_assert1 = info == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (info, @py_assert2)) % {'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    response, content = http.request('http://0.0.0.0:8080/spaces/nancy/members', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='GET')
    response['status'] == '404'
    return


def test_create_space():
    cookie = get_auth('cdent', 'cow')
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/spaces/cdent', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='PUT')
    @py_assert0 = response['status']
    @py_assert3 = '409'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/spaces/extra', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '404'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/spaces/extra', method='PUT')
    @py_assert0 = response['status']
    @py_assert3 = '403'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/spaces/extra', method='PUT', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie})
    @py_assert0 = response['status']
    @py_assert3 = '201'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['location']
    @py_assert3 = 'http://extra.0.0.0.0:8080/'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/spaces/extra/members', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='GET')
    response['status'] == '200'
    info = simplejson.loads(content)
    if not info == ['cdent']:
        raise AssertionError, content
        response, content = http.request('http://extra.0.0.0.0:8080/bags/extra_public/tiddlers/SiteInfo.json')
        @py_assert0 = response['status']
        @py_assert3 = '200'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        info = simplejson.loads(content)
        @py_assert0 = 'Space extra'
        @py_assert3 = info['text']
        @py_assert2 = @py_assert0 in @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        response, content = http.request('http://extra.0.0.0.0:8080/GettingStarted.json')
        @py_assert0 = response['status']
        @py_assert3 = '200'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        info = simplejson.loads(content)
        @py_assert0 = info['bag']
        @py_assert3 = 'extra_public'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        bag = store.get(Bag('extra_public'))
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.owner
        @py_assert6 = 'cdent'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.read
        @py_assert6 = []
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.accept
        @py_assert6 = ['NONE']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.accept\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.manage
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.write
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.create
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.create\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.delete
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.delete\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        bag = store.get(Bag('extra_private'))
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.owner
        @py_assert6 = 'cdent'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.read
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.accept
        @py_assert6 = ['NONE']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.accept\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.manage
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.write
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.create
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.create\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.delete
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.delete\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        bag = store.get(Bag('extra_archive'))
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.owner
        @py_assert6 = 'cdent'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.read
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.accept
        @py_assert6 = ['NONE']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.accept\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.manage
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.write
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.create
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.create\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = bag.policy
        @py_assert3 = @py_assert1.delete
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.delete\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        recipe = store.get(Recipe('extra_public'))
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.owner
        @py_assert6 = 'cdent'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.read
        @py_assert6 = []
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.accept
        @py_assert6 = ['NONE']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.accept\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.manage
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.write
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.create
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.create\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.delete
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.delete\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        recipe_list = recipe.get_recipe()
        @py_assert2 = len(recipe_list)
        @py_assert5 = 7
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(recipe_list) if 'recipe_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe_list) else 'recipe_list', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = recipe_list[0][0]
        @py_assert3 = 'system'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[1][0]
        @py_assert3 = 'tiddlyspace'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[2][0]
        @py_assert3 = 'system-plugins_public'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[3][0]
        @py_assert3 = 'system-info_public'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[4][0]
        @py_assert3 = 'system-images_public'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[5][0]
        @py_assert3 = 'system-theme_public'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[6][0]
        @py_assert3 = 'extra_public'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        recipe = store.get(Recipe('extra_private'))
        recipe_list = recipe.get_recipe()
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.owner
        @py_assert6 = 'cdent'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.read
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.accept
        @py_assert6 = ['NONE']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.accept\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.manage
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.write
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.create
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.create\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = recipe.policy
        @py_assert3 = @py_assert1.delete
        @py_assert6 = ['cdent']
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.delete\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert2 = len(recipe_list)
        @py_assert5 = 8
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(recipe_list) if 'recipe_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe_list) else 'recipe_list', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = recipe_list[0][0]
        @py_assert3 = 'system'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[1][0]
        @py_assert3 = 'tiddlyspace'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[2][0]
        @py_assert3 = 'system-plugins_public'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[3][0]
        @py_assert3 = 'system-info_public'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[4][0]
        @py_assert3 = 'system-images_public'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[5][0]
        @py_assert3 = 'system-theme_public'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[6][0]
        @py_assert3 = 'extra_public'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = recipe_list[7][0]
        @py_assert3 = 'extra_private'
        @py_assert2 = @py_assert0 == @py_assert3
        @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_reserved_space_name():
    cookie = get_auth('cdent', 'cow')
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/spaces/www', method='PUT', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie})
    @py_assert0 = response['status']
    @py_assert3 = '409'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'Invalid space name: www'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_case_in_space():
    cookie = get_auth('cdent', 'cow')
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/spaces/CeXtRa', method='PUT', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie})
    @py_assert0 = response['status']
    @py_assert3 = '409'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_chars_in_space():
    testcases = [
     ('foo', '201'),
     ('bAr', '409'),
     ('f0o', '201'),
     ('fo0', '201'),
     ('0foo', '201'),
     ('foo-bar', '201'),
     ('foo-bar-baz', '201'),
     ('-foo', '409'),
     ('foo-', '409')]
    cookie = get_auth('cdent', 'cow')
    http = httplib2.Http()
    for name, status in testcases:
        response, content = http.request('http://0.0.0.0:8080/spaces/%s' % name, method='PUT', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie})
        @py_assert0 = response['status']
        @py_assert2 = @py_assert0 == status
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, status)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(status) if 'status' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(status) else 'status'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    return


def test_add_a_member():
    cookie = get_auth('cdent', 'cow')
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/spaces/extra/members/fnd', method='PUT')
    if not response['status'] == '403':
        raise AssertionError, content
        response, content = http.request('http://extra.0.0.0.0:8080/spaces/extra/members/fnd', method='PUT')
        if not response['status'] == '403':
            raise AssertionError, content
            response, content = http.request('http://0.0.0.0:8080/spaces/extra/members/fnd', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='PUT')
            @py_assert0 = response['status']
            @py_assert3 = '403'
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            response, content = http.request('http://extra.0.0.0.0:8080/spaces/extra/members/fnd', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='PUT')
            @py_assert0 = response['status']
            @py_assert3 = '204'
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            response, content = http.request('http://0.0.0.0:8080/spaces/extra/members', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='GET')
            if not response['status'] == '200':
                raise AssertionError, content
                info = simplejson.loads(content)
                @py_assert2 = ['cdent', 'fnd']
                @py_assert1 = info == @py_assert2
                if not @py_assert1:
                    @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (info, @py_assert2)) % {'py0': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info', 'py3': @pytest_ar._saferepr(@py_assert2)}
                    @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert1 = @py_assert2 = None
                bag = store.get(Bag('extra_private'))
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.owner
                @py_assert6 = 'cdent'
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.read
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.accept
                @py_assert6 = ['NONE']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.accept\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.manage
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.write
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.create
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.create\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.delete
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.delete\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                bag = store.get(Bag('extra_archive'))
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.owner
                @py_assert6 = 'cdent'
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.read
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.accept
                @py_assert6 = ['NONE']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.accept\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.manage
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.write
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.create
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.create\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.delete
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.delete\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                bag = store.get(Bag('extra_public'))
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.owner
                @py_assert6 = 'cdent'
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.read
                @py_assert6 = []
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.accept
                @py_assert6 = ['NONE']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.accept\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.manage
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.write
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.create
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.create\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                @py_assert1 = bag.policy
                @py_assert3 = @py_assert1.delete
                @py_assert6 = ['cdent', 'fnd']
                @py_assert5 = @py_assert3 == @py_assert6
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.delete\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                cookie = get_auth('psd', 'cat')
                response, content = http.request('http://0.0.0.0:8080/spaces/extra/members/psd', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='PUT')
                @py_assert0 = response['status']
                @py_assert3 = '403'
                @py_assert2 = @py_assert0 == @py_assert3
                @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            cookie = get_auth('fnd', 'bird')
            response, content = http.request('http://extra.0.0.0.0:8080/spaces/extra/members/psd', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='PUT')
            @py_assert0 = response['status']
            @py_assert3 = '204'
            @py_assert2 = @py_assert0 == @py_assert3
            @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        cookie = get_auth('fnd', 'bird')
        response, content = http.request('http://extra.0.0.0.0:8080/spaces/extra/members/mary', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='PUT')
        @py_assert0 = response['status']
        @py_assert3 = '409'
        @py_assert2 = @py_assert0 == @py_assert3
        @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_update_policy_nonstandard():
    policy = _make_policy('jon')
    setattr(policy, 'write', ['ANY'])
    setattr(policy, 'read', ['fnd'])
    py.test.raises(HTTP409, '_update_policy(policy, add="jon")')
    setattr(policy, 'write', [])
    setattr(policy, 'create', ['NONE'])
    py.test.raises(HTTP409, '_update_policy(policy, add="jon")')


def test_delete_member():
    cookie = get_auth('fnd', 'bird')
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/spaces/extra/members/psd', method='DELETE')
    @py_assert0 = response['status']
    @py_assert3 = '403'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://extra.0.0.0.0:8080/spaces/extra/members/psd', method='DELETE')
    @py_assert0 = response['status']
    @py_assert3 = '403'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/spaces/extra/members/psd', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='DELETE')
    @py_assert0 = response['status']
    @py_assert3 = '403'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://extra.0.0.0.0:8080/spaces/extra/members/psd', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='DELETE')
    @py_assert0 = response['status']
    @py_assert3 = '204'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://extra.0.0.0.0:8080/spaces/extra/members/fnd', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie}, method='DELETE')
    @py_assert0 = response['status']
    @py_assert3 = '204'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    bag = store.get(Bag('extra_private'))
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.owner
    @py_assert6 = 'cdent'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.read
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.accept
    @py_assert6 = ['NONE']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.accept\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.manage
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.write
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.create
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.create\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.delete
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.delete\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    bag = store.get(Bag('extra_archive'))
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.owner
    @py_assert6 = 'cdent'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.read
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.accept
    @py_assert6 = ['NONE']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.accept\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.manage
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.write
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.create
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.create\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.delete
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.delete\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_subscription():
    cookie = get_auth('cdent', 'cow')
    http = httplib2.Http()
    subscriptions = simplejson.dumps({'subscriptions': ['extra']})
    response, content = http.request('http://0.0.0.0:8080/spaces/cdent', method='POST', headers={'Content-Type': 'application/json'}, body=subscriptions)
    @py_assert0 = response['status']
    @py_assert3 = '403'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/spaces/cdent', method='POST', headers={'Content-Type': 'application/json', 
       'Cookie': 'tiddlyweb_user="%s"' % cookie}, body='')
    @py_assert0 = response['status']
    @py_assert3 = '409'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/spaces/cdent', method='POST', headers={'Content-Type': 'application/json', 
       'Cookie': 'tiddlyweb_user="%s"' % cookie}, body=subscriptions)
    @py_assert0 = response['status']
    @py_assert3 = '204'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_blacklisted_subscription():
    cookie = get_auth('cdent', 'cow')
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/spaces/scrappy', method='PUT', headers={'Cookie': 'tiddlyweb_user="%s"' % cookie})
    @py_assert0 = response['status']
    @py_assert3 = '201'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    subscriptions = simplejson.dumps({'subscriptions': ['scrappy']})
    response, content = http.request('http://0.0.0.0:8080/spaces/cdent', method='POST', headers={'Content-Type': 'application/json', 
       'Cookie': 'tiddlyweb_user="%s"' % cookie}, body=subscriptions)
    @py_assert0 = response['status']
    @py_assert3 = '409'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'Subscription not allowed to space: scrappy'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_list_my_spaces():
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/spaces?mine=1', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '200'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    info = simplejson.loads(content)
    @py_assert0 = 'fnd'
    @py_assert2 = @py_assert0 not in info
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, info)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(info) if 'info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(info) else 'info'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return