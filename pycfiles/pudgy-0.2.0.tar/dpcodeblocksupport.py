# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/dpcodeblocksupport.py
# Compiled at: 2006-08-12 03:04:37
import docutils.parsers.rst

def code_block(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    """
    The code-block directive provides syntax highlighting for blocks
    of code.  It is used with the the following syntax::

    .. code-block:: Python
 
        class Test(object):
            pass
    
    All code in the indented block following the directive will be put in a
    textarea with the class set to the language. This is useful when combined
    with a Javascript syntax highlighter like dp.SyntaxHighlighter.

    """
    try:
        language = arguments[0]
    except IndexError:
        language = options['language']

    if language.lower() == 'hypertext':
        language = 'html'
    content = ('\n').join(content).replace('&', '&amp;').replace('<', '&lt;')
    content = content.replace('>', '&gt;')
    html = '<textarea name="code" class="%s">\n%s\n</textarea>' % (language.lower(), content)
    raw = docutils.nodes.raw('', html, format='html')
    return [
     raw]


code_block.arguments = (0, 1, 1)
code_block.options = {'language': docutils.parsers.rst.directives.unchanged}
code_block.content = 1
docutils.parsers.rst.directives.register_directive('code-block', code_block)