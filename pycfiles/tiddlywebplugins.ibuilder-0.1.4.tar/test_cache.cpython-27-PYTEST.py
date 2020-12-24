# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.ibuilder/test/test_cache.py
# Compiled at: 2013-08-01 11:55:53
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, shutil
from tiddlywebplugins.ibuilder import cache_tiddlers

def setup_module(module):
    try:
        shutil.rmtree('testpackage/resources')
    except:
        pass


def test_cache():
    cache_tiddlers('testpackage')
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store/bags/bagone/tiddlers/'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store/bags/bagone/tiddlers/test'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert5 = 'testpackage/resources/store/bags/bagone/tiddlers/file.css'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    return