# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/controllers/wikiparser/text_style_simple.py
# Compiled at: 2006-11-21 20:30:39
"""fellowiki wiki parser: special markup

TODO
    
"""
from parser import Token, XMLElement, WHITESPACE
from text_style import SPECIAL_MARKUP, EMBED_MARKUP, ENCAPSULATE_MARKUP
SWITCH_MARKUP = 'switch markup'

class SwitchMarkupToken(Token):
    __module__ = __name__

    def __init__(self, token, *args, **kwargs):
        Token.__init__(self, token, *args, **kwargs)
        self.STATE = SWITCH_MARKUP + self.text
        self.EMBED = EMBED_MARKUP + self.text

    def evaluate(self, result, tokens, state, procs):
        Token.evaluate(self, result, tokens, state, procs)
        state[self.STATE] = state.get(self.STATE, 0) + 1

    def match_is_open(self):
        return self.state.get(self.STATE, 0) > 0

    def close_matching(self, match):
        return self.state.get(self.STATE, 0) == 1 and match.is_a(SWITCH_MARKUP)

    def close(self, match, new_token):
        self.state[self.STATE] = self.state.get(self.STATE, 0) - 2
        if new_token.xhtml.is_not_empty():
            new_token.xhtml.tag = SPECIAL_MARKUP[self.text][0]
            new_token.xhtml.attributes['class'] = SPECIAL_MARKUP[self.text][1]
            if self.state.get(ENCAPSULATE_MARKUP + self.text, 0) > 0:
                if not self.state.has_key(self.EMBED):
                    self.state[self.EMBED] = []
                self.state[self.EMBED].append(new_token.xhtml)
            xhtml = XMLElement('div')
            xhtml.append(new_token.xhtml)
            new_token.xhtml = xhtml
        else:
            new_token.prepend(match.token)
            new_token.append(self.token)
        self.tokens.insert(0, new_token)

    def render(self, new_token):
        self.state[self.STATE] = self.state.get(self.STATE, 0) - 1
        Token.render(self, new_token)

    def is_a(self, *capabilities):
        return SWITCH_MARKUP in capabilities


def extend_wiki_parser(wiki_parser):
    regex_whitespace = wiki_parser.regexes[WHITESPACE]

    class WhitespaceToken(regex_whitespace[2]):
        __module__ = __name__

        def evaluate(self, result, tokens, state, procs):
            regex_whitespace[2].evaluate(self, result, tokens, state, procs)
            for key in SPECIAL_MARKUP.keys():
                state[SWITCH_MARKUP + key] = 0

    wiki_parser.regexes[WHITESPACE] = (regex_whitespace[0], regex_whitespace[1], WhitespaceToken, regex_whitespace[3])
    wiki_parser.regexes[SWITCH_MARKUP] = (
     90, '[/\\*_=]', SwitchMarkupToken, dict(preference=90))