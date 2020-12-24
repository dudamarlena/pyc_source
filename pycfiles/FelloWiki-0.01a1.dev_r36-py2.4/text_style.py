# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/controllers/wikiparser/text_style.py
# Compiled at: 2006-11-21 20:30:39
"""fellowiki wiki parser: text style

TODO

TODO: translate Textauszeichnungen
    
"""
from parser import XMLElement, EncapsulateToken
EMBED_MARKUP = 'embed markup'
ENCAPSULATE_MARKUP = 'encapsulate markup'
STYLE_OPEN = 'style open'
STYLE_CLOSE = 'style close'
SPECIAL_MARKUP = {'/': ('em', 'italic'), '*': ('b', 'bold'), '_': ('span', 'underlined'), '=': ('tt', 'typewriter'), "'": ('span', 'single_quotes'), '"': ('span', 'double_quotes'), '^': ('span', 'superscript'), ',': ('span', 'subscript'), '#': ('span', 'large'), '~': ('span', 'small')}

class EncapsulateMarkupToken(EncapsulateToken):
    __module__ = __name__

    def __init__(self, token, *args, **kwargs):
        EncapsulateToken.__init__(self, token, *args, **kwargs)
        self.STATE = ENCAPSULATE_MARKUP + self.text
        self.EMBED = EMBED_MARKUP + self.text

    def close(self, match, new_token):
        EncapsulateToken.close(self, match, new_token)
        if new_token.xhtml.is_not_empty():
            new_token.xhtml.tag = SPECIAL_MARKUP[self.text][0]
            new_token.xhtml.attributes['class'] = SPECIAL_MARKUP[self.text][1]
            xhtml = XMLElement('div')
            xhtml.append(new_token.xhtml)
            new_token.xhtml = xhtml
            for xhtml_purge in self.state.pop(self.EMBED, ()):
                xhtml_purge.tag = None

        else:
            new_token.prepend(match.token)
            new_token.append(self.token)
        return


def extend_wiki_parser(wiki_parser):
    wiki_parser.regexes[STYLE_OPEN] = (
     10, '\\[[/\\*_=\\\'"^,#~]', EncapsulateMarkupToken, dict(type='(', preference=20, cut_left=1))
    wiki_parser.regexes[STYLE_CLOSE] = (
     10, '[/\\*_=\\\'"^,#~]\\]', EncapsulateMarkupToken, dict(type=')', preference=20, cut_right=1))