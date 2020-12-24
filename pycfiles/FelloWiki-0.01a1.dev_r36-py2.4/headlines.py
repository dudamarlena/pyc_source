# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/controllers/wikiparser/headlines.py
# Compiled at: 2006-11-21 20:30:39
"""fellowiki wiki parser: headline support

TODO
    
"""
from parser import PrefixToken, BetweenParagraphsXHTML
HEADLINES = 'headlines'

class HeadlineToken(PrefixToken):
    __module__ = __name__

    def do_prefix(self, new_token):
        new_token.xhtml.tag = 'h%i' % (len(self.token) - 1)
        self.tokens.insert(0, BetweenParagraphsXHTML(self.token, new_token.xhtml))


def extend_wiki_parser(wiki_parser):
    wiki_parser.regexes[HEADLINES] = (
     10, '^={1,6}[ \\t]', HeadlineToken, dict(preference=30))