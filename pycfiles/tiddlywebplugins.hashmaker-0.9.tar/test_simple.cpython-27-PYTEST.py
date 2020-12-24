# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.hashmaker/test/test_simple.py
# Compiled at: 2010-09-27 14:56:07
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlyweb.config import config
from tiddlywebplugins.utils import get_store
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlywebplugins.hashmaker import init, hash_tiddler_hook

def setup_module(module):
    init(config)
    module.store = get_store(config)


def test_default_hash_generation():
    tiddler1 = Tiddler('hi')
    tiddler1.text = 'hello'
    @py_assert0 = '_hash'
    @py_assert4 = tiddler1.fields
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s.fields\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler1) if 'tiddler1' in @py_builtins.locals() is not @py_builtins.globals() else 'tiddler1', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    hash_tiddler_hook(store.storage, tiddler1)
    @py_assert0 = '_hash'
    @py_assert4 = tiddler1.fields
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.fields\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler1) if 'tiddler1' in @py_builtins.locals() is not @py_builtins.globals() else 'tiddler1', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    tiddler2 = Tiddler('bye')
    tiddler2.text = 'hello'
    hash_tiddler_hook(store.storage, tiddler2)
    @py_assert0 = tiddler1.fields['_hash']
    @py_assert3 = tiddler2.fields['_hash']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    tiddler2.text = 'goodbye'
    del tiddler2.fields['_hash']
    hash_tiddler_hook(store.storage, tiddler2)
    @py_assert0 = tiddler1.fields['_hash']
    @py_assert3 = tiddler2.fields['_hash']
    @py_assert2 = @py_assert0 != @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert2,), ('%(py1)s != %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_complex_hash_generation():
    config['hashmaker.attributes'] = [
     'text', 'karma']
    tiddler1 = Tiddler('hi')
    tiddler1.text = 'hello'
    tiddler1.fields['karma'] = 'bad'
    hash_tiddler_hook(store.storage, tiddler1)
    tiddler2 = Tiddler('bye')
    tiddler2.text = 'hello'
    tiddler2.fields['karma'] = 'bad'
    hash_tiddler_hook(store.storage, tiddler2)
    @py_assert0 = tiddler1.fields['_hash']
    @py_assert3 = tiddler2.fields['_hash']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    tiddler2.fields['karma'] = 'good'
    del tiddler2.fields['_hash']
    hash_tiddler_hook(store.storage, tiddler2)
    @py_assert0 = tiddler1.fields['_hash']
    @py_assert3 = tiddler2.fields['_hash']
    @py_assert2 = @py_assert0 != @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert2,), ('%(py1)s != %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    config['hashmaker.attributes'] = [
     'text']
    del tiddler1.fields['_hash']
    del tiddler2.fields['_hash']
    hash_tiddler_hook(store.storage, tiddler1)
    hash_tiddler_hook(store.storage, tiddler2)
    @py_assert0 = tiddler1.fields['_hash']
    @py_assert3 = tiddler2.fields['_hash']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_store_hook():
    bag = Bag('nancy')
    store.put(bag)
    tiddler1 = Tiddler('hi', 'nancy')
    tiddler1.text = 'hello'
    store.put(tiddler1)
    tiddler2 = Tiddler('hi', 'nancy')
    tiddler2 = store.get(tiddler2)
    @py_assert0 = '_hash'
    @py_assert4 = tiddler2.fields
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.fields\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler2) if 'tiddler2' in @py_builtins.locals() is not @py_builtins.globals() else 'tiddler2', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    hash_tiddler_hook(store.storage, tiddler1)
    @py_assert0 = tiddler1.fields['_hash']
    @py_assert3 = tiddler2.fields['_hash']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return