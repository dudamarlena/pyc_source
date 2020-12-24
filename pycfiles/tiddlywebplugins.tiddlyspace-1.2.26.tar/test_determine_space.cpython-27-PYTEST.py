# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_determine_space.py
# Compiled at: 2010-11-24 00:13:20
"""
Note: This tests doesn't do much any more as 
_determine space has become too complex and needs
more environment information to get fully tested.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlywebplugins.tiddlyspace.handler import determine_space
config = {'server_host': {'scheme': 'http', 
                   'host': '0.0.0.0', 
                   'port': '8080'}}
environ = {'tiddlyweb.config': config}

def test_simple_space():
    space = determine_space(environ, 'foo.0.0.0.0:8080')
    @py_assert2 = 'foo'
    @py_assert1 = space == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (space, @py_assert2)) % {'py0': @pytest_ar._saferepr(space) if 'space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space) else 'space', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    space = determine_space(environ, 'foo.bar.0.0.0.0:8080')
    @py_assert2 = 'foo.bar'
    @py_assert1 = space == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (space, @py_assert2)) % {'py0': @pytest_ar._saferepr(space) if 'space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space) else 'space', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return