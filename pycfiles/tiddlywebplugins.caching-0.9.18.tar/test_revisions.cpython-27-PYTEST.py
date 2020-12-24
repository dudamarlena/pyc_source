# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.caching/test/test_revisions.py
# Compiled at: 2011-12-19 07:39:48
"""
A bug was discovered wherein revisions were
not being deleted from the cache properly.
This test confirms it is fixed. In the process
it should confirm generally workingness.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlyweb.config import config
from tiddlyweb.store import Store, NoTiddlerError
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
import py.test

def setup_module(module):
    module.store = Store(config['server_store'][0], config['server_store'][1], environ={'tiddlyweb.config': config})
    try:
        bag = Bag('holder')
        store.delete(bag)
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


def test_put_get_tiddlers():
    tiddler = Tiddler('tiddler1', 'holder')
    tiddler.text = 'rev1'
    store.put(tiddler)
    tiddler.text = 'rev2'
    store.put(tiddler)
    tiddler.text = 'rev3'
    store.put(tiddler)
    retrieved = Tiddler('tiddler1', 'holder')
    retrieved = store.get(retrieved)
    @py_assert1 = retrieved.revision
    @py_assert4 = 3
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.revision\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = retrieved.text
    @py_assert4 = 'rev3'
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
    retrieved.revision = 1
    retrieved = store.get(retrieved)
    @py_assert1 = retrieved.revision
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.revision\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = retrieved.text
    @py_assert4 = 'rev1'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    retrieved.revision = 2
    retrieved = store.get(retrieved)
    @py_assert1 = retrieved.revision
    @py_assert4 = 2
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.revision\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = retrieved.text
    @py_assert4 = 'rev2'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_delete_gets_revisions():
    """this relies on the previous test"""
    removed = Tiddler('tiddler1', 'holder')
    store.delete(removed)
    revision = Tiddler('tiddler1', 'holder')
    revision.revision = 2
    py.test.raises(NoTiddlerError, 'store.get(revision)')