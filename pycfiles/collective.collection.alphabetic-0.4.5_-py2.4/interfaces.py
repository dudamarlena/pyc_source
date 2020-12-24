# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/collection/alphabetic/interfaces.py
# Compiled at: 2009-06-10 16:49:02
from zope.interface import Interface
from zope.schema import Bool, TextLine
from collective.collection.alphabetic import CollectionAlphabeticMessageFactory as _

class ICharacters(Interface):
    __module__ = __name__

    def __call__(character_tokens, alphabet):
        """Returns characters."""
        pass


class ICharacterTokens(Interface):
    __module__ = __name__

    def __call__(character_tokens, use_alphabet):
        """Clean up tokens by eliminating duplications."""
        pass


class ICharacterOptions(Interface):
    __module__ = __name__
    use_alphabet = Bool(title=_('Use alphabets?'), description=_('Select this option if you want to use alphabets, A-Z.'), default=True, required=False)
    character_tokens = TextLine(title=_('Characters'), description=_('Input characters without any separation.'), required=False)