# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_mapuser_validate.py
# Compiled at: 2013-08-20 13:22:51
"""
Test creation of tiddlers in the MAPUSER bag.

The name of the tiddler is the external auth usersign.
The PUT tiddler is empty. A validator sets
fields['mapped_user'] to the current usersign.name.

Note: This does not test the way in which the MAPUSER
information is used by the extractor. Just the proper
creation of the tiddlers.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, wsgi_intercept, httplib2, Cookie, simplejson
from wsgi_intercept import httplib2_intercept
from tiddlyweb.model.user import User
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.web.util import make_cookie
from test.fixtures import make_test_env
AUTH_COOKIE = None

def setup_module(module):
    make_test_env(module)
    from tiddlyweb.config import config
    module.secret = config['secret']
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    user = User('cdent')
    user.set_password('cow')
    module.store.put(user)
    user = User('fnd')
    module.store.put(user)


def test_create_map_requires_user():
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/bags/MAPUSER/tiddlers/x.auth.thing', method='PUT', headers={'Content-Type': 'application/json'}, body='{}')
    @py_assert0 = response['status']
    @py_assert3 = '403'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_create_map_uses_user():
    global AUTH_COOKIE
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/challenge/tiddlywebplugins.tiddlyspace.cookie_form', body='user=cdent&password=cow', method='POST', headers={'Content-Type': 'application/x-www-form-urlencoded'})
    @py_assert0 = response.previous['status']
    @py_assert3 = '303'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    user_cookie = response.previous['set-cookie']
    cookie = Cookie.SimpleCookie()
    cookie.load(user_cookie)
    AUTH_COOKIE = cookie['tiddlyweb_user'].value
    bad_second_cookie = make_cookie('tiddlyweb_secondary_user', 'x.auth.thing', mac_key='slippy')
    mismatch_second_cookie = make_cookie('tiddlyweb_secondary_user', 'y.auth.thing', mac_key=secret)
    second_cookie = make_cookie('tiddlyweb_secondary_user', 'x.auth.thing', mac_key=secret)
    response, content = http.request('http://0.0.0.0:8080/bags/MAPUSER/tiddlers/x.auth.thing', method='PUT', headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"' % AUTH_COOKIE}, body='{"text":"house"}')
    if not response['status'] == '409':
        raise AssertionError, content
        @py_assert0 = 'secondary cookie not present'
        @py_assert2 = @py_assert0 in content
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        response, content = http.request('http://0.0.0.0:8080/bags/MAPUSER/tiddlers/x.auth.thing', method='PUT', headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"; %s' % (
                    AUTH_COOKIE, bad_second_cookie)}, body='{"text":"house"}')
        if not response['status'] == '409':
            raise AssertionError, content
            @py_assert0 = 'secondary cookie invalid'
            @py_assert2 = @py_assert0 in content
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None
            response, content = http.request('http://0.0.0.0:8080/bags/MAPUSER/tiddlers/x.auth.thing', method='PUT', headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"; %s' % (
                        AUTH_COOKIE, mismatch_second_cookie)}, body='{"text":"house"}')
            if not response['status'] == '409':
                raise AssertionError, content
                @py_assert0 = 'secondary cookie mismatch'
                @py_assert2 = @py_assert0 in content
                if not @py_assert2:
                    @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
                    @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert0 = @py_assert2 = None
                response, content = http.request('http://0.0.0.0:8080/bags/MAPUSER/tiddlers/x.auth.thing', method='PUT', headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"; %s' % (
                            AUTH_COOKIE, second_cookie)}, body='{"text":"house"}')
                @py_assert0 = response['status']
                @py_assert3 = '204'
                @py_assert2 = @py_assert0 == @py_assert3
                if not @py_assert2:
                    @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                    @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert0 = @py_assert2 = @py_assert3 = None
                response, content = http.request('http://0.0.0.0:8080/bags/MAPUSER/tiddlers/x.auth.thing', method='GET', headers={'Accept': 'application/json', 'Cookie': 'tiddlyweb_user="%s"; %s' % (
                            AUTH_COOKIE, second_cookie)})
                @py_assert0 = response['status']
                @py_assert3 = '403'
                @py_assert2 = @py_assert0 == @py_assert3
                if not @py_assert2:
                    @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                    @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert0 = @py_assert2 = @py_assert3 = None
                @py_assert0 = 'may not read'
                @py_assert2 = @py_assert0 in content
                if not @py_assert2:
                    @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
                    @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert0 = @py_assert2 = None
                tiddler = Tiddler('x.auth.thing', 'MAPUSER')
                tiddler = store.get(tiddler)
                @py_assert1 = tiddler.modifier
                @py_assert4 = 'cdent'
                @py_assert3 = @py_assert1 == @py_assert4
                if not @py_assert3:
                    @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.modifier\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
                    @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format8))
                @py_assert1 = @py_assert3 = @py_assert4 = None
                @py_assert1 = tiddler.text
                @py_assert4 = ''
                @py_assert3 = @py_assert1 == @py_assert4
                if not @py_assert3:
                    @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
                    @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format8))
                @py_assert1 = @py_assert3 = @py_assert4 = None
                @py_assert0 = 'mapped_user'
                @py_assert4 = tiddler.fields
                @py_assert2 = @py_assert0 in @py_assert4
                if not @py_assert2:
                    @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.fields\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py5': @pytest_ar._saferepr(@py_assert4)}
                    @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format8))
                @py_assert0 = @py_assert2 = @py_assert4 = None
                @py_assert0 = tiddler.fields['mapped_user']
                @py_assert3 = 'cdent'
                @py_assert2 = @py_assert0 == @py_assert3
                @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            response, content = http.request('http://0.0.0.0:8080/bags/MAPUSER/tiddlers/x.auth.thing', method='PUT', headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"; %s' % (
                        AUTH_COOKIE, second_cookie)}, body='{}')
            @py_assert0 = response['status']
            @py_assert3 = '403'
            @py_assert2 = @py_assert0 == @py_assert3
            @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = 'may not write'
        @py_assert2 = @py_assert0 in content
        @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_user_may_not_map_user():
    """Make user X can't map user Y to themselves."""
    second_cookie = make_cookie('tiddlyweb_secondary_user', 'fnd', mac_key=secret)
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/bags/MAPUSER/tiddlers/fnd', method='PUT', headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"; %s' % (
                AUTH_COOKIE, second_cookie)}, body='{}')
    @py_assert0 = response['status']
    @py_assert3 = '409'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'username exists'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_user_may_not_map_self():
    """Make user X can't map user Y to themselves."""
    second_cookie = make_cookie('tiddlyweb_secondary_user', 'cdent', mac_key=secret)
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/bags/MAPUSER/tiddlers/cdent', method='PUT', headers={'Content-Type': 'application/json', 'Cookie': 'tiddlyweb_user="%s"; %s' % (
                AUTH_COOKIE, second_cookie)}, body='{}')
    @py_assert0 = response['status']
    @py_assert3 = '409'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'username exists'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_user_maps_info():
    """User can get their own identities at /users/{username}/identities"""
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/users/cdent/identities', method='GET')
    @py_assert0 = response['status']
    @py_assert3 = '401'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = http.request('http://0.0.0.0:8080/users/cdent/identities', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % AUTH_COOKIE})
    if not response['status'] == '200':
        raise AssertionError, content
        info = simplejson.loads(content)
        if not 'x.auth.thing' in info:
            raise AssertionError, info
            tiddler = Tiddler('fnd.example.org', 'MAPUSER')
            tiddler.fields['mapped_user'] = 'fnd'
            tiddler = store.put(tiddler)
            tiddler = Tiddler('cdent.example.com', 'MAPUSER')
            tiddler.fields['mapped_user'] = 'cdent'
            tiddler = store.put(tiddler)
            response, content = http.request('http://0.0.0.0:8080/users/cdent/identities', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % AUTH_COOKIE})
            identities = simplejson.loads(content)
            if not response['status'] == '200':
                raise AssertionError, content
                @py_assert2 = len(identities)
                @py_assert5 = 2
                @py_assert4 = @py_assert2 == @py_assert5
                if not @py_assert4:
                    @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(identities) if 'identities' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(identities) else 'identities', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
                    @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format9))
                @py_assert2 = @py_assert4 = @py_assert5 = None
                @py_assert0 = 'x.auth.thing'
                @py_assert2 = @py_assert0 in identities
                if not @py_assert2:
                    @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, identities)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(identities) if 'identities' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(identities) else 'identities'}
                    @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert0 = @py_assert2 = None
                @py_assert0 = 'cdent.example.com'
                @py_assert2 = @py_assert0 in identities
                if not @py_assert2:
                    @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, identities)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(identities) if 'identities' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(identities) else 'identities'}
                    @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert0 = @py_assert2 = None
                @py_assert0 = 'fnd.example.org'
                @py_assert2 = @py_assert0 not in identities
                if not @py_assert2:
                    @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, identities)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(identities) if 'identities' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(identities) else 'identities'}
                    @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert0 = @py_assert2 = None
                response, content = http.request('http://0.0.0.0:8080/users/fnd/identities', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % AUTH_COOKIE})
                @py_assert0 = response['status']
                @py_assert3 = '403'
                @py_assert2 = @py_assert0 == @py_assert3
                if not @py_assert2:
                    @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                    @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert0 = @py_assert2 = @py_assert3 = None
                @py_assert0 = 'Bad user for action'
                @py_assert2 = @py_assert0 in content
                @py_format4 = @py_assert2 or @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None
            user = store.get(User('cdent'))
            user.add_role('ADMIN')
            store.put(user)
            response, content = http.request('http://0.0.0.0:8080/users/fnd/identities', method='GET', headers={'Cookie': 'tiddlyweb_user="%s"' % AUTH_COOKIE})
            @py_assert0 = response['status']
            @py_assert3 = '200'
            @py_assert2 = @py_assert0 == @py_assert3
            @py_format5 = @py_assert2 or @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        identities = simplejson.loads(content)
        @py_assert2 = ['fnd.example.org']
        @py_assert1 = identities == @py_assert2
        @py_format4 = @py_assert1 or @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (identities, @py_assert2)) % {'py0': @pytest_ar._saferepr(identities) if 'identities' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(identities) else 'identities', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return