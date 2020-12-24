# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.twimport/test/test_import_one.py
# Compiled at: 2013-11-12 13:36:08
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlyweb.config import config
from tiddlyweb.store import Store, NoBagError
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlywebplugins.twimport import import_one

def setup_module(module):
    module.store = Store(config['server_store'][0], config['server_store'][1], {'tiddlyweb.config': config})
    _cleanup(module.store)


def _cleanup(store):
    bag = Bag('testone')
    try:
        store.delete(bag)
    except NoBagError:
        pass

    store.put(bag)


def test_import_one_wiki():
    import_one('testone', 'test/samples/tiddlers.wiki', store)
    bag = store.get(Bag('testone'))
    @py_assert3 = store.list_bag_tiddlers
    @py_assert6 = @py_assert3(bag)
    @py_assert8 = list(@py_assert6)
    @py_assert10 = len(@py_assert8)
    @py_assert13 = 9
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s.list_bag_tiddlers\n}(%(py5)s)\n})\n})\n} == %(py14)s',), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py2': @pytest_ar._saferepr(store) if 'store' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(store) else 'store', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    return


def test_import_one_html_wiki():
    import_one('testone', 'test/samples/tiddlers.html', store)
    bag = store.get(Bag('testone'))
    @py_assert3 = store.list_bag_tiddlers
    @py_assert6 = @py_assert3(bag)
    @py_assert8 = list(@py_assert6)
    @py_assert10 = len(@py_assert8)
    @py_assert13 = 9
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s.list_bag_tiddlers\n}(%(py5)s)\n})\n})\n} == %(py14)s',), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py2': @pytest_ar._saferepr(store) if 'store' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(store) else 'store', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    return


def test_import_one_recipe():
    import_one('testone', 'test/samples/alpha/index.html.recipe', store)
    bag = store.get(Bag('testone'))
    @py_assert3 = store.list_bag_tiddlers
    @py_assert6 = @py_assert3(bag)
    @py_assert8 = list(@py_assert6)
    @py_assert10 = len(@py_assert8)
    @py_assert13 = 19
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s.list_bag_tiddlers\n}(%(py5)s)\n})\n})\n} == %(py14)s',), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py2': @pytest_ar._saferepr(store) if 'store' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(store) else 'store', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    return


def test_import_one_tiddler():
    import_one('testone', 'test/samples/alpha/plugins/bplugin.js', store)
    bag = store.get(Bag('testone'))
    @py_assert3 = store.list_bag_tiddlers
    @py_assert6 = @py_assert3(bag)
    @py_assert8 = list(@py_assert6)
    @py_assert10 = len(@py_assert8)
    @py_assert13 = 19
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s.list_bag_tiddlers\n}(%(py5)s)\n})\n})\n} == %(py14)s',), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py2': @pytest_ar._saferepr(store) if 'store' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(store) else 'store', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    tiddler = store.get(Tiddler('bplugin', 'testone'))
    @py_assert1 = tiddler.type
    @py_assert4 = 'text/javascript'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.text
    @py_assert4 = "alert('i am here');"
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_import_one_wiki_fragment():
    _cleanup(store)
    import_one('testone', 'test/samples/tiddlers.wiki#codeblocked', store)
    bag = store.get(Bag('testone'))
    tiddlers = list(store.list_bag_tiddlers(bag))
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
    @py_assert5 = 'codeblocked'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_import_one_recipe_fragment():
    _cleanup(store)
    import_one('testone', 'test/samples/alpha/index.html.recipe#Greetings', store)
    bag = store.get(Bag('testone'))
    tiddlers = list(store.list_bag_tiddlers(bag))
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
    @py_assert5 = 'Greetings'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_import_one_js_meta():
    import_one('testone', 'test/samples/alpha/plugins/metaplugin.js', store)
    tiddler = store.get(Tiddler('metaplugin', 'testone'))
    @py_assert1 = tiddler.title
    @py_assert4 = 'metaplugin'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.tags
    @py_assert4 = ['alpha', 'beta']
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.tags\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_import_one_css_meta():
    import_one('testone', 'test/samples/alpha/fnord.css', store)
    tiddler = store.get(Tiddler('fnord.css', 'testone'))
    @py_assert1 = tiddler.title
    @py_assert4 = 'fnord.css'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.type
    @py_assert4 = 'text/css'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.tags
    @py_assert4 = ['alpha', 'beta']
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.tags\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_import_one_css_type():
    import_one('testone', 'https://github.com/necolas/normalize.css/raw/master/normalize.css text/css', store)
    tiddler = store.get(Tiddler('normalize.css', 'testone'))
    @py_assert1 = tiddler.title
    @py_assert4 = 'normalize.css'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.type
    @py_assert4 = 'text/css'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.tags
    @py_assert4 = []
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.tags\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return