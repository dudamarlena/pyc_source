# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.caching/test/test_bag_handling.py
# Compiled at: 2011-12-23 11:32:57
"""
A bug was discovered wherein revisions were
not being deleted from the cache properly.
This test confirms it is fixed. In the process
it should confirm generally workingness.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, shutil
from tiddlyweb.config import config
from tiddlyweb.store import Store, NoTiddlerError
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
import py.test

def setup_module(module):
    if os.path.exists('store'):
        shutil.rmtree('store')
    module.store = Store(config['server_store'][0], config['server_store'][1], environ={'tiddlyweb.config': config})
    try:
        bag = Bag('holder')
        module.store.delete(bag)
    except:
        pass

    bag = Bag('holder')
    module.store.put(bag)


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


def test_put_tiddlers_delete_bag():
    tiddler = Tiddler('tiddler1', 'holder')
    tiddler.text = 'one'
    store.put(tiddler)
    tiddler = Tiddler('tiddler2', 'holder')
    tiddler.text = 'two'
    store.put(tiddler)
    retrieved = Tiddler('tiddler1', 'holder')
    retrieved = store.get(retrieved)
    @py_assert1 = retrieved.text
    @py_assert4 = 'one'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = retrieved.bag
    @py_assert4 = 'holder'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.bag\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    retrieved = Tiddler('tiddler2', 'holder')
    retrieved = store.get(retrieved)
    @py_assert1 = retrieved.text
    @py_assert4 = 'two'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = retrieved.bag
    @py_assert4 = 'holder'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.bag\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    bag = Bag('holder')
    store.delete(bag)
    py.test.raises(NoTiddlerError, 'store.get(retrieved)')
    return


def test_get_bag():
    bag = Bag('thing')
    bag.desc = 'stuff'
    store.put(bag)
    if hasattr(bag, 'list_tiddlers'):
        retrieved = Bag('thing')
        retrieved.skinny = True
        retrieved = store.get(retrieved)
        @py_assert1 = retrieved.desc
        @py_assert4 = 'stuff'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.desc\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        retrieved = Bag('thing')
        retrieved = store.get(retrieved)
        @py_assert1 = retrieved.desc
        @py_assert4 = 'stuff'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.desc\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
    else:
        retrieved = Bag('thing')
        retrieved = store.get(retrieved)
        @py_assert1 = retrieved.desc
        @py_assert4 = 'stuff'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.desc\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_get_bags():
    bags = store.list_bags()
    bags = store.list_bags()
    for name in ['alpha', 'beta', 'gamma']:
        store.put(Bag(name))

    bags = store.list_bags()
    @py_assert0 = 'alpha'
    @py_assert3 = [ bag.name for bag in bags ]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_listing_tiddlers():
    for title in ['hi', 'bye', 'greetings', 'salutations']:
        tiddler = Tiddler(title, 'thing')
        tiddler.text = title
        store.put(tiddler)

    tiddlers1 = list(store.list_bag_tiddlers(Bag('thing')))
    tiddlers2 = list(store.list_bag_tiddlers(Bag('thing')))
    @py_assert2 = len(tiddlers1)
    @py_assert7 = len(tiddlers2)
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}',), (@py_assert2, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers1) if 'tiddlers1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers1) else 'tiddlers1', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(tiddlers2) if 'tiddlers2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers2) else 'tiddlers2'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    tiddler = Tiddler('adios', 'thing')
    tiddler.text = 'adios'
    store.put(tiddler)
    tiddlers3 = list(store.list_bag_tiddlers(Bag('thing')))
    tiddlers4 = list(store.list_bag_tiddlers(Bag('thing')))
    @py_assert2 = len(tiddlers1)
    @py_assert7 = len(tiddlers3)
    @py_assert4 = @py_assert2 != @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('!=',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} != %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}',), (@py_assert2, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers1) if 'tiddlers1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers1) else 'tiddlers1', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(tiddlers3) if 'tiddlers3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers3) else 'tiddlers3'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert2 = len(tiddlers3)
    @py_assert7 = len(tiddlers4)
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}',), (@py_assert2, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers3) if 'tiddlers3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers3) else 'tiddlers3', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(tiddlers4) if 'tiddlers4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers4) else 'tiddlers4'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    return