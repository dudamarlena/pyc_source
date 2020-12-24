# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jsick/.virtualenvs/paperweight/lib/python2.7/site-packages/paperweight/nlputils.py
# Compiled at: 2015-01-12 15:16:16
"""
Utility functions for working with NLTK
"""
import nltk

def wordify(text):
    """Generate a list of words given text, removing punctuation.

    Parameters
    ----------
    text : unicode
        A piece of english text.

    Returns
    -------
    words : list
        List of words.
    """
    stopset = set(nltk.corpus.stopwords.words('english'))
    tokens = nltk.WordPunctTokenizer().tokenize(text)
    return [ w for w in tokens if w not in stopset ]