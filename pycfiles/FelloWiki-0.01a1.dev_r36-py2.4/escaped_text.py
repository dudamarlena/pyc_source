# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/controllers/wikiparser/escaped_text.py
# Compiled at: 2006-11-21 20:30:39
"""fellowiki wiki parser: support for escaped text

TODO
    
"""
from parser import Token, TextToken, ParagraphSeparatorToken, XMLElement
NO_WIKI_TAGS = 'no wiki tags'
PREFORMATTED = 'preformatted'
SINGLE_ESCAPED_CHARACTER = 'single escaped character'

class PreformattedTextToken(ParagraphSeparatorToken):
    __module__ = __name__

    def do_extended_close(self, inserted_token):
        embed = XMLElement('pre')
        embed.append(self.text)
        inserted_token.xhtml.append(embed)


def extend_wiki_parser(wiki_parser):
    wiki_parser.regexes[NO_WIKI_TAGS] = (
     10, '\\[%([^\\\\%\\[]|\\\\.|%[^\\\\\\]])*%\\]', TextToken, dict(cut_left=2, cut_right=2, decode_backslash=True))
    wiki_parser.regexes[PREFORMATTED] = (
     10, '\\[@([^\\\\@]|@?\\\\.|@[^\\\\\\]])*@\\]', PreformattedTextToken, dict(preference=0, cut_left=2, cut_right=2, decode_backslash=True))
    wiki_parser.regexes[SINGLE_ESCAPED_CHARACTER] = (
     10, '\\\\.', TextToken, dict(cut_left=1))