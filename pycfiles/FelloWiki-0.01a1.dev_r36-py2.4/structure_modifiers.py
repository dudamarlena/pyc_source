# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/controllers/wikiparser/structure_modifiers.py
# Compiled at: 2006-11-21 20:30:39
"""fellowiki wiki parser: structure modifiers support

TODO
    
"""
from parser import Token, STRUCTUREMOD
STRUCTURE_MODIFIERS = {':': ('align', 'center'), '(': ('align', 'left'), ')': ('align', 'right'), '^': ('valign', 'top'), '-': ('valign', 'middle'), ',': ('valign', 'bottom')}

class StructureModifyToken(Token):
    __module__ = __name__

    def modify(self, modifiers):
        (key, value) = STRUCTURE_MODIFIERS[self.text]
        modifiers[key] = modifiers.get(key, value)

    def is_a(self, *capabilities):
        if STRUCTUREMOD in capabilities:
            return True
        else:
            return Token.is_a(self, *capabilities)


def extend_wiki_parser(wiki_parser):
    wiki_parser.regexes[STRUCTUREMOD] = (10, '<[:()^,\\-]>', StructureModifyToken, dict(cut_left=1, cut_right=1))