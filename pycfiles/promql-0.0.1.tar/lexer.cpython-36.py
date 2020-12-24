# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/contrib/regular_languages/lexer.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 3407 bytes
__doc__ = '\n`GrammarLexer` is compatible with Pygments lexers and can be used to highlight\nthe input using a regular grammar with token annotations.\n'
from __future__ import unicode_literals
from prompt_tool_kit.document import Document
from prompt_tool_kit.layout.lexers import Lexer
from prompt_tool_kit.layout.utils import split_lines
from prompt_tool_kit.token import Token
from .compiler import _CompiledGrammar
from six.moves import range
__all__ = ('GrammarLexer', )

class GrammarLexer(Lexer):
    """GrammarLexer"""

    def __init__(self, compiled_grammar, default_token=None, lexers=None):
        if not isinstance(compiled_grammar, _CompiledGrammar):
            raise AssertionError
        elif not default_token is None:
            if not isinstance(default_token, tuple):
                raise AssertionError
        else:
            if not lexers is None:
                if not all(isinstance(v, Lexer) for k, v in lexers.items()):
                    raise AssertionError
            if not lexers is None:
                assert isinstance(lexers, dict)
        self.compiled_grammar = compiled_grammar
        self.default_token = default_token or Token
        self.lexers = lexers or {}

    def _get_tokens(self, cli, text):
        m = self.compiled_grammar.match_prefix(text)
        if m:
            characters = [[self.default_token, c] for c in text]
            for v in m.variables():
                lexer = self.lexers.get(v.varname)
                if lexer:
                    document = Document(text[v.start:v.stop])
                    lexer_tokens_for_line = lexer.lex_document(cli, document)
                    lexer_tokens = []
                    for i in range(len(document.lines)):
                        lexer_tokens.extend(lexer_tokens_for_line(i))
                        lexer_tokens.append((Token, '\n'))

                    if lexer_tokens:
                        lexer_tokens.pop()
                    i = v.start
                    for t, s in lexer_tokens:
                        for c in s:
                            if characters[i][0] == self.default_token:
                                characters[i][0] = t
                            i += 1

            trailing_input = m.trailing_input()
            if trailing_input:
                for i in range(trailing_input.start, trailing_input.stop):
                    characters[i][0] = Token.TrailingInput

            return characters
        else:
            return [
             (
              Token, text)]

    def lex_document(self, cli, document):
        lines = list(split_lines(self._get_tokens(cli, document.text)))

        def get_line(lineno):
            try:
                return lines[lineno]
            except IndexError:
                return []

        return get_line