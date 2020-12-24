# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.postgresql/test/test_search.py
# Compiled at: 2013-09-01 08:16:08
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, py.test
from tiddlyweb.config import config
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlywebplugins.utils import get_store
from tiddlywebplugins.postgresql import Base, index_query

def setup_module(module):
    module.store = get_store(config)
    module.environ = {'tiddlyweb.config': config, 'tiddlyweb.store': module.store}
    session = module.store.storage.session
    Base.metadata.drop_all()
    Base.metadata.create_all()


def test_simple_store():
    bag = Bag('bag1')
    store.put(bag)
    tiddler = Tiddler('tiddler1', 'bag1')
    tiddler.text = 'oh hello i chrisdent have nothing to say here you know'
    tiddler.tags = ['apple', 'orange', 'pear']
    tiddler.fields['house'] = 'cottage'
    store.put(tiddler)
    retrieved = Tiddler('tiddler1', 'bag1')
    retrieved = store.get(retrieved)
    @py_assert1 = retrieved.text
    @py_assert5 = tiddler.text
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py6)s\n{%(py6)s = %(py4)s.text\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(retrieved) if 'retrieved' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved) else 'retrieved', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    return


def test_simple_search():
    tiddlers = list(store.search('chrisdent'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'tiddler1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.bag
    @py_assert5 = 'bag1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.bag\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search('hello'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'tiddler1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.bag
    @py_assert5 = 'bag1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.bag\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_index_query_id():
    kwords = {'id': 'bag1:tiddler1'}
    tiddlers = list(index_query(environ, **kwords))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'tiddler1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.bag
    @py_assert5 = 'bag1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.bag\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_index_query_filter():
    kwords = {'tag': 'orange'}
    tiddlers = list(index_query(environ, **kwords))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'tiddler1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.bag
    @py_assert5 = 'bag1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.bag\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_index_query_filter_fields():
    kwords = {'house': 'cottage'}
    tiddlers = list(index_query(environ, **kwords))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'tiddler1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.bag
    @py_assert5 = 'bag1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.bag\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0].fields['house']
    @py_assert3 = 'cottage'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    kwords = {'house': 'mansion'}
    tiddlers = list(index_query(environ, **kwords))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_index_query_filter_fields():
    kwords = {'bag': 'bag1', 'house': 'cottage'}
    tiddlers = list(index_query(environ, **kwords))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'tiddler1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.bag
    @py_assert5 = 'bag1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.bag\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0].fields['house']
    @py_assert3 = 'cottage'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_search_right_revision():
    tiddler = Tiddler('revised', 'bag1')
    tiddler.text = 'alpha'
    tiddler.fields['house'] = 'cottage'
    store.put(tiddler)
    tiddler = Tiddler('revised', 'bag1')
    tiddler.text = 'beta'
    tiddler.fields['house'] = 'mansion'
    store.put(tiddler)
    tiddler = Tiddler('revised', 'bag1')
    tiddler.text = 'gamma'
    tiddler.fields['house'] = 'barn'
    store.put(tiddler)
    tiddler = Tiddler('revised', 'bag1')
    tiddler.text = 'delta'
    tiddler.fields['house'] = 'bungalow'
    store.put(tiddler)
    tiddler = Tiddler('revised', 'bag1')
    tiddler.text = 'epsilon'
    tiddler.fields['house'] = 'treehouse'
    store.put(tiddler)
    tiddlers = list(store.search('beta'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search('epsilon'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddler = store.get(Tiddler(tiddlers[0].title, tiddlers[0].bag))
    @py_assert1 = tiddler.title
    @py_assert4 = 'revised'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.bag
    @py_assert4 = 'bag1'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.bag\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = tiddler.fields['house']
    @py_assert3 = 'treehouse'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    kwords = {'bag': 'bag1', 'house': 'barn'}
    tiddlers = list(index_query(environ, **kwords))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    kwords = {'bag': 'bag1', 'house': 'treehouse'}
    tiddlers = list(index_query(environ, **kwords))
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'revised'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.bag
    @py_assert5 = 'bag1'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.bag\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0].fields['house']
    @py_assert3 = 'treehouse'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    kwords = {'bag': 'bag1', 'tag': 'orange'}
    tiddlers = list(index_query(environ, **kwords))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    kwords = {'bag': 'bag1', 'tag': 'rang'}
    tiddlers = list(index_query(environ, **kwords))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_search_follow_syntax():
    QUERY = 'ftitle:GettingStarted (bag:cdent_public OR bag:fnd_public)'
    store.put(Bag('fnd_public'))
    store.put(Bag('cdent_public'))
    tiddler = Tiddler('GettingStarted', 'fnd_public')
    tiddler.text = 'fnd starts'
    tiddler.fields['house'] = 'treehouse'
    tiddler.fields['car'] = 'porsche'
    store.put(tiddler)
    tiddler = Tiddler('GettingStarted', 'cdent_public')
    tiddler.text = 'cdent starts'
    tiddler.fields['left-hand'] = 'well dirty'
    store.put(tiddler)
    tiddler = Tiddler('other', 'cdent_public')
    tiddler.text = 'cdent starts'
    store.put(tiddler)
    tiddlers = list(store.search('starts'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 3
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search(QUERY))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search('cdent starts'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search('fnd starts'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddler = list(store.search('left-hand:"well dirty"'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_search_arbitrarily_complex():
    QUERY = 'ftitle:GettingStarted (bag:cdent_public OR bag:fnd_public) house:treehouse'
    tiddlers = list(store.search(QUERY))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    QUERY = 'ftitle:GettingStarted ((bag:cdent_public OR bag:fnd_public) AND (house:treehouse AND car:porsche))'
    tiddlers = list(store.search(QUERY))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_field_with_dot():
    tiddler = Tiddler('geoplace', 'cdent_public')
    tiddler.text = 'some place somewhere'
    tiddler.fields['geo.lat'] = '1.25'
    tiddler.fields['geo.long'] = '-45.243'
    store.put(tiddler)
    tiddlers = list(store.search('geo.lat:1.2*'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search('geo.lat:"1.2*" AND geo.long:"-45.*"'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search('geo.lat:"1.3*" AND geo.long:"-46.*"'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search('geo.lat:"1.2*" OR geo.long:"-46.*"'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_limited_search--- This code section failed: ---

 L. 206         0  LOAD_GLOBAL           0  'list'
                3  LOAD_GLOBAL           1  'store'
                6  LOAD_ATTR             2  'search'
                9  LOAD_CONST               'starts _limit:1'
               12  CALL_FUNCTION_1       1  None
               15  CALL_FUNCTION_1       1  None
               18  STORE_FAST            0  'tiddlers'

 L. 207        21  LOAD_GLOBAL           3  'len'
               24  LOAD_FAST             0  'tiddlers'
               27  CALL_FUNCTION_1       1  None
               30  LOAD_CONST               1
               33  COMPARE_OP            2  ==
               36  POP_JUMP_IF_TRUE     48  'to 48'
               39  LOAD_ASSERT              AssertionError
               42  LOAD_FAST             0  'tiddlers'
               45  RAISE_VARARGS_2       2  None

 L. 209        48  LOAD_GLOBAL           0  'list'
               51  LOAD_GLOBAL           1  'store'
               54  LOAD_ATTR             2  'search'
               57  LOAD_CONST               'starts'
               60  CALL_FUNCTION_1       1  None
               63  CALL_FUNCTION_1       1  None
               66  STORE_FAST            0  'tiddlers'

 L. 210        69  LOAD_GLOBAL           3  'len'
               72  LOAD_FAST             0  'tiddlers'
               75  CALL_FUNCTION_1       1  None
               78  LOAD_CONST               1
               81  COMPARE_OP            3  !=
               84  POP_JUMP_IF_TRUE     96  'to 96'
               87  LOAD_ASSERT              AssertionError
               90  LOAD_FAST             0  'tiddlers'
               93  RAISE_VARARGS_2       2  None

 L. 212        96  LOAD_GLOBAL           0  'list'
               99  LOAD_GLOBAL           1  'store'
              102  LOAD_ATTR             2  'search'
              105  LOAD_CONST               'starts _limit:so'
              108  CALL_FUNCTION_1       1  None
              111  CALL_FUNCTION_1       1  None
              114  STORE_FAST            0  'tiddlers'

 L. 213       117  LOAD_GLOBAL           3  'len'
              120  LOAD_FAST             0  'tiddlers'
              123  CALL_FUNCTION_1       1  None
              126  LOAD_CONST               1
              129  COMPARE_OP            3  !=
              132  POP_JUMP_IF_TRUE    144  'to 144'
              135  LOAD_ASSERT              AssertionError
              138  LOAD_FAST             0  'tiddlers'
              141  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_FAST' instruction at offset 138


def test_modified():
    """
    Note the multiple store.put in here are to create
    additional revisions to make sure that joins are
    sufficiently limited.
    """
    tiddler = Tiddler('GettingStarted', 'fnd_public')
    tiddler.modifier = 'fnd'
    store.put(tiddler)
    tiddlers = list(store.search('modifier:fnd'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddler = Tiddler('GettingStarted', 'fnd_public')
    tiddler.tags = ['monkey', 'cow', 'food']
    tiddler.modifier = 'cdent'
    store.put(tiddler)
    store.put(tiddler)
    store.put(tiddler)
    store.put(tiddler)
    tiddlers = list(store.search('modifier:fnd'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddler = Tiddler('GettingFancy', 'fnd_public')
    tiddler.tags = ['cow', 'food']
    tiddler.modifier = 'fnd'
    store.put(tiddler)
    store.put(tiddler)
    store.put(tiddler)
    store.put(tiddler)
    tiddlers = list(store.search('modifier:fnd OR modifier:cdent'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search('modifier:fnd NOT modifier:cdent'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search('modifier:fnd NOT (modifier:cdent OR title:GettingStarted)'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search('modifier:fnd AND modified:20*'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_not():
    py.test.skip('need better sql-fu to get this right')
    tiddlers = list(store.search('bag:fnd_public NOT tag:monkey'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_or_tags():
    tiddler = Tiddler('tagone', 'fnd_public')
    tiddler.text = 'hi @onething hello'
    tiddler.tags = ['one', 'three', 'five']
    store.put(tiddler)
    tiddler = Tiddler('tagtwo', 'fnd_public')
    tiddler.text = 'hi @twothing hello'
    tiddler.tags = ['two', 'four', 'six']
    store.put(tiddler)
    tiddlers = list(store.search('@twothing OR tag:one'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_at_tags():
    tiddler = Tiddler('tagat', 'fnd_public')
    tiddler.text = 'new stuff to not mess'
    tiddler.tags = ['one', 'three', 'five', '@cdent']
    store.put(tiddler)
    tiddlers = list(store.search('tag:@cdent'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_paren_title():
    tiddler = Tiddler('(i)', 'fnd_public')
    tiddler.text = 'hi @onething hello'
    tiddler.tags = ['one', 'three', 'five']
    store.put(tiddler)
    tiddlers = list(store.search('title:(i)'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = '(i)'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_text_as_field--- This code section failed: ---

 L. 310         0  LOAD_GLOBAL           0  'list'
                3  LOAD_GLOBAL           1  'store'
                6  LOAD_ATTR             2  'search'
                9  LOAD_CONST               'text:hello'
               12  CALL_FUNCTION_1       1  None
               15  CALL_FUNCTION_1       1  None
               18  STORE_FAST            0  'tiddlers'

 L. 312        21  LOAD_GLOBAL           3  'len'
               24  LOAD_FAST             0  'tiddlers'
               27  CALL_FUNCTION_1       1  None
               30  LOAD_CONST               4
               33  COMPARE_OP            2  ==
               36  POP_JUMP_IF_TRUE     48  'to 48'
               39  LOAD_ASSERT              AssertionError
               42  LOAD_FAST             0  'tiddlers'
               45  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_FAST' instruction at offset 42


def test_srevision_attr--- This code section failed: ---

 L. 315         0  LOAD_GLOBAL           0  'list'
                3  LOAD_GLOBAL           1  'store'
                6  LOAD_ATTR             2  'search'
                9  LOAD_CONST               'fields:hello'
               12  CALL_FUNCTION_1       1  None
               15  CALL_FUNCTION_1       1  None
               18  STORE_FAST            0  'tiddlers'

 L. 317        21  LOAD_GLOBAL           3  'len'
               24  LOAD_FAST             0  'tiddlers'
               27  CALL_FUNCTION_1       1  None
               30  LOAD_CONST               0
               33  COMPARE_OP            2  ==
               36  POP_JUMP_IF_TRUE     48  'to 48'
               39  LOAD_ASSERT              AssertionError
               42  LOAD_FAST             0  'tiddlers'
               45  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_FAST' instruction at offset 42


def test_tiddler_field_join():
    tiddler = Tiddler('fieldtest', 'fnd_public')
    tiddler.text = 'hi again'
    tiddler.fields = {'barney': 'evil', 
       'soup': 'good'}
    store.put(tiddler)
    tiddlers = list(store.search('barney:evil'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'fieldtest'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    tiddlers = list(store.search('barney:evil AND soup:good'))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'fieldtest'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    return