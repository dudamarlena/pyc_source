# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyweb-plugins/diststore/test/test_dist.py
# Compiled at: 2010-01-13 16:26:14
"""
Test that the disting actually dists.

This is obviously incomplete, but at leasts adds a
bit of coverage.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, shutil
from tiddlyweb.model.bag import Bag
from tiddlyweb.store import Store
SAMPLE_CONFIG = {'server_store': [
                  'tiddlywebplugins.diststore',
                  {'main': [
                            'text', {'store_root': 'store1'}], 
                     'extras': [
                              (
                               '^c', ['text', {'store_root': 'store2'}])]}]}
ENVIRON = {'tiddlyweb.config': SAMPLE_CONFIG}

def setup_module(module):
    for dir in ['store1', 'store2']:
        if os.path.exists(dir):
            shutil.rmtree(dir)


def test_where_it_goes():
    store = Store(SAMPLE_CONFIG['server_store'][0], SAMPLE_CONFIG['server_store'][1], environ=ENVIRON)
    bbag = Bag('bbag')
    cbag = Bag('cbag')
    store.put(bbag)
    store.put(cbag)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'store1/bags/bbag/tiddlers'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() is not @py_builtins.globals() else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'store2/bags/cbag/tiddlers'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() is not @py_builtins.globals() else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'store2/bags/bbag/tiddlers'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = not @py_assert7
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() is not @py_builtins.globals() else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'store1/bags/cbag/tiddlers'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = not @py_assert7
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() is not @py_builtins.globals() else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    return