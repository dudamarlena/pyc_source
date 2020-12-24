# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/slopos/__init__.py
# Compiled at: 2014-07-11 18:09:03
import pickle, types, os
from collections import Iterable
this_dir = os.path.dirname(os.path.realpath(__file__))
tagger = pickle.load(open(os.path.join(this_dir, 'sl-tagger.pickle'), 'rb'))

def tag(sentence):
    """
    Tags a sentence with POS symbols. Expected parameter is either text (which will be tokenized on word an punctuation
    boundaries) or a list of words.

    Returns a list of tuples in form (word, tag)
    """
    if isinstance(sentence, types.StringTypes):
        from nltk.tokenize import WordPunctTokenizer
        return tagger.tag(WordPunctTokenizer().tokenize(sentence))
    if isinstance(sentence, Iterable):
        return tagger.tag(sentence)
    raise ArgumentError('Tag parameter MUST be either a string or an iterable collection of words!')