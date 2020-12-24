# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pycommunity/__init__.py
# Compiled at: 2007-02-25 12:00:08
__doc__ = ' Setup pygment extension for reST\n'
from docutils import nodes
from docutils.parsers.rst import directives
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
pygments_formatter = HtmlFormatter()

def pygments_directive(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    try:
        lexer = get_lexer_by_name(arguments[0])
    except ValueError:
        lexer = get_lexer_by_name('text')

    parsed = highlight(('\n').join(content), lexer, pygments_formatter)
    return [
     nodes.raw('', parsed, format='html')]


pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
directives.register_directive('sourcecode', pygments_directive)