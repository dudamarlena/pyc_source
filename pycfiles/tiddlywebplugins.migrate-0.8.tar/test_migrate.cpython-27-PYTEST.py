# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.migrate/test/test_migrate.py
# Compiled at: 2013-03-07 11:38:14
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, shutil
from random import shuffle
from tiddlyweb.config import config
from tiddlyweb.store import Store
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.user import User
from tiddlyweb.model.tiddler import Tiddler
from tiddlywebplugins.migrate import migrate_entities

def setup_module(module):
    environ = {'tiddlyweb.config': config}
    source_store = Store(config['server_store'][0], config['server_store'][1], environ)
    target_store = Store(config['target_store'][0], config['target_store'][1], environ)
    module.source_store = source_store
    module.target_store = target_store
    module.environ = environ
    base_content(source_store)


def reset_stores(new_only=False):
    for store_root in ['store', 'newstore']:
        if new_only and store_root is 'store':
            continue
        try:
            shutil.rmtree(store_root)
        except:
            pass

    if new_only:
        target_store = Store(config['target_store'][0], config['target_store'][1], environ)


def base_content(store):
    bags = [
     'one', 'two', 'three']
    for name in bags:
        bag = Bag(name)
        store.put(bag)
        for title in ['alpha', 'bravo', 'corpuscle']:
            tiddler = Tiddler(title, name)
            store.put(tiddler)

    for name in ['cake', 'pudding', 'sauce']:
        recipe = Recipe(name)
        shuffle(bags)
        recipe_list = [ (name, '') for name in bags ]
        recipe.set_recipe(recipe_list)
        store.put(recipe)

    for name in ['john', 'jane', 'clancy']:
        user = User(name)
        store.put(user)


def test_migrate_all():
    new_bags = target_store.list_bags()
    @py_assert3 = list(new_bags)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 0
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() is not @py_builtins.globals() else 'list', 'py2': @pytest_ar._saferepr(new_bags) if 'new_bags' in @py_builtins.locals() is not @py_builtins.globals() else 'new_bags', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    migrate_entities(source_store, target_store)
    new_bags = target_store.list_bags()
    @py_assert3 = list(new_bags)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() is not @py_builtins.globals() else 'list', 'py2': @pytest_ar._saferepr(new_bags) if 'new_bags' in @py_builtins.locals() is not @py_builtins.globals() else 'new_bags', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    new_recipes = target_store.list_recipes()
    @py_assert3 = list(new_recipes)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() is not @py_builtins.globals() else 'list', 'py2': @pytest_ar._saferepr(new_recipes) if 'new_recipes' in @py_builtins.locals() is not @py_builtins.globals() else 'new_recipes', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    new_users = target_store.list_users()
    @py_assert3 = list(new_users)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() is not @py_builtins.globals() else 'list', 'py2': @pytest_ar._saferepr(new_users) if 'new_users' in @py_builtins.locals() is not @py_builtins.globals() else 'new_users', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    new_tiddlers = target_store.list_bag_tiddlers(Bag('one'))
    @py_assert3 = list(new_tiddlers)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() is not @py_builtins.globals() else 'list', 'py2': @pytest_ar._saferepr(new_tiddlers) if 'new_tiddlers' in @py_builtins.locals() is not @py_builtins.globals() else 'new_tiddlers', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_migrate_one_bag():
    reset_stores(True)
    new_bags = target_store.list_bags()
    @py_assert3 = list(new_bags)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 0
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() is not @py_builtins.globals() else 'list', 'py2': @pytest_ar._saferepr(new_bags) if 'new_bags' in @py_builtins.locals() is not @py_builtins.globals() else 'new_bags', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    migrate_entities(source_store, target_store, ['one'])
    new_bags = target_store.list_bags()
    @py_assert3 = list(new_bags)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 1
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() is not @py_builtins.globals() else 'list', 'py2': @pytest_ar._saferepr(new_bags) if 'new_bags' in @py_builtins.locals() is not @py_builtins.globals() else 'new_bags', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    new_recipes = target_store.list_recipes()
    @py_assert3 = list(new_recipes)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 0
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() is not @py_builtins.globals() else 'list', 'py2': @pytest_ar._saferepr(new_recipes) if 'new_recipes' in @py_builtins.locals() is not @py_builtins.globals() else 'new_recipes', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    new_users = target_store.list_users()
    @py_assert3 = list(new_users)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 0
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() is not @py_builtins.globals() else 'list', 'py2': @pytest_ar._saferepr(new_users) if 'new_users' in @py_builtins.locals() is not @py_builtins.globals() else 'new_users', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    new_tiddlers = target_store.list_bag_tiddlers(Bag('one'))
    @py_assert3 = list(new_tiddlers)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() is not @py_builtins.globals() else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() is not @py_builtins.globals() else 'list', 'py2': @pytest_ar._saferepr(new_tiddlers) if 'new_tiddlers' in @py_builtins.locals() is not @py_builtins.globals() else 'new_tiddlers', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return