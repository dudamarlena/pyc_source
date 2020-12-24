# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reddit2ebook/ebooklib_patched/plugins/sourcecode.py
# Compiled at: 2016-05-13 06:16:04
# Size of source mod 2**32: 2481 bytes
from ebooklib.plugins.base import BasePlugin
from ebooklib.utils import parse_html_string

class SourceHighlighter(BasePlugin):

    def __init__(self):
        pass

    def html_before_write(self, book, chapter):
        from lxml import etree, html
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from ebooklib import epub
        try:
            tree = parse_html_string(chapter.content)
        except:
            return

        root = tree.getroottree()
        had_source = False
        if len(root.find('body')) != 0:
            body = tree.find('body')
            for source in body.xpath('//pre[contains(@class,"source-")]'):
                css_class = source.get('class')
                source_text = (source.text or '') + ''.join([html.tostring(child) for child in source.iterchildren()])
                if 'source-python' in css_class:
                    from pygments.lexers import PythonLexer
                    _text = highlight(source_text, PythonLexer(), HtmlFormatter())
                if 'source-css' in css_class:
                    from pygments.lexers import CssLexer
                    _text = highlight(source_text, CssLexer(), HtmlFormatter())
                _parent = source.getparent()
                _parent.replace(source, etree.XML(_text))
                had_source = True

        if had_source:
            chapter.add_link(href='style/code.css', rel='stylesheet', type='text/css')
            chapter.content = etree.tostring(tree, pretty_print=True, encoding='utf-8')