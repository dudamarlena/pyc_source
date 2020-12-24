# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.pkgstore/test/test_write_store.py
# Compiled at: 2013-07-20 12:40:18
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, shutil, py.test
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.user import User
from tiddlyweb.store import Store, StoreMethodNotImplemented, StoreError
from tiddlyweb.config import config
from tiddlywebplugins.pkgstore import ReadOnlyError

def setup_module(module):
    try:
        shutil.rmtree('testpackage/resources/store')
    except:
        pass

    environ = {'tiddlyweb.config': config}
    wstore = Store('tiddlywebplugins.pkgstore', {'package': 'testpackage', 'read_only': False}, environ)
    module.wstore = wstore
    rstore = Store('tiddlywebplugins.pkgstore', {'package': 'testpackage', 'read_only': True}, environ)
    module.rstore = rstore


def test_base_structure():
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isdir
    @py_assert5 = 'testpackage/resources/store'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isdir\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store/recipes'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isdir
    @py_assert5 = 'testpackage/resources/store/recipes'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isdir\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store/bags'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isdir
    @py_assert5 = 'testpackage/resources/store/bags'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isdir\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store/users'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isdir
    @py_assert5 = 'testpackage/resources/store/users'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isdir\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    return


def test_put_bag():
    bag = Bag('testone')
    wstore.put(bag)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store/bags/testone'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isdir
    @py_assert5 = 'testpackage/resources/store/bags/testone'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isdir\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    return


def test_put_recipe():
    recipe = Recipe('testone')
    wstore.put(recipe)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store/recipes/testone'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isfile
    @py_assert5 = 'testpackage/resources/store/recipes/testone'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isfile\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    wstore.delete(recipe)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store/recipes/testone'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = not @py_assert7
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    return


def test_put_tiddler():
    tiddler = Tiddler('tiddlerone', 'testone')
    tiddler.text = 'oh hi'
    wstore.put(tiddler)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store/bags/testone/tiddlers/tiddlerone'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isdir
    @py_assert5 = 'testpackage/resources/store/bags/testone/tiddlers/tiddlerone'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isdir\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    with open('testpackage/resources/store/bags/testone/tiddlers/tiddlerone/1') as (tiddler_file):
        content = tiddler_file.read().split('\n\n')[1].strip()
        @py_assert2 = 'oh hi'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0': @pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
    return


def test_get_tiddler():
    tiddler = Tiddler('tiddlerone', 'testone')
    tiddler = wstore.get(tiddler)
    @py_assert1 = tiddler.text
    @py_assert4 = 'oh hi'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    tiddler = rstore.get(tiddler)
    @py_assert1 = tiddler.text
    @py_assert4 = 'oh hi'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    py.test.raises(ReadOnlyError, 'rstore.put(tiddler)')
    py.test.raises(ReadOnlyError, 'rstore.delete(tiddler)')
    wstore.delete(tiddler)
    py.test.raises(StoreError, 'rstore.get(tiddler)')
    return


def test_skip_bags():
    bag = Bag('skippedbag')
    wstore.put(bag)
    tiddler = Tiddler('thing', 'skippedbag')
    wstore.put(tiddler)
    config['pkgstore.skip_bags'] = [
     'skippedbag']
    bag = wstore.get(Bag('skippedbag'))
    py.test.raises(StoreError, 'rstore.get(Bag("skippedbag"))')
    tiddler = wstore.get(Tiddler('thing', 'skippedbag'))
    py.test.raises(StoreError, 'rstore.get(Tiddler("thing", "skippedbag"))')
    bags = wstore.list_bags()
    @py_assert3 = list(bags)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 2
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py2': @pytest_ar._saferepr(bags) if 'bags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bags) else 'bags', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    bags = rstore.list_bags()
    @py_assert3 = list(bags)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 1
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py2': @pytest_ar._saferepr(bags) if 'bags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bags) else 'bags', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_cover_write_and_readonly():
    recipe = Recipe('testone')
    wstore.put(recipe)
    recipe2 = rstore.get(recipe)
    @py_assert1 = recipe2.name
    @py_assert5 = recipe.name
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py6)s\n{%(py6)s = %(py4)s.name\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(recipe2) if 'recipe2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe2) else 'recipe2', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    py.test.raises(ReadOnlyError, 'rstore.put(recipe)')
    py.test.raises(ReadOnlyError, 'rstore.delete(recipe)')
    bag = Bag('testone')
    wstore.put(bag)
    bag2 = rstore.get(bag)
    @py_assert1 = bag2.name
    @py_assert5 = bag.name
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py6)s\n{%(py6)s = %(py4)s.name\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(bag2) if 'bag2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag2) else 'bag2', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    py.test.raises(ReadOnlyError, 'rstore.put(bag)')
    py.test.raises(ReadOnlyError, 'rstore.delete(bag)')
    wstore.delete(bag)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store/bags/testone'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = not @py_assert7
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    return


def test_user_not_supported():
    user = User('me')
    py.test.raises(StoreMethodNotImplemented, 'rstore.put(user)')
    py.test.raises(StoreMethodNotImplemented, 'rstore.get(user)')
    py.test.raises(StoreMethodNotImplemented, 'rstore.delete(user)')