# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fnd/Dev/TiddlyWeb/bfw/test/test_plugin_integration.py
# Compiled at: 2014-01-18 04:51:01
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.manage import handle
from . import make_instance, req, StreamCapture

def setup_module(module):
    instance = make_instance()
    module.STORE = instance['store']


def test_gitstore():
    gitdir = os.path.join(STORE.storage._root, '.git')
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isdir
    @py_assert6 = @py_assert3(gitdir)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isdir\n}(%(py5)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(gitdir) if 'gitdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gitdir) else 'gitdir', 'py7': @pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    return


def test_tagdex():
    bag = Bag('snippets')
    STORE.put(bag)
    tiddler = Tiddler('index', 'snippets')
    tiddler.text = 'lipsum'
    tiddler.tags = ['foo', 'bar']
    STORE.put(tiddler)
    response, content = req('GET', '/tags/foo')
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    response, content = req('GET', '/tags/bar')
    @py_assert1 = response.status
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    with StreamCapture('stdout') as (stream):
        handle(['', 'tags'])
        stream.seek(0)
        tags = stream.read().splitlines()
        @py_assert0 = 'foo'
        @py_assert2 = @py_assert0 in tags
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, tags)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tags) if 'tags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tags) else 'tags'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'bar'
        @py_assert2 = @py_assert0 in tags
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, tags)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tags) if 'tags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tags) else 'tags'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
    return