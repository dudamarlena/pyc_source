# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ulif/rest/pygments_directive.py
# Compiled at: 2008-02-24 09:47:59
"""
    The Pygments reStructuredText directive
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This fragment is a Docutils_ 0.4 directive that renders source code
    (to HTML only, currently) via Pygments.

    To use it, adjust the options below and copy the code into a module
    that you import on initialization.  The code then automatically
    registers a ``sourcecode`` directive that you can use instead of
    normal code blocks like this::

        .. sourcecode:: python

            My code goes here.

    If you want to have different code styles, e.g. one with line numbers
    and one without, add formatters with their names in the VARIANTS dict
    below.  You can invoke them instead of the DEFAULT one by using a
    directive option::

        .. sourcecode:: python
            :linenos:

            My code goes here.

    Look at the `directive documentation`_ to get all the gory details.

    .. _Docutils: http://docutils.sf.net/
    .. _directive documentation:
       http://docutils.sourceforge.net/docs/howto/rst-directives.html

    :copyright: 2007 by Georg Brandl.
    :license: BSD, see LICENSE for more details.
"""
INLINESTYLES = True
from pygments.formatters import HtmlFormatter
DEFAULT = HtmlFormatter(noclasses=INLINESTYLES)
VARIANTS = {'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True), 'nolinenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=False)}
from docutils import nodes
from docutils.parsers.rst import directives
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer

def pygments_directive(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    try:
        lexer = get_lexer_by_name(arguments[0])
    except ValueError:
        lexer = TextLexer()

    formatter = options and VARIANTS[options.keys()[0]] or DEFAULT
    parsed = highlight(('\n').join(content), lexer, formatter)
    return [nodes.raw('', parsed, format='html')]


pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
pygments_directive.options = dict([ (key, directives.flag) for key in VARIANTS ])
directives.register_directive('sourcecode', pygments_directive)
directives.register_directive('code-block', pygments_directive)