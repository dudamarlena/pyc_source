# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebwiki/test/test_serialize_tiddler.py
# Compiled at: 2014-02-24 07:12:15
"""
Tests for turning a Tiddler into HTML within a TiddlyWiki document
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.serializer import Serializer
from tiddlyweb.config import config
from tiddlywebwiki.serialization import SPLITTER
BASE_TIDDLYWIKI = 'tiddlywebwiki/resources/empty.html'
config['base_tiddlywiki'] = BASE_TIDDLYWIKI
environ = {'tiddlyweb.config': config}

def test_html_attribute_escape_with_recipe():
    tiddler = Tiddler('escape "double" quotes & &amp; in <tiddler> field values')
    tiddler.bag = 'foo "bar" baz'
    tiddler.recipe = 'baz "bar" foo'
    tiddler.modifier = 'Chris "sensei" Dent'
    tiddler.tags = ['foo', 'xxx "yyy" zzz']
    tiddler.fields['custom'] = 'lorem \'ipsum\' dolor "sit" amet'
    tiddler.text = ''
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    @py_assert0 = 'title="escape &quot;double&quot; quotes &amp; &amp;amp; in &lt;tiddler&gt; field values"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'server.title="escape &quot;double&quot; quotes &amp; &amp;amp; in &lt;tiddler&gt; field values"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'bag="foo &quot;bar&quot; baz"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'recipe="baz &quot;bar&quot; foo"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'server.workspace="bags/foo &quot;bar&quot; baz"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'modifier="Chris &quot;sensei&quot; Dent"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'creator="Chris &quot;sensei&quot; Dent"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'tags="foo [[xxx &quot;yyy&quot; zzz]]"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'custom="lorem \'ipsum\' dolor &quot;sit&quot; amet"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'you may still <a href="/bags/foo%20%22bar%22%20baz/tiddlers/escape%20%22double%22%20quotes%20%26%20%26amp%3B%20in%20%3Ctiddler%3E%20field%20values">browse'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_html_attribute_escape_with_bag():
    tiddler = Tiddler('escape "double" quotes in tiddler field values')
    tiddler.bag = 'foo "bar" baz'
    tiddler.modifier = 'Chris "sensei" Dent'
    tiddler.tags = ['foo', 'xxx "yyy" zzz']
    tiddler.fields['custom'] = 'lorem \'ipsum\' dolor "sit" amet'
    tiddler.text = ''
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    @py_assert0 = 'title="escape &quot;double&quot; quotes in tiddler field values"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'server.title="escape &quot;double&quot; quotes in tiddler field values"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'bag="foo &quot;bar&quot; baz"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'server.workspace="bags/foo &quot;bar&quot; baz"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'modifier="Chris &quot;sensei&quot; Dent"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'creator="Chris &quot;sensei&quot; Dent"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'tags="foo [[xxx &quot;yyy&quot; zzz]]"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'custom="lorem \'ipsum\' dolor &quot;sit&quot; amet"'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'you may still <a href="/bags/foo%20%22bar%22%20baz/tiddlers/escape%20%22double%22%20quotes%20in%20tiddler%20field%20values">browse'
    @py_assert2 = @py_assert0 in string
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, string)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_content_type():
    tiddler = Tiddler('Foo', 'Alpha')
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('Foo', string)
    @py_assert0 = 'server.content-type=""'
    @py_assert2 = @py_assert0 in tiddler
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, tiddler)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tiddler = Tiddler('_Foo', 'Alpha')
    tiddler.type = 'None'
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('_Foo', string)
    @py_assert0 = 'server.content-type=""'
    @py_assert2 = @py_assert0 in tiddler
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, tiddler)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tiddler = Tiddler('Bar', 'Bravo')
    tiddler.type = 'text/x-custom'
    tiddler.text = 'lorem ipsum dolor sit amet'
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('Bar', string)
    @py_assert0 = 'server.content-type="text/x-custom"'
    @py_assert2 = @py_assert0 in tiddler
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, tiddler)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '<pre>lorem ipsum dolor sit amet</pre>'
    @py_assert2 = @py_assert0 in tiddler
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, tiddler)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    tiddler = Tiddler('Baz', 'Charlie')
    tiddler.type = 'application/x-custom'
    tiddler.text = 'lorem ipsum dolor sit amet'
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('Baz', string)
    @py_assert0 = 'server.content-type="application/x-custom"'
    @py_assert2 = @py_assert0 in tiddler
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, tiddler)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_server_etag():
    tiddler = Tiddler('Foo', 'Alpha')
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('Foo', string)
    @py_assert0 = 'server.etag="&quot;Alpha/Foo/'
    @py_assert2 = @py_assert0 in tiddler
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, tiddler)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def _extract_tiddler(title, wiki):
    """
    helper function to extract a tiddler DIV from a TiddlyWiki string

    tiddlywebplugins.twimport:wiki_string_to_tiddlers does this better
    """
    tiddlystart, tiddlyfinish = wiki.split(SPLITTER, 2)
    tiddlystart, store = tiddlystart.split('<div id="storeArea">', 2)
    splitter = '<div title='
    for tiddler in store.split(splitter):
        if tiddler.startswith('"%s"' % title):
            return splitter + tiddler