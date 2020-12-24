# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/controllers/wikiparser/special_markup.py
# Compiled at: 2006-11-21 20:30:39
"""fellowiki wiki parser: special markup

TODO
    
"""
from parser import Token, LineBreakToken, LINEBREAK, XMLElement, BetweenParagraphsXHTML
LINEBREAK_OUTPUT = 'linebreak output'
HORIZONTAL_RULE = 'horizontal rule'

class LineBreakOutputToken(LineBreakToken):
    __module__ = __name__

    def render(self, new_token):
        xhtml = XMLElement('br')
        new_token.prepend(xhtml)

    def evaluate(self, result, tokens, state, procs):
        while tokens[0].is_a(LINEBREAK):
            next_token = tokens.pop(0)
            self.token += next_token.token

        while len(result) > 0 and result[(-1)].is_a(LINEBREAK):
            previous_result = result.pop()
            self.token = previous_result.token + self.token

        LineBreakToken.evaluate(self, result, tokens, state, procs)

    is_a = Token.is_a


def extend_wiki_parser(wiki_parser):
    wiki_parser.regexes[LINEBREAK_OUTPUT] = (
     20, '^%%%%%+[ \\t]*(\\n%%%%%+[ \\t]*)*$', LineBreakOutputToken, dict(preference=1))
    wiki_parser.regexes[HORIZONTAL_RULE] = (
     10, '^----$', BetweenParagraphsXHTML, dict(xhtml=XMLElement('hr')))