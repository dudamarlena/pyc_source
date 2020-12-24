# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/core/docs.py
# Compiled at: 2010-05-21 08:57:50
"""Define and register a code-block directive using pygments
"""
from docutils import nodes
from docutils.parsers.rst import directives
try:
    import pygments
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters.html import _get_ttype_class
except ImportError:
    pass

unstyled_tokens = [
 '']

class DocutilsInterface(object):
    """Parse `code` string and yield "classified" tokens.

    Arguments

      code     -- string of source code to parse
      language -- formal language the code is written in.

    Merge subsequent tokens of the same token-type.

    Yields the tokens as ``(ttype_class, value)`` tuples,
    where ttype_class is taken from pygments.token.STANDARD_TYPES and
    corresponds to the class argument used in pygments html output.

    """

    def __init__(self, code, language):
        self.code = code
        self.language = language

    def lex(self):
        try:
            lexer = get_lexer_by_name(self.language)
        except ValueError:
            lexer = get_lexer_by_name('text')

        return pygments.lex(self.code, lexer)

    def join(self, tokens):
        """join subsequent tokens of same token-type
        """
        tokens = iter(tokens)
        (lasttype, lastval) = tokens.next()
        for (ttype, value) in tokens:
            if ttype is lasttype:
                lastval += value
            else:
                yield (
                 lasttype, lastval)
                lasttype, lastval = ttype, value

        yield (
         lasttype, lastval)

    def __iter__(self):
        """parse code string and yield "clasified" tokens
        """
        try:
            tokens = self.lex()
        except IOError:
            print 'INFO: Pygments lexer not found, using fallback'
            yield (
             '', self.code)
            return
        else:
            for (ttype, value) in self.join(tokens):
                yield (
                 _get_ttype_class(ttype), value)


def code_block_directive(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    """parse and classify content of a code_block
    """
    language = arguments[0]
    code_block = nodes.literal_block(classes=['code-block', language])
    for (cls, value) in DocutilsInterface(('\n').join(content), language):
        if cls in unstyled_tokens:
            code_block += nodes.Text(value, value)
        else:
            code_block += nodes.inline(value, value, classes=[cls])

    return [
     code_block]


code_block_directive.arguments = (1, 0, 1)
code_block_directive.content = 1
directives.register_directive('code-block', code_block_directive)
import sys

def trim(docstring):
    """ triming docstrings for docs """
    if not docstring:
        return ''
    lines = docstring.expandtabs().splitlines()
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))

    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())

    while trimmed and not trimmed[(-1)]:
        trimmed.pop()

    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    return ('\n').join(trimmed)