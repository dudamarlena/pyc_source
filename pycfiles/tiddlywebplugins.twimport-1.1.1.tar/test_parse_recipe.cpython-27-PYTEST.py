# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.twimport/test/test_parse_recipe.py
# Compiled at: 2013-11-12 13:36:08
"""
First stab, parsing recipes.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from tiddlywebplugins.twimport import recipe_to_urls
SAMPLE = './test/samples/alpha/index.html.recipe'
URL_SAMPLE = 'file:' + os.path.abspath(SAMPLE)

def test_parse_recipe_path_or_url():
    urls_path = recipe_to_urls(SAMPLE)
    urls_url = recipe_to_urls(URL_SAMPLE)
    @py_assert1 = urls_path == urls_url
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (urls_path, urls_url)) % {'py0': @pytest_ar._saferepr(urls_path) if 'urls_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(urls_path) else 'urls_path', 'py2': @pytest_ar._saferepr(urls_url) if 'urls_url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(urls_url) else 'urls_url'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def test_parse_recipe_results():
    urls = recipe_to_urls(SAMPLE)
    @py_assert0 = 'https://raw.github.com/TiddlyWiki/tiddlywiki/master/shadows/ColorPalette.tid'
    @py_assert2 = @py_assert0 in urls
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, urls)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(urls) if 'urls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(urls) else 'urls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'https://raw.github.com/TiddlyWiki/tiddlywiki/master/shadows/ViewTemplate.tid'
    @py_assert2 = @py_assert0 in urls
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, urls)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(urls) if 'urls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(urls) else 'urls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    filenames = [ os.path.basename(url.split(' ', 1)[0]) for url in urls ]
    @py_assert2 = len(filenames)
    @py_assert5 = 10
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(filenames) if 'filenames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filenames) else 'filenames', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = 'aplugin.js'
    @py_assert2 = @py_assert0 in filenames
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, filenames)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(filenames) if 'filenames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filenames) else 'filenames'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'bplugin.js'
    @py_assert2 = @py_assert0 in filenames
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, filenames)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(filenames) if 'filenames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filenames) else 'filenames'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'Welcome.tid'
    @py_assert2 = @py_assert0 in filenames
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, filenames)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(filenames) if 'filenames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filenames) else 'filenames'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'Greetings.tiddler'
    @py_assert2 = @py_assert0 in filenames
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, filenames)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(filenames) if 'filenames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filenames) else 'filenames'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'Empty.tiddler'
    @py_assert2 = @py_assert0 in filenames
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, filenames)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(filenames) if 'filenames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filenames) else 'filenames'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'Hello.tid'
    @py_assert2 = @py_assert0 in filenames
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, filenames)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(filenames) if 'filenames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filenames) else 'filenames'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'hole.js'
    @py_assert2 = @py_assert0 in filenames
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, filenames)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(filenames) if 'filenames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filenames) else 'filenames'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'ColorPalette.tid'
    @py_assert2 = @py_assert0 in filenames
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, filenames)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(filenames) if 'filenames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filenames) else 'filenames'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'ViewTemplate.tid'
    @py_assert2 = @py_assert0 in filenames
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, filenames)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(filenames) if 'filenames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filenames) else 'filenames'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'normalize.css'
    @py_assert2 = @py_assert0 in filenames
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, filenames)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(filenames) if 'filenames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filenames) else 'filenames'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return