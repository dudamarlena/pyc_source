# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fnd/Dev/TiddlyWeb/bfw/test/test_web.py
# Compiled at: 2014-01-18 04:40:48
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from urllib import urlencode
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.policy import Policy
from tiddlyweb.store import NoTiddlerError, NoBagError
from tiddlyweb.config import config as CONFIG
from tiddlyweb.web.util import make_cookie
from . import make_instance, req

def setup_module(module):
    instance = make_instance()
    module.STORE = instance['store']
    module.ADMIN_COOKIE = instance['admin_cookie']
    bag = Bag('alpha')
    bag.policy = Policy(read=['admin'], write=['admin'], create=['admin'], delete=[
     'admin'], manage=['admin'])
    STORE.put(bag)
    bag = Bag('bravo')
    STORE.put(bag)
    bag = Bag('charlie')
    bag.policy = Policy(read=['nobody'], write=['nobody'], create=['nobody'], delete=[
     'nobody'], manage=['nobody'])
    STORE.put(bag)
    tiddler = Tiddler('index', 'bravo')
    tiddler.text = 'lorem ipsum\ndolor *sit* amet'
    tiddler.type = 'text/x-markdown'
    STORE.put(tiddler)


def test_front_page():
    response, content = req('GET', '/')
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['content-type']
    @py_assert3 = 'text/html; charset=UTF-8'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'Log in'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'Register'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    uri = 'https://github.com/FND/tiddlywebplugins.bfw'
    @py_assert0 = '<a href="%s">BFW</a>'
    @py_assert3 = @py_assert0 % uri
    @py_assert4 = @py_assert3 in content
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('(%(py1)s %% %(py2)s) in %(py5)s', ), (@py_assert3, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py2': @pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri', 'py5': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert3 = @py_assert4 = None
    frontpage = Tiddler('index', 'meta')
    STORE.delete(frontpage)
    response, content = req('GET', '/')
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<a href="%s">BFW</a>'
    @py_assert3 = @py_assert0 % uri
    @py_assert4 = @py_assert3 not in content
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert4,), ('(%(py1)s %% %(py2)s) not in %(py5)s', ), (@py_assert3, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py2': @pytest_ar._saferepr(uri) if 'uri' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uri) else 'uri', 'py5': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert3 = @py_assert4 = None
    return


def test_dashboard():
    response, content = req('GET', '/~')
    @py_assert1 = response.status
    @py_assert4 = 401
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    response, content = req('GET', '/~', headers={'Cookie': ADMIN_COOKIE})
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<a href="/meta/index">meta</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<a href="/admin/index">admin</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<a href="/alpha/index">alpha</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<a href="/bravo/index">bravo</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'charlie'
    @py_assert2 = @py_assert0 in content
    @py_assert6 = not @py_assert2
    if not @py_assert6:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format7 = 'assert not %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert6 = None
    @py_assert0 = '<option value="meta">'
    @py_assert2 = @py_assert0 not in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<option value="admin">'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<option value="alpha">'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<option value="bravo">'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = req('GET', '/~', headers={'Cookie': ADMIN_COOKIE})
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = "admin's personal wiki"
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    index = Tiddler('index', 'admin')
    STORE.delete(index)
    response, content = req('GET', '/~', headers={'Cookie': ADMIN_COOKIE})
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_wiki_page():
    response, content = req('GET', '/alpha/index')
    @py_assert1 = response.status
    @py_assert4 = 302
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '/challenge?tiddlyweb_redirect=%2Falpha%2Findex'
    @py_assert3 = response['location']
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['location']
    @py_assert2 = @py_assert0.endswith
    @py_assert4 = '/challenge?tiddlyweb_redirect=%s'
    @py_assert6 = '%2Falpha%2Findex'
    @py_assert8 = @py_assert4 % @py_assert6
    @py_assert9 = @py_assert2(@py_assert8)
    if not @py_assert9:
        @py_format11 = 'assert %(py10)s\n{%(py10)s = %(py3)s\n{%(py3)s = %(py1)s.endswith\n}((%(py5)s %% %(py7)s))\n}' % {'py1': @pytest_ar._saferepr(@py_assert0), 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    response, content = req('GET', '/bravo/index')
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<p>lorem ipsum\ndolor <em>sit</em> amet</p>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<a href="/editor?page=bravo%2Findex">edit</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = req('GET', '/bravo/HelloWorld')
    @py_assert1 = response.status
    @py_assert4 = 302
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['location']
    @py_assert3 = '/editor?page=bravo%2FHelloWorld'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_page_editor():
    response, content = req('GET', '/editor?page=alpha%2FHelloWorld')
    @py_assert1 = response.status
    @py_assert4 = 302
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['location']
    @py_assert2 = @py_assert0.endswith
    @py_assert4 = '/challenge?tiddlyweb_redirect=%s'
    @py_assert6 = '%2Feditor%3Fpage%3Dalpha%252FHelloWorld'
    @py_assert8 = @py_assert4 % @py_assert6
    @py_assert9 = @py_assert2(@py_assert8)
    if not @py_assert9:
        @py_format11 = 'assert %(py10)s\n{%(py10)s = %(py3)s\n{%(py3)s = %(py1)s.endswith\n}((%(py5)s %% %(py7)s))\n}' % {'py1': @pytest_ar._saferepr(@py_assert0), 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    response, content = req('GET', '/editor?page=bravo%2FHelloWorld')
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<form '
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'action="/pages"'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'method="post"'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<title>bravo/HelloWorld</title>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<h1>HelloWorld</h1>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<input type="hidden" name="wiki" value="bravo">'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<input type="hidden" name="title" value="HelloWorld">'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<textarea name="text" data-widearea="enable"></textarea>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '"HelloWorld" does not exist yet in wiki "bravo"'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = req('GET', '/editor?page=bravo%2Findex')
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<textarea name="text" data-widearea="enable">lorem ipsum\ndolor *sit* amet</textarea>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'does not exist yet'
    @py_assert2 = @py_assert0 in content
    @py_assert6 = not @py_assert2
    if not @py_assert6:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format7 = 'assert not %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert6 = None
    return


def test_user_registration():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'username': 'fnd', 
       'password': 'foo', 
       'password_confirmation': 'foo'}
    @py_assert1 = 'fnd'
    @py_assert3 = _bag_exists(@py_assert1)
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0': @pytest_ar._saferepr(_bag_exists) if '_bag_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_bag_exists) else '_bag_exists', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    response, content = req('POST', '/register', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 303
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = 'tiddlyweb_user="fnd:'
    @py_assert3 = response['set-cookie']
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    bag = _bag_exists('fnd')
    if not bag:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.read
    @py_assert6 = ['fnd']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    bag = Bag('sandbox')
    STORE.put(bag)
    _data = {}
    _data.update(data)
    _data['username'] = 'sandbox'
    response, content = req('POST', '/register', urlencode(_data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 409
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    response, content = req('POST', '/register', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 409
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    data['username'] = 'wikis'
    response, content = req('POST', '/register', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 409
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    data = {'username': 'dummy', 
       'password': 'foo', 
       'password_confirmation': 'foo'}
    response, content = req('POST', '/register', urlencode(data), headers={'Content-Type': 'application/x-www-form-urlencoded'})
    cookie = make_cookie('tiddlyweb_user', 'dummy', mac_key=CONFIG['secret'])
    response, content = req('GET', '/~', headers={'Cookie': cookie})
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = "dummy's personal wiki"
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_login():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'user': 'fnd', 
       'password': 'foo'}
    response, content = req('POST', '/challenge/cookie_form', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 303
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = 'tiddlyweb_user="fnd:'
    @py_assert3 = response['set-cookie']
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = req('POST', '/logout')
    @py_assert1 = response.status
    @py_assert4 = 303
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['set-cookie']
    @py_assert3 = 'tiddlyweb_user=; Max-Age=0; Path=/'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = response['location']
    @py_assert3 = 'http://example.org:8001/'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_wiki_creation():
    @py_assert1 = 'foo'
    @py_assert3 = _bag_exists(@py_assert1)
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0': @pytest_ar._saferepr(_bag_exists) if '_bag_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_bag_exists) else '_bag_exists', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    default_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'wiki': 'foo', 
       'private': '1'}
    response, content = req('POST', '/wikis')
    @py_assert1 = response.status
    @py_assert4 = 415
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    response, content = req('POST', '/wikis', urlencode(data), headers=default_headers)
    @py_assert1 = response.status
    @py_assert4 = 401
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = 'foo'
    @py_assert3 = _bag_exists(@py_assert1)
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0': @pytest_ar._saferepr(_bag_exists) if '_bag_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_bag_exists) else '_bag_exists', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    headers = {'Cookie': ADMIN_COOKIE}
    headers.update(default_headers)
    response, content = req('POST', '/wikis', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 303
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['location']
    @py_assert3 = '/foo/index'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = 'foo'
    @py_assert3 = _bag_exists(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0': @pytest_ar._saferepr(_bag_exists) if '_bag_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_bag_exists) else '_bag_exists', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    response, content = req('GET', '/foo', headers={'Cookie': ADMIN_COOKIE})
    @py_assert1 = response.status
    @py_assert4 = 302
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['location']
    @py_assert3 = '/foo/index'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = req('GET', '/bar')
    @py_assert1 = response.status
    @py_assert4 = 404
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    response, content = req('GET', '/foo')
    @py_assert1 = response.status
    @py_assert4 = 302
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['location']
    @py_assert2 = @py_assert0.endswith
    @py_assert4 = '/challenge?tiddlyweb_redirect=%2Ffoo'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.endswith\n}(%(py5)s)\n}' % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    headers = {'Cookie': ADMIN_COOKIE}
    headers.update(default_headers)
    response, content = req('POST', '/wikis', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 409
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    data['wiki'] = 'wikis'
    response, content = req('POST', '/wikis', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 409
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = 'bar'
    @py_assert3 = _bag_exists(@py_assert1)
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0': @pytest_ar._saferepr(_bag_exists) if '_bag_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_bag_exists) else '_bag_exists', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    data = {'wiki': 'bar'}
    headers = {'Cookie': ADMIN_COOKIE}
    headers.update(default_headers)
    response, content = req('POST', '/wikis', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 303
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['location']
    @py_assert3 = '/bar/index'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = 'bar'
    @py_assert3 = _bag_exists(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0': @pytest_ar._saferepr(_bag_exists) if '_bag_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_bag_exists) else '_bag_exists', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    response, content = req('GET', '/bar')
    @py_assert1 = response.status
    @py_assert4 = 302
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['location']
    @py_assert3 = '/bar/index'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_page_creation_and_modification():
    default_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'wiki': 'foo', 
       'title': 'Lipsum', 
       'tags': 'foo, bar, baz', 
       'text': 'lorem ipsum'}
    response, content = req('POST', '/pages')
    @py_assert1 = response.status
    @py_assert4 = 415
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    response, content = req('POST', '/pages', urlencode(data), headers=default_headers)
    @py_assert1 = response.status
    @py_assert4 = 403
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = 'Lipsum'
    @py_assert3 = 'foo'
    @py_assert5 = _tiddler_exists(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}' % {'py0': @pytest_ar._saferepr(_tiddler_exists) if '_tiddler_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_tiddler_exists) else '_tiddler_exists', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    headers = {'Cookie': ADMIN_COOKIE}
    headers.update(default_headers)
    response, content = req('POST', '/pages', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 303
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['location']
    @py_assert3 = '/foo/Lipsum'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = 'Lipsum'
    @py_assert3 = 'foo'
    @py_assert5 = _tiddler_exists(@py_assert1, @py_assert3)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}' % {'py0': @pytest_ar._saferepr(_tiddler_exists) if '_tiddler_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_tiddler_exists) else '_tiddler_exists', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    response, content = req('GET', '/foo/Lipsum', headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['content-type']
    @py_assert3 = 'text/html; charset=UTF-8'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '<p>lorem ipsum</p>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '>foo</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '>bar</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '>baz</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    data['text'] = 'lorem ipsum\ndolor *sit* amet'
    data['tags'] = 'hello,world'
    response, content = req('POST', '/pages', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 303
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = response['location']
    @py_assert3 = '/foo/Lipsum'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    response, content = req('GET', '/foo/Lipsum', headers=headers)
    @py_assert0 = '<p>lorem ipsum\ndolor <em>sit</em> amet</p>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '>hello</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '>world</a>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_errors():
    response, content = req('GET', '/N/A')
    @py_assert1 = response.status
    @py_assert4 = 404
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<html>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'not found'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = req('POST', '/')
    @py_assert1 = response.status
    @py_assert4 = 405
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<html>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'not allowed'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = req('GET', '/~')
    @py_assert1 = response.status
    @py_assert4 = 401
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<html>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'unauthorized'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    response, content = req('POST', '/register')
    @py_assert1 = response.status
    @py_assert4 = 415
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<html>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'unsupported'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    data = {'username': 'foo', 
       'password': 'bar', 
       'password_confirmation': 'baz'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response, content = req('POST', '/register', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 400
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<html>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'passwords do not match'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    data = {'username': 'admin', 
       'password': 'foo', 
       'password_confirmation': 'foo'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response, content = req('POST', '/register', urlencode(data), headers=headers)
    @py_assert1 = response.status
    @py_assert4 = 409
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<html>'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'username unavailable'
    @py_assert2 = @py_assert0 in content
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, content)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_static_assets():
    response, content = req('GET', '/static')
    @py_assert1 = response.status
    @py_assert4 = 404
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    response, content = req('GET', '/static/../tiddlywebconfig.py')
    @py_assert1 = response.status
    @py_assert4 = 404
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    response, content = req('GET', '/static/pure.css')
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    response, content = req('GET', '/static/favicon.ico')
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def _tiddler_exists(title, bag_name):
    tiddler = Tiddler(title, bag_name)
    try:
        tiddler = STORE.get(tiddler)
        return True
    except NoTiddlerError:
        return False


def _bag_exists(bag_name):
    bag = Bag(bag_name)
    try:
        STORE.get(bag)
        return bag
    except NoBagError:
        return False