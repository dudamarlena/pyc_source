# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.twimport/test/test_wiki_to_tiddlers.py
# Compiled at: 2010-12-12 07:00:33
"""
test importing a wiki.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
WIKI_HTML_FILE = 'test/samples/tiddlers.html'
WIKI_WIKI_FILE = 'test/samples/tiddlers.wiki'
from tiddlywebplugins.twimport import wiki_to_tiddlers

def test_wiki_wiki_to_tiddlers():
    tiddlers = wiki_to_tiddlers(WIKI_WIKI_FILE)
    @py_assert2 = len(tiddlers)
    @py_assert5 = 9
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    titles = [ tiddler.title for tiddler in tiddlers ]
    @py_assert0 = 'oog'
    @py_assert2 = @py_assert0 in titles
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, titles)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(titles) if 'titles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(titles) else 'titles'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'codeblocked'
    @py_assert2 = @py_assert0 in titles
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, titles)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(titles) if 'titles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(titles) else 'titles'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tag_info = {}
    tag_info = dict([ (tiddler.title, tiddler.tags) for tiddler in tiddlers ])
    @py_assert0 = 'systemConfig'
    @py_assert3 = tag_info['TiddlyWebAdaptor']
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'FND'
    @py_assert3 = tag_info['codeblocked']
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    for _, values in tag_info.items():
        @py_assert0 = 'None'
        @py_assert2 = @py_assert0 not in values
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, values)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(values) if 'values' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(values) else 'values'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    return


def test_wiki_html_to_tiddlers():
    tiddlers = wiki_to_tiddlers(WIKI_HTML_FILE)
    @py_assert2 = len(tiddlers)
    @py_assert5 = 9
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    titles = [ tiddler.title for tiddler in tiddlers ]
    @py_assert0 = 'oog'
    @py_assert2 = @py_assert0 in titles
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, titles)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(titles) if 'titles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(titles) else 'titles'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'codeblocked'
    @py_assert2 = @py_assert0 in titles
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, titles)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(titles) if 'titles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(titles) else 'titles'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tag_info = {}
    tag_info = dict([ (tiddler.title, tiddler.tags) for tiddler in tiddlers ])
    @py_assert0 = 'systemConfig'
    @py_assert3 = tag_info['TiddlyWebAdaptor']
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'FND'
    @py_assert3 = tag_info['codeblocked']
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    for _, values in tag_info.items():
        @py_assert0 = 'None'
        @py_assert2 = @py_assert0 not in values
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, values)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(values) if 'values' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(values) else 'values'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    return