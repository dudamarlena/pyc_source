# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/pygmentsupport.py
# Compiled at: 2007-01-07 21:35:14
import docutils.parsers.rst
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.formatters import HtmlFormatter

def code_block(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    """
    The code-block directive provides syntax highlighting for blocks
    of code.  It is used with the the following syntax::

    .. code-block:: Python
 
        class Test(object):
            pass
    
    The code will be highlighted with the pygments syntax highlighter. It's
    recommended that you include the appropriate stylesheets when using this
    highlighter.
    """
    try:
        language = arguments[0]
    except IndexError:
        language = options['language']

    language = language.lower()
    if language == 'hypertext':
        language = 'html'
    if language == 'pasteini':
        language = 'ini'
    lexer = get_lexer_by_name(language, stripall=True)
    formatter = HtmlFormatter(linenos=True, cssclass='syntax', encoding='utf-8')
    html = highlight(unicode(('\n').join(content)), lexer, formatter).decode('utf-8')
    raw = docutils.nodes.raw('', html, format='html')
    return [
     raw]


code_block.arguments = (0, 1, 1)
code_block.options = {'language': docutils.parsers.rst.directives.unchanged}
code_block.content = 1
docutils.parsers.rst.directives.register_directive('code-block', code_block)