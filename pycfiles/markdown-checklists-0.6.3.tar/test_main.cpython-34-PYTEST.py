# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: X:\markdown-checklist\test\test_main.py
# Compiled at: 2015-09-02 16:06:57
# Size of source mod 2**32: 10744 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from markdown import markdown
from markdown_checklists.extension import ChecklistsExtension

def test_checklists():
    source = '\nHello World\n===========\n\n* [ ] foo\n* [x] bar\n* [ ] baz\n* [ ]\n* [x]\n* [ ] Der Unit-Test `contextMenuReplacesText` wurde auskommentiert um die ausfuehrung zu verhindern. Dieser Test funktioniert in meiner Umgebung nicht wie erwachtet. (Tastatur Layout?, Aktivierte Sprache des Betriebsystems?) Datei: `X:\\pdfsam\\pdfsam-fx\\src\\test\\java\\org\\pdfsam\\ui\\prefix\\PrefixFieldTest.java`\n* [ ] What do you know about Magnolia configuration?\n+ * [ ] Do you know about the magnolia repository and workspaces?\n+ * [ ] Do you understand the Node2Bean mechanism?\n+ * [ ] Do you the know the relationship between nodes and properties?\n\nlorem ipsum\n    '.strip()
    html = markdown(source)
    @py_assert2 = '\n<h1>Hello World</h1>\n<ul>\n<li>[ ] foo</li>\n<li>[x] bar</li>\n<li>[ ] baz</li>\n<li>[ ]</li>\n<li>[x]</li>\n<li>[ ] Der Unit-Test <code>contextMenuReplacesText</code> wurde auskommentiert um die ausfuehrung zu verhindern. Dieser Test funktioniert in meiner Umgebung nicht wie erwachtet. (Tastatur Layout?, Aktivierte Sprache des Betriebsystems?) Datei: <code>X:\\pdfsam\\pdfsam-fx\\src\\test\\java\\org\\pdfsam\\ui\\prefix\\PrefixFieldTest.java</code></li>\n<li>[ ] What do you know about Magnolia configuration?</li>\n<li>\n<ul>\n<li>[ ] Do you know about the magnolia repository and workspaces?</li>\n</ul>\n</li>\n<li>\n<ul>\n<li>[ ] Do you understand the Node2Bean mechanism?</li>\n</ul>\n</li>\n<li>\n<ul>\n<li>[ ] Do you the know the relationship between nodes and properties?</li>\n</ul>\n</li>\n</ul>\n<p>lorem ipsum</p>\n    '
    @py_assert4 = @py_assert2.strip
    @py_assert6 = @py_assert4()
    @py_assert1 = html == @py_assert6
    if not @py_assert1:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.strip\n}()\n}', ), (html, @py_assert6)) % {'py0': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html',  'py3': @pytest_ar._saferepr(@py_assert2),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert2 = @py_assert4 = @py_assert6 = None
    expected = '\n<h1>Hello World</h1>\n<ul class="checklist">\n<li class="task-list-item"><input type="checkbox" id="ca052d1d7e0a2f787f4ef9937840dcf91e647b08b208df4bbce2e78d527a4f8c"><label for="ca052d1d7e0a2f787f4ef9937840dcf91e647b08b208df4bbce2e78d527a4f8c"> foo</label></li>\n<li class="task-list-item"><input type="checkbox" id="375719a43941c6a5e7f957c74b6f1d7e20cfefd0040181aaf6d3074c8eaac311" checked><label for="375719a43941c6a5e7f957c74b6f1d7e20cfefd0040181aaf6d3074c8eaac311"> bar</label></li>\n<li class="task-list-item"><input type="checkbox" id="7d80d75283fdbf2a3d8a0e2eed45e9d844d1a7482372cd8bc59581725373c179"><label for="7d80d75283fdbf2a3d8a0e2eed45e9d844d1a7482372cd8bc59581725373c179"> baz</label></li>\n<li class="task-list-item"><input type="checkbox"></li>\n<li class="task-list-item"><input type="checkbox" checked></li>\n<li class="task-list-item"><input type="checkbox" id="b10c83b54636ea0620ff6d9e9efb9c034205e0d833d0f9a808657caf3aa2a31e"><label for="b10c83b54636ea0620ff6d9e9efb9c034205e0d833d0f9a808657caf3aa2a31e"> Der Unit-Test <code>contextMenuReplacesText</code> wurde auskommentiert um die ausfuehrung zu verhindern. Dieser Test funktioniert in meiner Umgebung nicht wie erwachtet. (Tastatur Layout?, Aktivierte Sprache des Betriebsystems?) Datei: <code>X:\\pdfsam\\pdfsam-fx\\src\\test\\java\\org\\pdfsam\\ui\\prefix\\PrefixFieldTest.java</code></label></li>\n<li class="task-list-item"><input type="checkbox" id="c7eea1db1eefd672c4679fffeb4e62d8206294d74ae902ec005e169046802bec"><label for="c7eea1db1eefd672c4679fffeb4e62d8206294d74ae902ec005e169046802bec"> What do you know about Magnolia configuration?</label></li>\n<li>\n<ul class="checklist">\n<li class="task-list-item"><input type="checkbox" id="7716b5f69afb42dbcdfeb8bd1bee8d536e98230778640278e44c45a49de416d6"><label for="7716b5f69afb42dbcdfeb8bd1bee8d536e98230778640278e44c45a49de416d6"> Do you know about the magnolia repository and workspaces?</label></li>\n</ul>\n</li>\n<li>\n<ul class="checklist">\n<li class="task-list-item"><input type="checkbox" id="7e6d9c269c7243dd2282bae628b3c27e888784fe638586a5e0d2cadc084ab10d"><label for="7e6d9c269c7243dd2282bae628b3c27e888784fe638586a5e0d2cadc084ab10d"> Do you understand the Node2Bean mechanism?</label></li>\n</ul>\n</li>\n<li>\n<ul class="checklist">\n<li class="task-list-item"><input type="checkbox" id="68cfd25f74d33f39efffd08f83eafe89299e8c2cce1ff486ab611a90022e7674"><label for="68cfd25f74d33f39efffd08f83eafe89299e8c2cce1ff486ab611a90022e7674"> Do you the know the relationship between nodes and properties?</label></li>\n</ul>\n</li>\n</ul>\n<p>lorem ipsum</p>\n    '.strip()
    html = markdown(source, extensions=[ChecklistsExtension()])
    @py_assert1 = html == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (html, expected)) % {'py0': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html',  'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    html = markdown(source, extensions=['markdown_checklists.extension'])
    @py_assert1 = html == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (html, expected)) % {'py0': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html',  'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_syntax_variations():
    source = '\nHello World\n===========\n\n- [x] foo\n- [ ] bar\n- [X] baz\n\nlorem ipsum\n    '.strip()
    html = markdown(source, extensions=[ChecklistsExtension()])
    @py_assert2 = '\n<h1>Hello World</h1>\n<ul class="checklist">\n<li class="task-list-item"><input type="checkbox" id="ca052d1d7e0a2f787f4ef9937840dcf91e647b08b208df4bbce2e78d527a4f8c" checked><label for="ca052d1d7e0a2f787f4ef9937840dcf91e647b08b208df4bbce2e78d527a4f8c"> foo</label></li>\n<li class="task-list-item"><input type="checkbox" id="375719a43941c6a5e7f957c74b6f1d7e20cfefd0040181aaf6d3074c8eaac311"><label for="375719a43941c6a5e7f957c74b6f1d7e20cfefd0040181aaf6d3074c8eaac311"> bar</label></li>\n<li class="task-list-item"><input type="checkbox" id="7d80d75283fdbf2a3d8a0e2eed45e9d844d1a7482372cd8bc59581725373c179" checked><label for="7d80d75283fdbf2a3d8a0e2eed45e9d844d1a7482372cd8bc59581725373c179"> baz</label></li>\n</ul>\n<p>lorem ipsum</p>\n    '
    @py_assert4 = @py_assert2.strip
    @py_assert6 = @py_assert4()
    @py_assert1 = html == @py_assert6
    if not @py_assert1:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.strip\n}()\n}', ), (html, @py_assert6)) % {'py0': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html',  'py3': @pytest_ar._saferepr(@py_assert2),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_class():
    source = '\n* [x] foo\n* [ ] bar\n* [X] baz\n\n----\n\n* [ ] lorem\n* [x] ipsum\n* [ ] ...\n    '.strip()
    html = markdown(source, extensions=[ChecklistsExtension()])
    @py_assert2 = '\n<ul class="checklist">\n<li class="task-list-item"><input type="checkbox" id="ca052d1d7e0a2f787f4ef9937840dcf91e647b08b208df4bbce2e78d527a4f8c" checked><label for="ca052d1d7e0a2f787f4ef9937840dcf91e647b08b208df4bbce2e78d527a4f8c"> foo</label></li>\n<li class="task-list-item"><input type="checkbox" id="375719a43941c6a5e7f957c74b6f1d7e20cfefd0040181aaf6d3074c8eaac311"><label for="375719a43941c6a5e7f957c74b6f1d7e20cfefd0040181aaf6d3074c8eaac311"> bar</label></li>\n<li class="task-list-item"><input type="checkbox" id="7d80d75283fdbf2a3d8a0e2eed45e9d844d1a7482372cd8bc59581725373c179" checked><label for="7d80d75283fdbf2a3d8a0e2eed45e9d844d1a7482372cd8bc59581725373c179"> baz</label></li>\n</ul>\n<hr />\n<ul class="checklist">\n<li class="task-list-item"><input type="checkbox" id="d99f0729bf97ea577a31c7405e3cdd06cd348d2cc5abd49468dd491d5ff80c7c"><label for="d99f0729bf97ea577a31c7405e3cdd06cd348d2cc5abd49468dd491d5ff80c7c"> lorem</label></li>\n<li class="task-list-item"><input type="checkbox" id="c1faa4ff4d958383a5f295634f03a5f1d1dadda2f133b1116c1faf6c4b6c555a" checked><label for="c1faa4ff4d958383a5f295634f03a5f1d1dadda2f133b1116c1faf6c4b6c555a"> ipsum</label></li>\n<li class="task-list-item"><input type="checkbox" id="4501c820f066129ae4d33ca959607e85c8b9aeb7de7e329197c9e307ef05a023"><label for="4501c820f066129ae4d33ca959607e85c8b9aeb7de7e329197c9e307ef05a023"> ...</label></li>\n</ul>\n    '
    @py_assert4 = @py_assert2.strip
    @py_assert6 = @py_assert4()
    @py_assert1 = html == @py_assert6
    if not @py_assert1:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.strip\n}()\n}', ), (html, @py_assert6)) % {'py0': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html',  'py3': @pytest_ar._saferepr(@py_assert2),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_realworld_example():
    source = '\n**09.07.2015 - Getting Startet:**\n\n - [] Der Unit-Test `contextMenuReplacesText` wurde auskommentiert um die ausfuehrung zu verhindern. Dieser Test funktioniert in meiner Umgebung nicht wie erwachtet. (Tastatur Layout?, Aktivierte Sprache des Betriebsystems?) Datei: `X:\\pdfsam\\pdfsam-fx\\src\\test\\java\\org\\pdfsam\\ui\\prefix\\PrefixFieldTest.java`\n - [X] Parent Pom wird nicht gefunden beim starten der pdfsam-community variante. (`mvn exec:java`). Weiterer Schritt noetig um Parent Pom lokal zu installieren: `cd pdfsam-parent && mvn install`, bevor pdfsam-community gestartet werden kann.\n - [ ] Neuer vollstaendiger Befehl um das Projekt zu bauen, im lokalen maven repository zu installieren und pdf-sam community zu starten: `mvn clean install -Dmaven.test.skip=true && cd pdfsam-parent/ && mvn install && cd .. && cd pdfsam-community && mvn exec:java`\n\n    '.strip()
    html = markdown(source)
    @py_assert2 = '\n<p><strong>09.07.2015 - Getting Startet:</strong></p>\n<ul>\n<li>[] Der Unit-Test <code>contextMenuReplacesText</code> wurde auskommentiert um die ausfuehrung zu verhindern. Dieser Test funktioniert in meiner Umgebung nicht wie erwachtet. (Tastatur Layout?, Aktivierte Sprache des Betriebsystems?) Datei: <code>X:\\pdfsam\\pdfsam-fx\\src\\test\\java\\org\\pdfsam\\ui\\prefix\\PrefixFieldTest.java</code></li>\n<li>[X] Parent Pom wird nicht gefunden beim starten der pdfsam-community variante. (<code>mvn exec:java</code>). Weiterer Schritt noetig um Parent Pom lokal zu installieren: <code>cd pdfsam-parent &amp;&amp; mvn install</code>, bevor pdfsam-community gestartet werden kann.</li>\n<li>[ ] Neuer vollstaendiger Befehl um das Projekt zu bauen, im lokalen maven repository zu installieren und pdf-sam community zu starten: <code>mvn clean install -Dmaven.test.skip=true &amp;&amp; cd pdfsam-parent/ &amp;&amp; mvn install &amp;&amp; cd .. &amp;&amp; cd pdfsam-community &amp;&amp; mvn exec:java</code></li>\n</ul>\n    '
    @py_assert4 = @py_assert2.strip
    @py_assert6 = @py_assert4()
    @py_assert1 = html == @py_assert6
    if not @py_assert1:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.strip\n}()\n}', ), (html, @py_assert6)) % {'py0': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html',  'py3': @pytest_ar._saferepr(@py_assert2),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert2 = @py_assert4 = @py_assert6 = None
    html = markdown(source, extensions=[ChecklistsExtension()])
    @py_assert2 = '\n<p><strong>09.07.2015 - Getting Startet:</strong></p>\n<ul>\n<li>[] Der Unit-Test <code>contextMenuReplacesText</code> wurde auskommentiert um die ausfuehrung zu verhindern. Dieser Test funktioniert in meiner Umgebung nicht wie erwachtet. (Tastatur Layout?, Aktivierte Sprache des Betriebsystems?) Datei: <code>X:\\pdfsam\\pdfsam-fx\\src\\test\\java\\org\\pdfsam\\ui\\prefix\\PrefixFieldTest.java</code></li>\n<li class="task-list-item"><input type="checkbox" id="f52fc4f205721240ee423f364cf8f02be6f746b8f896c7b66b6d4ef1a22b8a17" checked><label for="f52fc4f205721240ee423f364cf8f02be6f746b8f896c7b66b6d4ef1a22b8a17"> Parent Pom wird nicht gefunden beim starten der pdfsam-community variante. (<code>mvn exec:java</code>). Weiterer Schritt noetig um Parent Pom lokal zu installieren: <code>cd pdfsam-parent &amp;&amp; mvn install</code>, bevor pdfsam-community gestartet werden kann.</label></li>\n<li class="task-list-item"><input type="checkbox" id="ab359a20aaed490a792e4e5ee94e20e1d57e46ab44c2c450cbc0783c8c2a61be"><label for="ab359a20aaed490a792e4e5ee94e20e1d57e46ab44c2c450cbc0783c8c2a61be"> Neuer vollstaendiger Befehl um das Projekt zu bauen, im lokalen maven repository zu installieren und pdf-sam community zu starten: <code>mvn clean install -Dmaven.test.skip=true &amp;&amp; cd pdfsam-parent/ &amp;&amp; mvn install &amp;&amp; cd .. &amp;&amp; cd pdfsam-community &amp;&amp; mvn exec:java</code></label></li>\n</ul>\n    '
    @py_assert4 = @py_assert2.strip
    @py_assert6 = @py_assert4()
    @py_assert1 = html == @py_assert6
    if not @py_assert1:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.strip\n}()\n}', ), (html, @py_assert6)) % {'py0': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html',  'py3': @pytest_ar._saferepr(@py_assert2),  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert2 = @py_assert4 = @py_assert6 = None