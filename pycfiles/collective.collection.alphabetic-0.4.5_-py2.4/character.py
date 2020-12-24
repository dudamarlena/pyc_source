# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/collection/alphabetic/utility/character.py
# Compiled at: 2009-06-10 17:42:06
from zope.interface import implements
from collective.collection.alphabetic.interfaces import ICharacters, ICharacterTokens
from collective.collection.alphabetic.config import ALPHABETS

class Characters(object):
    __module__ = __name__
    implements(ICharacters)

    def __call__(self, character_tokens, alphabet):
        if alphabet:
            alphabets = list(ALPHABETS)
            if character_tokens:
                tokens = [ unicode(character) for character in character_tokens ]
                return alphabets + tokens
            else:
                return alphabets
        elif character_tokens is not None:
            return [ unicode(character) for character in character_tokens ]
        else:
            None
        return


class CharacterTokens(object):
    __module__ = __name__
    implements(ICharacterTokens)

    def __call__(self, tokens, use_alphabet):
        uni_tokens = unicode(tokens.upper())
        tokens = ''
        if use_alphabet:
            alphabets = ALPHABETS
            for token in uni_tokens:
                if token not in alphabets + tokens:
                    tokens += token

            tokens = tokens.replace(' ', '')
            return tuple(tokens)
        else:
            for token in uni_tokens:
                if token not in tokens:
                    tokens += token

            tokens = tokens.replace(' ', '')
            return tuple(tokens)