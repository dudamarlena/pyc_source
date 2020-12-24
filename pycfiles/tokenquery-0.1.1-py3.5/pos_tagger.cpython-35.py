# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/nlp/pos_tagger.py
# Compiled at: 2017-01-30 13:19:33
# Size of source mod 2**32: 765 bytes
import nltk
from nltk import pos_tag

class POSTagger:
    __doc__ = '\n        NLTK pos tagger\n    '

    def __init__(self):
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger/averaged_perceptron_tagger.pickle')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')

    def tag(self, tokens):
        """
            add pos tags to token objects

            :param tokens: list of token objects
            :type tokens: list(Token)
            :return: label augmented list of Token objects
            :rtype: list(Token)
        """
        tags = pos_tag([token.get_text() for token in tokens])
        for token, tag in zip(tokens, tags):
            token.add_a_label('pos', tag[1])

        return tokens