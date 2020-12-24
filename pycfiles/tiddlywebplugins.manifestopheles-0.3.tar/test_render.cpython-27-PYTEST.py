# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/manifestopheles/test/test_render.py
# Compiled at: 2013-01-21 13:39:24
"""
Our default renderer takes content that is
expected to be plain text and for titles in
a given bag, links to those titles.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, shutil
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.config import config
from tiddlywebplugins.manifestopheles.contextify import render
from tiddlywebplugins.utils import get_store

def setup_module(module):
    try:
        shutil.rmtree('store')
    except:
        pass

    store = get_store(config)
    bag = Bag('devil-dictionary')
    store.put(bag)
    bag = Bag('x-manifesto')
    store.put(bag)
    recipe = Recipe('devil')
    recipe.set_recipe([
     ('devil-dictionary', ''),
     ('x-manifesto', '')])
    store.put(recipe)
    tiddler = Tiddler('fancy', 'devil-dictionary')
    store.put(tiddler)
    tiddler = Tiddler('house car', 'devil-dictionary')
    store.put(tiddler)
    tiddler = Tiddler('car', 'devil-dictionary')
    store.put(tiddler)
    tiddler = Tiddler('The Truth', 'x-manifesto')
    tiddler.text = '\nI was walking and spied something fancy.\n\nTruth is, I thought it was a house car,\nbut it turns out I was wrong.\n\nIt was a\n      house\n         car!\n\nWhich is way more fancy.\n'
    store.put(tiddler)


def test_simple():
    store = get_store(config)
    environ = {'tiddlyweb.usersign': {'name': 'devil', 'roles': []}, 'tiddlyweb.store': store, 
       'tiddlyweb.manifesto': 'devil', 
       'tiddlyweb.dictionary': 'devil-dictionary'}
    tiddler = store.get(Tiddler('The Truth', 'x-manifesto'))
    output = render(tiddler, environ)
    @py_assert0 = 'something <a title="fancy" href="/manifestos/devil/fancy">fancy</a>.'
    @py_assert2 = @py_assert0 in output
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, output)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() is not @py_builtins.globals() else 'output'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'a <a title="house car" href="/manifestos/devil/house%20car">house car</a>,'
    @py_assert2 = @py_assert0 in output
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, output)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() is not @py_builtins.globals() else 'output'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return