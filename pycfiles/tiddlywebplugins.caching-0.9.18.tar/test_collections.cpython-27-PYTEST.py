# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.caching/test/test_collections.py
# Compiled at: 2011-12-23 11:34:14
"""
Collection (list_*) code was added without tests and since then some
bugs have been found. This tries to at least get some coverage of
the code. Not to check full correctness, just to exercise.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, shutil
from tiddlyweb.config import config
from tiddlyweb.store import Store, StoreError
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.user import User
import py.test

def setup_module(module):
    if os.path.exists('store'):
        shutil.rmtree('store')
    module.store = Store(config['server_store'][0], config['server_store'][1], environ={'tiddlyweb.config': config})
    module.store.storage.mc.flush_all()


def test_memcache_up():
    store.storage.mc.set('keyone', 'valueone')
    @py_assert1 = store.storage
    @py_assert3 = @py_assert1.mc
    @py_assert5 = @py_assert3.get
    @py_assert7 = 'keyone'
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert12 = 'valueone'
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.storage\n}.mc\n}.get\n}(%(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(store) if 'store' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(store) else 'store', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    store.storage.mc.delete('keyone')
    return


def test_list_users():
    user = User('monkey')
    store.put(user)
    users = list(store.list_users())
    @py_assert2 = len(users)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(users) if 'users' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(users) else 'users', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    store.get(users[0])
    store.delete(user)
    users = list(store.list_users())
    @py_assert2 = len(users)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(users) if 'users' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(users) else 'users', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_list_recipes():
    recipe = Recipe('monkey')
    store.put(recipe)
    recipes = list(store.list_recipes())
    @py_assert2 = len(recipes)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(recipes) if 'recipes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipes) else 'recipes', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    store.get(recipes[0])
    store.delete(recipe)
    recipes = list(store.list_recipes())
    @py_assert2 = len(recipes)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(recipes) if 'recipes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipes) else 'recipes', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return