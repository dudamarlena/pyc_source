# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.policyfilter/test/test_filter.py
# Compiled at: 2014-02-08 16:07:39
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlyweb.filters import FilterError, recursive_filter, parse_for_filters
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.store import Store
from tiddlywebplugins.policyfilter import init
from tiddlyweb.config import config
import pytest

def setup_module(module):
    init(config)
    environ = {'tiddlyweb.config': config, 
       'tiddlyweb.usersign': {'name': 'cdent', 'roles': ['COW', 'MOO']}}
    module.store = Store(config['server_store'][0], config['server_store'][1], environ)
    environ['tiddlyweb.store'] = module.store
    module.environ = environ


def test_filtering_bags():
    bag1 = Bag('bag1')
    bag1.policy.create = ['cdent']
    bag2 = Bag('bag2')
    bag2.policy.create = ['R:COW']
    bag3 = Bag('bag3')
    bag3.policy.create = []
    bag4 = Bag('bag4')
    bag4.policy.create = ['NONE']
    bags = [
     bag1, bag2, bag3, bag4]
    for bag in bags:
        store.put(bag)

    found_bags = list(filter('select=policy:create', bags))
    @py_assert2 = len(found_bags)
    @py_assert5 = 3
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(found_bags) if 'found_bags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(found_bags) else 'found_bags', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    names = [ bag.name for bag in found_bags ]
    @py_assert0 = 'bag1'
    @py_assert2 = @py_assert0 in names
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, names)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(names) if 'names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(names) else 'names'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'bag2'
    @py_assert2 = @py_assert0 in names
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, names)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(names) if 'names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(names) else 'names'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'bag3'
    @py_assert2 = @py_assert0 in names
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, names)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(names) if 'names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(names) else 'names'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'bag4'
    @py_assert2 = @py_assert0 not in names
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, names)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(names) if 'names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(names) else 'names'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_filter_recipes():
    recipe1 = Recipe('recipe1')
    recipe1.policy.create = ['cdent']
    recipe2 = Recipe('recipe2')
    recipe2.policy.create = ['R:COW']
    recipe3 = Recipe('recipe3')
    recipe3.policy.create = []
    recipe4 = Recipe('recipe4')
    recipe4.policy.create = ['NONE']
    recipes = [
     recipe1, recipe2, recipe3, recipe4]
    for recipe in recipes:
        store.put(recipe)

    found_recipes = list(filter('select=policy:create', recipes))
    @py_assert2 = len(found_recipes)
    @py_assert5 = 3
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(found_recipes) if 'found_recipes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(found_recipes) else 'found_recipes', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    names = [ recipe.name for recipe in found_recipes ]
    @py_assert0 = 'recipe1'
    @py_assert2 = @py_assert0 in names
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, names)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(names) if 'names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(names) else 'names'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'recipe2'
    @py_assert2 = @py_assert0 in names
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, names)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(names) if 'names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(names) else 'names'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'recipe3'
    @py_assert2 = @py_assert0 in names
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, names)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(names) if 'names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(names) else 'names'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'recipe4'
    @py_assert2 = @py_assert0 not in names
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, names)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(names) if 'names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(names) else 'names'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_filter_tiddlers():
    """
    This should error.
    """
    tiddler1 = Tiddler('tiddler1', 'bag1')
    tiddler1.text = 'foo'
    store.put(tiddler1)
    with pytest.raises(AttributeError):
        found_tiddlers = list(filter('select=policy:create', [tiddler1]))


def filter(filter_string, entities):
    return recursive_filter(parse_for_filters(filter_string, environ)[0], entities)