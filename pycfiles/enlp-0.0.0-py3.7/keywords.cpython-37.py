# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/enlp/understanding/keywords.py
# Compiled at: 2019-11-27 15:57:30
# Size of source mod 2**32: 1346 bytes
"""
Contains functions for keyword extraction
"""
from rake_nltk import Rake
import string

def keyphrase_list(text, language='english', stopwords=[], min_phrase_len=1, max_phrase_len=2, with_scores=True):
    """Extract keywords from a piece of text

    Parameters
    ----------
    text : :obj:`str`
        text string from which to extract keywords
    language : :obj:`str`
        language of text, must work with nltk
    stopwords : :obj:`list`
       list of stopwords to consider when extracting keywords
    min_phrase_len : :obj:`int`
        minimum token length key phrase can be
    max_phrase_len : :obj:`int`
        maximum token length key phrase can be
    with_scores : :obj:`bool`
        whether to return phrases with score or not, default is True

    Returns
    -------
        r : :obj:`list`
            List of keyphrases

    """
    r = Rake(language=language, stopwords=stopwords,
      punctuations=(string.punctuation),
      min_length=min_phrase_len,
      max_length=max_phrase_len)
    r.extract_keywords_from_text(text)
    if with_scores:
        return r.rank_list
    return r.ranked_phrases