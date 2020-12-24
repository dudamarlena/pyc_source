# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.remotebag/test/test_remotebag.py
# Compiled at: 2013-07-02 11:37:53
"""
Test for remotebag.py.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
REMOTE_BAG = 'http://remotebag-test.tiddlyspace.com/bags/remotebag-test_public/tiddlers'
REMOTE_HTML = 'http://peermore.com/astool.html'
from tiddlyweb.config import config
from tiddlywebplugins.remotebag import init, get_remote_tiddlers, get_remote_tiddler
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.recipe import Recipe
from tiddlyweb import control
from tiddlywebplugins.utils import get_store
import httplib2

def setup_module(module):
    import shutil
    try:
        shutil.rmtree('store')
    except OSError:
        pass

    init(config)
    module.store = get_store(config)
    module.environ = {'tiddlyweb.config': config, 'tiddlyweb.store': store}


def test_get_tiddlers():
    tiddlers = list(get_remote_tiddlers(environ, REMOTE_BAG))
    titles = [ tiddler.title for tiddler in tiddlers ]
    for title in ['alpha', 'beta', 'gamma']:
        @py_assert1 = title in titles
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (title, titles)) % {'py0': @pytest_ar._saferepr(title) if 'title' in @py_builtins.locals() is not @py_builtins.globals() else 'title', 'py2': @pytest_ar._saferepr(titles) if 'titles' in @py_builtins.locals() is not @py_builtins.globals() else 'titles'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.bag
    @py_assert4 = @py_assert2 == REMOTE_BAG
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.bag\n} == %(py5)s', ), (@py_assert2, REMOTE_BAG)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(REMOTE_BAG) if 'REMOTE_BAG' in @py_builtins.locals() is not @py_builtins.globals() else 'REMOTE_BAG'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0._text
    @py_assert4 = @py_assert2 == None
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s._text\n} == %(py5)s', ), (@py_assert2, None)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() is not @py_builtins.globals() else 'None'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    return


def test_get_tiddler():
    remote_tiddler = Tiddler('alpha', REMOTE_BAG)
    tiddler = get_remote_tiddler(environ, remote_tiddler)
    @py_assert1 = tiddler.tags
    @py_assert4 = ['alpha']
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.tags\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() is not @py_builtins.globals() else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.text
    @py_assert4 = 'alpha'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() is not @py_builtins.globals() else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_get_recipe():
    recipe = Recipe('thing')
    recipe.set_recipe([(REMOTE_BAG, '')])
    store.put(recipe)
    tiddlers = control.get_tiddlers_from_recipe(recipe, environ)
    titles = [ tiddler.title for tiddler in tiddlers ]
    for title in ['alpha', 'beta', 'gamma']:
        @py_assert1 = title in titles
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (title, titles)) % {'py0': @pytest_ar._saferepr(title) if 'title' in @py_builtins.locals() is not @py_builtins.globals() else 'title', 'py2': @pytest_ar._saferepr(titles) if 'titles' in @py_builtins.locals() is not @py_builtins.globals() else 'titles'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.bag
    @py_assert4 = @py_assert2 == REMOTE_BAG
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.bag\n} == %(py5)s', ), (@py_assert2, REMOTE_BAG)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(REMOTE_BAG) if 'REMOTE_BAG' in @py_builtins.locals() is not @py_builtins.globals() else 'REMOTE_BAG'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0._text
    @py_assert4 = @py_assert2 == None
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s._text\n} == %(py5)s', ), (@py_assert2, None)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() is not @py_builtins.globals() else 'None'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    return


def test_get_recipe_filters():
    recipe = Recipe('thing')
    recipe.set_recipe([(REMOTE_BAG, 'select=tag:alpha')])
    store.put(recipe)
    tiddlers = control.get_tiddlers_from_recipe(recipe, environ)
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() is not @py_builtins.globals() else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'alpha'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.bag
    @py_assert4 = @py_assert2 == REMOTE_BAG
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.bag\n} == %(py5)s', ), (@py_assert2, REMOTE_BAG)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(REMOTE_BAG) if 'REMOTE_BAG' in @py_builtins.locals() is not @py_builtins.globals() else 'REMOTE_BAG'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.text
    @py_assert5 = 'alpha'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.text\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_get_remote_weird():
    recipe = Recipe('stuff')
    recipe.set_recipe([(REMOTE_HTML, '')])
    store.put(recipe)
    tiddlers = control.get_tiddlers_from_recipe(recipe, environ)
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() is not @py_builtins.globals() else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'The Computer as Tool: From Interaction To Augmentation'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddler = store.get(tiddlers[0])
    @py_assert0 = 'Humans are likely to grant intention to someone or something that performs actions in a way that is difficult to understand.'
    @py_assert4 = tiddler.text
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.text\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() is not @py_builtins.globals() else 'tiddler', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    return