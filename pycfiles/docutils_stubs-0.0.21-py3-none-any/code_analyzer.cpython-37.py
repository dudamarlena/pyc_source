# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/utils/code_analyzer.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 4927 bytes
"""Lexical analysis of formal languages (i.e. code) using Pygments."""
from docutils import ApplicationError
try:
    import pygments
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters.html import _get_ttype_class
    with_pygments = True
except (ImportError, SyntaxError):
    with_pygments = False

unstyled_tokens = [
 'token',
 'text',
 '']

class LexerError(ApplicationError):
    pass


class Lexer(object):
    __doc__ = 'Parse `code` lines and yield "classified" tokens.\n\n    Arguments\n\n      code       -- string of source code to parse,\n      language   -- formal language the code is written in,\n      tokennames -- either \'long\', \'short\', or \'\' (see below).\n\n    Merge subsequent tokens of the same token-type.\n\n    Iterating over an instance yields the tokens as ``(tokentype, value)``\n    tuples. The value of `tokennames` configures the naming of the tokentype:\n\n      \'long\':  downcased full token type name,\n      \'short\': short name defined by pygments.token.STANDARD_TYPES\n               (= class argument used in pygments html output),\n      \'none\':      skip lexical analysis.\n    '

    def __init__(self, code, language, tokennames='short'):
        """
        Set up a lexical analyzer for `code` in `language`.
        """
        self.code = code
        self.language = language
        self.tokennames = tokennames
        self.lexer = None
        if language in ('', 'text') or tokennames == 'none':
            return
        if not with_pygments:
            raise LexerError('Cannot analyze code. Pygments package not found.')
        try:
            self.lexer = get_lexer_by_name(self.language)
        except pygments.util.ClassNotFound:
            raise LexerError('Cannot analyze code. No Pygments lexer found for "%s".' % language)

    def merge(self, tokens):
        """Merge subsequent tokens of same token-type.

           Also strip the final newline (added by pygments).
        """
        tokens = iter(tokens)
        lasttype, lastval = next(tokens)
        for ttype, value in tokens:
            if ttype is lasttype:
                lastval += value
            else:
                yield (
                 lasttype, lastval)
                lasttype, lastval = ttype, value

        if lastval.endswith('\n'):
            lastval = lastval[:-1]
        if lastval:
            yield (
             lasttype, lastval)

    def __iter__(self):
        """Parse self.code and yield "classified" tokens.
        """
        if self.lexer is None:
            yield ([], self.code)
            return
        tokens = pygments.lex(self.code, self.lexer)
        for tokentype, value in self.merge(tokens):
            if self.tokennames == 'long':
                classes = str(tokentype).lower().split('.')
            else:
                classes = [
                 _get_ttype_class(tokentype)]
            classes = [cls for cls in classes if cls not in unstyled_tokens]
            yield (classes, value)


class NumberLines(object):
    __doc__ = "Insert linenumber-tokens at the start of every code line.\n\n    Arguments\n\n       tokens    -- iterable of ``(classes, value)`` tuples\n       startline -- first line number\n       endline   -- last line number\n\n    Iterating over an instance yields the tokens with a\n    ``(['ln'], '<the line number>')`` token added for every code line.\n    Multi-line tokens are splitted."

    def __init__(self, tokens, startline, endline):
        self.tokens = tokens
        self.startline = startline
        self.fmt_str = '%%%dd ' % len(str(endline))

    def __iter__(self):
        lineno = self.startline
        yield (['ln'], self.fmt_str % lineno)
        for ttype, value in self.tokens:
            lines = value.split('\n')
            for line in lines[:-1]:
                yield (
                 ttype, line + '\n')
                lineno += 1
                yield (['ln'], self.fmt_str % lineno)

            yield (
             ttype, lines[(-1)])