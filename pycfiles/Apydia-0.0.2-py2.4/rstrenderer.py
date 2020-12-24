# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/apydia/renderers/rstrenderer.py
# Compiled at: 2007-10-26 14:28:44
"""
    reST-renderer module for Apydia
    ===============================
    
    To enable pygments based sourcecode highlighting in your reST-docstrings,
    prepend the following to the appropriate sections (instead of eg. "::"):
    
        .. sourcecode:: python
    
"""
from docutils import nodes
from docutils.core import publish_parts
from docutils.parsers.rst import directives
from apydia.renderers.base import HTMLRenderer
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    _pygments_formatter = HtmlFormatter(cssclass='source')

    def _pygments_directive(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
        try:
            lexer = get_lexer_by_name(arguments[0])
        except ValueError:
            lexer = get_lexer_by_name('text')

        parsed = highlight(('\n').join(content), lexer, _pygments_formatter)
        return [nodes.raw('', parsed, format='html')]


    _pygments_directive.arguments = (1, 0, 1)
    _pygments_directive.content = 1
    for directive in ('sourcecode', 'code-block', 'code'):
        directives.register_directive(directive, _pygments_directive)

except ImportError:
    pass

class DocutilsReSTRenderer(HTMLRenderer):
    __module__ = __name__
    name = ('rst', 'reStructuredText', 'reST')

    def _render(self, source):
        settings = dict(pep_references=True, rfc_references=True, tab_width=4)
        try:
            parts = publish_parts(source, writer_name='html', settings_overrides=settings)
            body = parts['body']
        except:
            body = source

        return body