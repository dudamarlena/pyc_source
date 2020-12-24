# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/apydia/renderers/markdownrenderer.py
# Compiled at: 2007-11-28 06:40:55
"""
    Markdown Renderer
    =================
    
    The markdown/Pygments code highlighting integration is a stripped down
    version of "CodeHilite" which can be found at
    http://achinghead.com/markdown/codehilite/ .
"""
import re
from apydia.renderers.base import HTMLRenderer
from markdown import Markdown, Preprocessor
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
from pygments.util import ClassNotFound
__all__ = [
 'MarkdownRenderer']

class Highlighter(object):
    __module__ = __name__
    lang_detect = re.compile('\n        (?:(?:::+)|(?P<shebang>[#]!))\n        (?P<path>(?:/\\w+)*[/ ])?\n        (?P<lang>\\w*)\n    ', re.VERBOSE)

    def __init__(self, text):
        self.text = text
        self.formatter = HtmlFormatter(cssclass='source')
        self.lang = None
        lines = self.text.splitlines()
        first_line = lines.pop(0)
        matches = self.lang_detect.search(first_line)
        if matches:
            try:
                self.lang = matches.group('lang').lower()
            except IndexError:
                pass
            else:
                if matches.group('path'):
                    lines.insert(0, first_line)
        else:
            lines.insert(0, first_line)
        self.text = ('\n').join(lines).strip('\n')
        return

    def highlight(self):
        if self.lang:
            lexer = get_lexer_by_name(self.lang)
        else:
            try:
                lexer = guess_lexer(self.text)
            except ClassNotFound:
                lexer = get_lexer_by_name('text')

        return highlight(self.text, lexer, self.formatter)


class MarkdownRenderer(HTMLRenderer):
    __module__ = __name__
    name = 'markdown'

    def __init__(self):
        self.markdown = md = Markdown(safe_mode=False)

        def _highlight_block(parent_elem, lines, in_list):
            (detabbed, rest) = md.blockGuru.detectTabbed(lines)
            text = ('\n').join(detabbed).rstrip() + '\n'
            code = Highlighter(text)
            placeholder = md.htmlStash.store(code.highlight())
            parent_elem.appendChild(md.doc.createTextNode(placeholder))
            md._processSection(parent_elem, rest, in_list)

        self.markdown._processCodeBlock = _highlight_block

    def _render(self, source):
        if not source:
            return ''
        return self.markdown.__str__(source)