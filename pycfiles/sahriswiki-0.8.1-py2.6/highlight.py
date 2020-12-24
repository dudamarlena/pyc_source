# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sahriswiki/highlight.py
# Compiled at: 2010-07-22 02:45:05
"""Highlighting

...
"""
import pygments, pygments.util, pygments.lexers, pygments.formatters
from genshi import Markup
from genshi.builder import tag

class HTMLFormatter(pygments.formatters.HtmlFormatter):

    def wrap(self, source, outfile):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        yield (0, '<pre xml:space="preserve">')
        for (i, t) in source:
            if not t.strip():
                t = '<br />'
            yield (
             i, t)

        yield (0, '</pre>')


def highlight(text, mime=None, lang=None, linenos=False):
    formatter = HTMLFormatter(cssclass='code', linenos=linenos)
    try:
        if mime:
            lexer = pygments.lexers.get_lexer_for_mimetype(mime)
        elif lang:
            lexer = pygments.lexers.get_lexer_by_name(lang)
        else:
            lexer = pygments.lexers.guess_lexer(text)
    except pygments.util.ClassNotFound:
        return tag.pre(text)

    return Markup(pygments.highlight(text, lexer, formatter))