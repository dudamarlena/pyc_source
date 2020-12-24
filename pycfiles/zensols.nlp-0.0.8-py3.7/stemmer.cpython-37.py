# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/nlp/stemmer.py
# Compiled at: 2020-04-17 19:37:40
# Size of source mod 2**32: 691 bytes
"""Stem text using the Porter stemmer.

"""
__author__ = 'Paul Landes'
import logging
from nltk.stem import PorterStemmer
from zensols.nlp import TokenMapper, TokenMapperFactory
logger = logging.getLogger(__name__)

class PorterStemmerTokenMapper(TokenMapper):
    __doc__ = 'Use the Porter Stemmer from the NTLK to stem as normalized tokens.\n\n    '

    def __init__(self, *args, **kwargs):
        (super(PorterStemmerTokenMapper, self).__init__)(*args, **kwargs)
        self.stemmer = PorterStemmer()

    def map_tokens(self, token_tups):
        return (
         map(lambda t: (t[0], self.stemmer.stem(t[1])), token_tups),)


TokenMapperFactory.register(PorterStemmerTokenMapper)